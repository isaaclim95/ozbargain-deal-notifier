from bs4 import BeautifulSoup
import urllib3
from tabulate import tabulate
import re
import sys
import time


def main():

    # Time in seconds before scraping again
    delay = 60
    # Show posts with upvotes higher than upvote_threshold
    upvote_threshold = 150

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    results_dict = {}
    while True:
        print("Scraping site...")
        file = open("ozbargain.html", "w", encoding="utf-8")
        file.write("<!DOCTYPE html>\n")
        file.write("<html>\n")
        file.write("<head>\n")
        file.write("	<title>Ozbargain Links</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("	<ul>\n")

        for x in range(20):
            url = "https://www.ozbargain.com.au/?page=" + str(x)

            http = urllib3.PoolManager()
            html = http.request('GET', url).data

            # html = urllib3.urlopen(url, headers={'User-Agent': 'Mozilla/5.0'})

            while True:
                try:
                    soup = BeautifulSoup(html, 'html.parser')
                except Exception:
                    continue
                break
            first_div = soup.findAll("div", {"class": "node node-ozbdeal node-teaser"})

            for div in first_div:
                # Finding upvotes
                tags = div.findAll("div", {"class": "n-vote n-deal inact"})
                for tag in tags:
                    tags2 = tag.findAll("span", {"class": "nvb voteup"})
                    for tag in tags2:
                        match = re.search("[0-9]+", str(tag))
                        upvotes = int(match[0])
                if upvotes >= upvote_threshold:
                    # Finding title
                    tags = div.findAll("h2", {"class": "title"})
                    for tag in tags:
                        matches = re.findall(r'"([^"]*)"', str(tag))
                        title = matches[1]
                    if title not in results_dict:
                        # Finding links
                        tags = div.find_all('a', href=True)
                        bargain_link = "https://www.ozbargain.com.au" + tags[0].get_attribute_list('href')[0]
                        ozb_link = "https://www.ozbargain.com.au" + tags[1].get_attribute_list('href')[0]
                        results_dict[title] = (upvotes, ozb_link, bargain_link)
                        # print("Added {} {} {} {}".format(upvotes, title, ozb_link, bargain_link))

        for key in results_dict:
            file.write("   <li><a href=" + results_dict[key][1] + ">" + key + "</li>\n")
        file.write("	</ul>\n")
        file.write("</body>\n")
        file.write("</html>\n")
        file.close()
        print("Generated .html file")
        print("Waiting for " + str(delay / 60) + " minutes...")
        try:
            time.sleep(delay)
        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)
        print("Searching...")


if __name__ == "__main__":
    main()


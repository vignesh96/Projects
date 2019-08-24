import requests
from bs4 import BeautifulSoup


class ScrapeIndeed(object):

    def __init__(self):
        self.params = {}
        self.headers = {"Accept": "application/json"}
        self.url = "https://www.indeed.co.in/jobs"
        self.what = None
        self.city = None
        self.state = None
        self.soups = []

    def get_input(self):
        self.what = input("Enter the role/job you want : ")
        self.city = input("Enter the city of preference : ")
        self.state = input("Enter the state of preference : ")
        self.params = {"q": self.what.strip(), "l": self.city.strip() + ", " + self.state.strip(), "start": 0}

    def start_process(self):
        try:
            self.get_input()

            page_no = 1
            # Scrape all the results pages
            while True:
                print("In Page {page_no}".format(page_no=page_no))

                self.params["start"] = (page_no - 1) * 10
                response = requests.get(url=self.url, params=self.params, headers=self.headers, verify=False)
                # print(response.text)
                soup = BeautifulSoup(response.text, "html.parser")
                total_results = soup.find(id="searchCount").get_text()
                page_number = int(
                    total_results[total_results.index("e") + 1:total_results.index("of")].replace(",", "").strip())
                print(page_number)
                if page_no == page_number:
                    self.soups.append(soup)
                else:
                    break
                page_no += 1
            return self.soups
        except Exception as exp_msg:
            print(exp_msg)

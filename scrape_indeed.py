import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

class ScrapeIndeed(object):

    def __init__(self):
        self.params = {}
        self.headers = {"Accept": "application/json"}
        self.url = "https://www.indeed.co.in/jobs"
        self.what = None
        self.city = None
        self.state = None
        self.job_titles_list = []

    def get_input(self):
        self.what = input("Enter the role/job you want : ")
        self.city = input("Enter the city of preference : ")
        self.state = input("Enter the state of preference : ")
        self.params = {"q": self.what.strip(), "l": self.city.strip(), "start": "0"}

    def extract_job_titles(self, soup):
        try:
            jobs = []
            for div in soup.find_all(name="div", attrs={"class":"row"}):
                for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
                    jobs.append(a["title"])
            return (jobs)
        except Exception as exception_msg:
            print(exception_msg)

    def plot_frequency_job_titles(self):
        # Get frequency of job titles
        job_title_df = pd.Series(self.job_titles_list)
        job_freqs = job_title_df.value_counts().to_dict()
        num_of_items = len(list(job_freqs.keys()))
        ind = np.arange(0, num_of_items*2, 2)
        plt.figure(figsize=(100, 20))
        plt.bar(ind, list(job_freqs.values()), width=1, align='center', color='green')
        plt.xlabel("Job Titles", fontsize=5)
        plt.ylabel("# of Job Titles", fontsize=5)
        plt.xticks(ind, list(job_freqs.keys()), rotation=90)
        plt.title("Number of Job Titles")
        plt.show()

    def start_process(self):
        try:
            self.get_input()
            # Scrape first 10 pages
            for i in range(0, 10):
                self.params["start"] = str(int(self.params["start"]) + 10)
                response = requests.get(url=self.url, params=self.params, headers=self.headers, verify=False)
                #print(response.text)
                soup = BeautifulSoup(response.text, "html.parser")
                job_title_page = self.extract_job_titles(soup)
                self.job_titles_list.extend(job_title_page)

            print(self.job_titles_list)
            self.plot_frequency_job_titles()

        except Exception as exp_msg:
                print(exp_msg)


if __name__ == "__main__":
    scrape_indeed = ScrapeIndeed()
    scrape_indeed.start_process()
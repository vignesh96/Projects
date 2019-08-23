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
        self.params = {"q": self.what.strip(), "l": self.state.strip(), "start": "0"}

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
        plt.figure(figsize=(8, 36))
        plt.barh(y=list(job_freqs.keys()), width=list(job_freqs.values()))
        plt.ylabel("Job Titles", fontsize=5)
        plt.xlabel("# of Job Titles", fontsize=5)
        plt.yticks(np.arange(0, len(list(job_freqs.keys()))))
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
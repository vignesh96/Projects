import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


class ScrapeIndeed(object):

    def __init__(self):
        self.job_details_list = []
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
        self.params = {"q": self.what.strip(), "l": self.city.strip() + ", " + self.state.strip(), "start": 0}

    def extract_job_infos(self, soup):
        try:
            jobs = []
            jobs_info = []
            for div in soup.find_all(name="div", attrs={"class": "row"}):
                # Extract job titles
                for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
                    jobs.append(a["title"])
                    title = a["title"]

                # Extract Company name
                company_link = div.find(name="span", attrs={"class":"company"})
                company = company_link.find(name="a", attrs={"class": "turnstileLink"})

                if not company:
                    company = company_link.text.strip()
                else:
                    company = company.text.strip()
                print(company)

                # Extract Location of the Comapany
                

                # Salary of the job
                salary = div.find(name="span", attrs={"class": "salary"})
                if not salary:
                    salary = None
                else:
                    salary = salary.text.strip()
                jobs_info.append([title, company, salary])
            return (jobs, jobs_info)
        except Exception as exception_msg:
            print(exception_msg)

    def plot_frequency_job_titles(self):
        # Get frequency of job titles
        job_title_df = pd.Series(self.job_titles_list)
        job_freqs = job_title_df.value_counts().to_dict()
        num_of_items = len(list(job_freqs.keys()))
        ind = np.arange(0, num_of_items * 2, 2)
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

            # Scrape first result page
            response = requests.get(url=self.url, params=self.params, headers=self.headers, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")
            # Get total results and last page number
            total_results = soup.find(id="searchCount").get_text()
            print(total_results)
            last_page = int(
                total_results[total_results.index("of") + 2: total_results.index("jobs")].replace(",", "").strip())
            print(last_page)

            if last_page < 10:
                job_title_page = self.extract_job_infos(soup)
                self.job_titles_list.extend(job_title_page)
            else:
                page_no = 0
                # Scrape all the results pages
                while len(self.job_titles_list) < last_page:
                    print("In Page {page_no}".format(page_no=page_no + 1))

                    self.params["start"] = page_no * 10
                    response = requests.get(url=self.url, params=self.params, headers=self.headers, verify=False)
                    # print(response.text)
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_title_page, jobs_info = self.extract_job_infos(soup)
                    self.job_titles_list.extend(job_title_page)
                    self.job_details_list.extend(jobs_info)
                    print(job_title_page)
                    print(len(self.job_titles_list))
                    page_no += 1

            print(self.job_titles_list)
            print(self.job_details_list)
            self.plot_frequency_job_titles()

        except Exception as exp_msg:
            print(exp_msg)


if __name__ == "__main__":
    scrape_indeed = ScrapeIndeed()
    scrape_indeed.start_process()

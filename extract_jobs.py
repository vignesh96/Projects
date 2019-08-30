import os
from datetime import datetime

import pandas as pd


class ExtractJob(object):

    def __init__(self, soups):
        self.job_titles_list = []
        self.job_details_list = []
        self.soups = soups
        self.columns = ["job_title", "company", "location", "salary", "job_description", "data_jk", "data_empn"]

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
                company_link = div.find(name="span", attrs={"class": "company"})
                company = company_link.find(name="a", attrs={"class": "turnstileLink"})

                if not company:
                    company = company_link.text.strip()
                else:
                    company = company.text.strip()

                # Extract Location of the Comapany
                location = div.find(name="span", attrs={"class": "location"})

                if not location:
                    location = None
                else:
                    location = location.text
                # print(location)

                # Salary of the job
                salary = div.find(name="span", attrs={"class": "salary"})
                if not salary:
                    salary = None
                else:
                    salary = salary.text.strip()

                # Get job descriptions
                span = div.find("div", attrs={"class": "summary"})
                job_desc = span.text.strip()

                # Get attributes for fetching the content
                data_jk = div["data-jk"]
                data_empn = div.get("data-empn", "")
                print(data_jk, data_empn)
                # print(job_desc)
                jobs_info.append([title, company, location, salary, job_desc, data_jk, data_empn])

            return (jobs, jobs_info)
        except Exception as exception_msg:
            print(exception_msg)

    def start_extract(self):
        for s in self.soups:
            job_title_page, jobs_info = self.extract_job_infos(s)
            self.job_titles_list.extend(job_title_page)
            self.job_details_list.extend(jobs_info)

        indeed_jobs_frame = pd.DataFrame(self.job_details_list)
        indeed_jobs_frame.transpose()
        indeed_jobs_frame.columns = self.columns
        file_name_csv = os.path.join(os.getcwd(), "scrapped_data", "indeed-{}.csv".format(datetime.now().date()))
        indeed_jobs_frame.to_csv(open(file_name_csv, 'w+', encoding='utf-8'), sep="|", na_rep=None)

        return indeed_jobs_frame

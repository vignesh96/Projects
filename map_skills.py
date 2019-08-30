import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


class MapSkills(object):

    def __init__(self, what, city, state, skills):
        self.indeed_data = None
        self.url = "https://www.indeed.co.in/viewjob"
        self.headers = {"Accept": "application/json"}
        self.what = what
        self.city = city
        self.state = state
        self.skills = skills
        self.job_descriptions = []
        self.stop_words = set(stopwords.words("english"))
        self.skill_freq = {}

    def plot_skills(self):
        self.job_descriptions = self.get_job_descriptions()

        # Removing stop words
        for i, desc in enumerate(self.job_descriptions):
            desc_list = desc.split()
            resultwords = [word.lower() for word in desc_list if word.lower() not in self.stop_words]
            print(resultwords)
            self.job_descriptions[i] = ' '.join(resultwords)

        # Compute word frequencies
        for desc in self.job_descriptions:
            for skill in self.skills:
                if skill not in self.skill_freq:
                    self.skill_freq[skill] = desc.count(skill.lower())
                else:
                    self.skill_freq[skill] += desc.count(skill.lower())

        # Plot the frequencies
        num_of_items = len(list(self.skill_freq.keys()))
        ind = np.arange(0, num_of_items*2, 2)
        plt.figure(figsize=(100, 50))
        plt.bar(ind, list(self.skill_freq.values()), width=1, align='center', color='green')
        plt.xlabel("Skill Sets", fontsize=5)
        plt.ylabel("Demand of skill sets", fontsize=5)
        plt.xticks(ind, list(self.skill_freq.keys()), rotation=90)
        plt.title("Demand for the skill set {}".format(self.what))
        plt.savefig(os.path.join(os.getcwd(), "plots", "{}{}-skill_sets.jpg".format(self.what, self.city)))

    def plot_frequency_job_titles(self):
        # Get frequency of job titles
        # Plot frequency of top 10 job titles
        job_title_df = self.indeed_data[:10]["job_title"]
        job_freqs = job_title_df.value_counts().to_dict()
        num_of_items = len(list(job_freqs.keys()))
        ind = np.arange(0, num_of_items * 2, 2)
        plt.figure(figsize=(100, 20))
        plt.bar(ind, list(job_freqs.values()), width=1, align='center', color='green')
        plt.xlabel("Job Titles", fontsize=5)
        plt.ylabel("# of Job Titles", fontsize=5)
        plt.xticks(ind, list(job_freqs.keys()), rotation=90)
        plt.title("Number of Job Titles")
        plt.savefig(os.path.join(os.getcwd(), "plots", "{}{}-job-titles.jpg".format(self.what, self.city)))

    def get_job_descriptions(self):

        job_description = []
        number_of_jobs = self.indeed_data.shape[0]
        data_jk = self.indeed_data["data_jk"].tolist()

        companies = self.indeed_data["company"].tolist()
        job_titles = self.indeed_data["job_title"].tolist()
        for i in range(20):
            params = {"cmp": companies[i], "t": job_titles[i], "jk": data_jk[i]}
            print(params)
            response = requests.get(url=self.url, params=params, headers=self.headers, verify=False)
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove script and styles
            for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
                script.extract()

            job_description.append(soup.text)

        return job_description

    def clean_data(self):
        # Drop sequence column
        self.indeed_data = self.indeed_data.drop(self.indeed_data.columns[[0]], axis=1)
        # print(self.indeed_data)

        # Remove duplicate entries
        self.indeed_data.drop_duplicates(keep=False, inplace=True)

        # Clean data_jk column values
        self.indeed_data["data_jk"].fillna("", inplace=True)

        # cleaning salaries

        self.indeed_data["salary"] = self.indeed_data["salary"].str.replace("₹", "")
        self.indeed_data["salary"] = self.indeed_data["salary"].str.replace(",", "")
        self.indeed_data["salary"] = self.indeed_data["salary"].str.strip()
        print(self.indeed_data["salary"])
        salary_range = self.indeed_data["salary"].str.replace("a year", "")
        salary_range = salary_range.str.replace("a month", "")
        salary_range = salary_range.str.replace("a day", "")

        # seperating salary range into two columns
        salary_range = salary_range.str.strip()
        salary_range = salary_range.str.split("-", n=1, expand=True)
        salary_min = salary_range[0]
        salary_max = salary_range[1]
        salary_min = salary_min.str.strip()
        salary_max = salary_max.str.strip()
        salary_min[salary_min.isnull()] = 0
        salary_max[salary_max.isnull()] = 0

        # Create two new columns
        self.indeed_data["salary_min (₹)"] = salary_min
        self.indeed_data["salary_max (₹)"] = salary_max
        self.indeed_data[["salary_min (₹)", "salary_max (₹)"]] = \
            self.indeed_data[["salary_min (₹)", "salary_max (₹)"]].apply(pd.to_numeric)
        self.indeed_data["salary"].fillna("0", inplace=True)
        self.indeed_data.loc[self.indeed_data.loc[:, "salary"].str.contains("year"), "salary_min (₹)"] //= 12
        self.indeed_data.loc[self.indeed_data.loc[:, "salary"].str.contains("year"), "salary_max (₹)"] //= 12
        self.indeed_data.loc[self.indeed_data.loc[:, "salary"].str.contains("day"), "salary_min (₹)"] *= 30
        self.indeed_data.loc[self.indeed_data.loc[:, "salary"].str.contains("day"), "salary_max (₹)"] *= 30

        print(self.indeed_data.dtypes)

    def start_mapping(self):
        scrapped_indeed_files = os.listdir(os.path.join(os.getcwd(), "scrapped_data"))

        for scrapped_file in scrapped_indeed_files:
            indeed_job_file_name = os.path.join(os.getcwd(), "scrapped_data", scrapped_file)
            self.indeed_data = pd.read_csv(indeed_job_file_name, delimiter="|")
            print(self.indeed_data.columns.values)
            self.clean_data()
            self.plot_skills()
            self.plot_frequency_job_titles()


if __name__ == "__main__":
    job_search_input_file_path = os.path.join(os.getcwd(), "input", "job_search_input.json")

    job_search_input_data = json.load(open(job_search_input_file_path, "r"))

    for job_input in job_search_input_data:
        map = MapSkills(what=job_input["field"], city=job_input["city"], state=job_input["state"],
                        skills=job_input["skills_needed"])
        map.start_mapping()

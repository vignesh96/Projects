import os
import pandas as pd
from collections import Counter

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import requests


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





    def get_job_descriptions(self):

        job_description = []
        number_of_jobs = self.indeed_data.shape[0]
        data_jk = self.indeed_data["data_jk"].tolist()
        # data_empn = self.indeed_data["data_empn"].tolist()
        companies = self.indeed_data["company"].tolist()
        job_titles = self.indeed_data["job_title"].tolist()
        for i in range(5):
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

        print(self.indeed_data.dtypes)

    def start_mapping(self):
        indeed_job_file_name = os.path.join(os.getcwd(), "scrapped_data", "indeed-2019-08-28.csv")
        self.indeed_data = pd.read_csv(indeed_job_file_name, delimiter="|")
        print(self.indeed_data.columns.values)
        self.clean_data()
        self.plot_skills()


if __name__ == "__main__":
    map = MapSkills(what="game",city="Chennai",state="Tamil Nadu",skills=["artist", "Python", "C#", "Unity"])
    map.start_mapping()

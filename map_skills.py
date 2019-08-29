import os
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
import requests

class MapSkills(object):

    def __init__(self):
        self.indeed_data = None

    def plot_skills(self):
        self.get_job_description()

    def get_job_description(self):
        params = {"q": self.what.strip(), "l": self.city.strip() + ", " + self.state.strip(), "start": 0}

    def clean_data(self):

        # Drop sequence column
        self.indeed_data = self.indeed_data.drop(self.indeed_data.columns[[0]], axis=1)
        # print(self.indeed_data)

        # Remove duplicate entries
        self.indeed_data.drop_duplicates(keep=False, inplace=True)

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
    map = MapSkills()
    map.start_mapping()
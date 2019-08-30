import json
import os

from extract_jobs import ExtractJob
from scrape_indeed import ScrapeIndeed

if __name__ == "__main__":
    job_search_input_file_path = os.path.join(os.getcwd(), "input", "job_search_input.json")

    job_search_input_data = json.load(open(job_search_input_file_path, "r"))
    for job_input in job_search_input_data:
        what = job_input.get("field", "")
        city = job_input.get("city", "")
        state = job_input.get("state", "")
        skills = job_input.get("skills_needed", "")
        scrape_indeed = ScrapeIndeed(what=what, city=city, state=state)
        soups = scrape_indeed.start_process()
        extract_jobs = ExtractJob(soups=soups)
        extract_jobs.start_extract()

from extract_jobs import ExtractJob
from scrape_indeed import ScrapeIndeed

if __name__ == "__main__":
    scrape_indeed = ScrapeIndeed()
    soups = scrape_indeed.start_process()
    extract_jobs = ExtractJob(soups=soups)
    extract_jobs.start_extract()

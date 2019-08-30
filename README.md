# Indeed Scraper

This application scrapes the data from www.indeed.co.in based on the input that is configured under <b>input</b> folder. The scraped data is used for the following - 
<ul>
    <li> Data is cleaned for duplicates and salary is converted to integer </li>
    <li> Visualize the top 10 job titles that are in demand </li>
    <li> Determine which skill sets are sought more </li>
</ul>

## Configuration

The input to be used for scraping is provided under input folder with file name <i> job_search_input.json</i>. The file has the following attributes in the form of the list - 
<ul>
    <li> field - Field that is sought by you </li>
    <li> city - City of interest</li>
    <li> state - State of interest </li>
    <li> skills_needed - Skills that are to be searched upon </li>
</ul> 

A cron job will be run on the <i> analyse_indeed.py</i> file to scrape the data and form a data frame to the <b>scrapped_data</b> folder. 
Another cron job will be run on <i>map_skills.py</i> which will clean the dataset and save the visual data in <b>plots</b> folder.

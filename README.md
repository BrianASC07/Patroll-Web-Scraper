# Patroll Web Scraper


## Overview
Patroll Web Scraper is a Python-based tool that uses Selenium and BeautifulSoup to extract contest data from United Patents Patroll. It collects contest titles, patent IDs, prior art references, and contest links for won contests, saving the results in a structured JSON file. It can also collect data from the PDFs of the winning prior art. Included is also functionality that allows users to be notified whenever a new winning patent is detected.


## Setup and Usage
Prerequisites:
* Python 3.0+
* Google Chrome browser
* ChromeDriver
* Required Python packages: ```pip install beautifulsoup selenium```


To run the main contest scraper to collect contest data and evaluate the accuracy of the scraped prior art against ground truth, run:
```python Autopat_scraper_and_evaluator.py```


To notify people upon receiving new contests, run:
```python notifier.py```


To run the main contest PDF scraper to collect data from the winning contest PDFs, run:
```python New_Scraper.py```




## Project Structure
**Scraper_evaluator.py**
* Compares scraped prior art patent IDs against a dictionary of true values. Calculates accuracy, precision, recall, and success rate for evaluation.


**Scrape_won_contests_to_json.py**
* Uses helper functions to scrape contests and outputs contest title, troll patent ID, prior art IDs, and URL as a JSON file titled, “won_patent_contests.json”.


**Autopat_scraper_and_evaluator.py**
* End-to-end script that combines contest scraping and evaluation. Outputs contest title, troll patent ID, prior art IDs, and URL, then evaluates performance metrics. Each contest is stored on a &lt;li&gt; tag on the main page. The hierarchy is structured like this, storing the link.


![image](https://github.com/user-attachments/assets/6e9b7792-2500-49bf-9130-66f5aed6792d)




**New_Scraper.py**
* Uses helper functions to scrape the  1 and 1a sections from the winning art PDFs.


**notifier.py**
* Sends users email notifications upon detecting new patents.
### Helper Functions
**extract_prior_art.py**
* Navigates to a contest page and returns the URL for the “DOWNLOAD WINNING PRIOR ART HERE” link. Returns a list of prior art patent IDs from a contest page.


**extract_contest_title.py**
* Returns the contest title by extracting the h1 tag from the contest page.


**PDF_links.py/PDF_path.py**
* Returns the PDF download link for prior art.
## Output Format
The output file is titled won_patent_contests.json and it is structured as follows:


```
{
  "contests": [
    {
      "contestTitle": "Example Contest Title",
      "patentID": "US1234567",
      "priorArtID": [
        {
          "patent_id": "US1234567",
          "country_code": "US"
        },
        ...
      ],
      "contestLink": "https://patroll.unifiedpatents.com/contests/example"
    },
    ...
  ],
  "totalContests": 100,
  "scrapedPages": 10
}
```
* contestTitle: title of the contest
* patentID: main patent ID for the contest
* priorArtID: list with patent ID and country code for prior art references
* contestLink: link to the contest page


**Note:** This documentation is based off of Zailey's fork, located at https://github.com/Zailey-Lawrence/Patroll-PDF-Web-Scraper. It seems to have the PDF scraper as well as optimizations from Jathin. 





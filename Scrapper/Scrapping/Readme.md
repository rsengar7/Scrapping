Create and Update a .env file in the Directory and change the path of the files:

BLACKLIST_DIR = /home/ritesh/Videos/Jason/Scrapper/Scrapping/company_blacklist.xlsx
WHITELIST_DIR = /home/ritesh/Videos/Jason/Scrapper/Scrapping/company_whitelist.xlsx
LOGS_DIR = /home/ritesh/Videos/Jason/Scrapper/Scrapping/
CHROME_DRIVER = /home/ritesh/Videos/Jason/Scrapper/Scrapping/chromedriver

BLACKLIST_DIR: Path of company_blacklist.xlsx

WHITELIST_DIR: Path of company_whitelist.xlsx

LOGS_DIR : Path of directory where Ecosystem Logs.xlsx, Insight X.xlsx, Renforce.xlsx files are placed.

CHROME_DRIVER: Path of ChromeDriver to Scrap the Data from the website.

----------------------------------------------------------------------------------------------------------------------

To Download the Chrome Driver:
Note: Please check the Installed Google Chrome Version.

https://chromedriver.chromium.org/downloads

----------------------------------------------------------------------------------------------------------------------

Steps to run the Script Successfully:

1 - Install Python3.7 or above

2 - Go to the Scrapping Directory

3 - Install the Virtual Environment:
	For Windows: python -m venv venv
	For Linux: python3 -m venv venv

4 - Activate the Virtual Environment
	For Windows: venv\Scripts\activate
	For Linux: source venv/bin/activate

5 - Install the Required Modules to run the Script using "pip install -r requirements.txt"

6 - Go to the need to be Scrapped Directory (Ex: cd Seek)

7 - Run the Script using (Ex: python seek.py)

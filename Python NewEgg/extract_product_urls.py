import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class NeweggScraper:
    """
    A class used to scrape product names and URLs from Newegg's website.

    Attributes
    ----------
    pages : int
        Number of pages to scrape (default is 20).
    names : list
        List to store product names.
    urls : list
        List to store product URLs.
    driver : webdriver
        Selenium WebDriver instance to interact with the browser.
    """

    def __init__(self, pages=20):
        """
        Initializes the NeweggScraper object with default options for Selenium ChromeDriver.

        :param pages: Number of pages to scrape (default is 20).
        """
        self.pages = pages
        self.names = []  # List to store product names
        self.urls = []  # List to store product URLs
        self.driver = self._init_driver()  # Initialize the Selenium WebDriver

    @staticmethod
    def _init_driver():
        """
        Initializes the Chrome WebDriver with necessary options.

        :return: The Chrome WebDriver object.
        """
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def scrape_data(self):
        """
        Scrapes the product names and URLs from Newegg's website for the specified number of pages.

        Iterates over the given pages, scraping product data from each page and storing it in the object's lists.
        """
        for i in range(1, self.pages + 1):
            url = f"https://www.newegg.com/p/pl?N=101702291&page={i}"
            self.driver.get(url)
            time.sleep(5)  # Wait for the page to load

            try:
                # Locate the product elements using their CSS selector
                data_list = self.driver.find_elements(By.CSS_SELECTOR, 'a[title="View Details"]')
                print(f"Length of items on page {i}: {len(data_list)}")

                for data in data_list:
                    name = data.text  # Extract product name
                    href = data.get_attribute('href')  # Extract product URL
                    print(name, href)

                    # Append data to the lists
                    self.names.append(name)
                    self.urls.append(href)
                    print("*" * 100)
                    time.sleep(1)

            except Exception as e:
                print(f"Error while scraping page {i}: {str(e)}")
            time.sleep(5)

    def save_to_csv(self, filename="urls.csv"):
        """
        Saves the scraped product names and URLs to a CSV file.

        :param filename: The name of the CSV file (default is 'urls.csv').
        """
        df = pd.DataFrame({"Names": self.names, "Urls": self.urls})
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def close_driver(self):
        """
        Closes the Selenium WebDriver once scraping is complete.
        """
        self.driver.quit()


if __name__ == "__main__":
    # Create an instance of the NeweggScraper class
    scraper = NeweggScraper(pages=20)  # Specify how many pages to scrape

    # Scrape the data
    scraper.scrape_data()

    # Save the scraped data to a CSV file
    scraper.save_to_csv("urls.csv")

    # Close the WebDriver
    scraper.close_driver()

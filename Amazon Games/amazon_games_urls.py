import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class AmazonScraper:
    """
    A class to scrape product URLs from Amazon's mobile app section.

    Attributes
    ----------
    driver : webdriver.Chrome
        The Selenium WebDriver instance used to interact with the browser.
    urls : list
        List to store scraped product URLs.

    Methods
    -------
    scrape_urls(page_start=1, page_end=331):
        Scrapes product URLs from the specified page range.
    save_to_csv(filename="amazon_urls.csv"):
        Saves the scraped URLs to a CSV file.
    """

    def __init__(self):
        """
        Initializes the AmazonScraper object by setting up the Chrome WebDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        self.urls = []  # List to store product URLs

    def scrape_urls(self, page_start=1, page_end=331):
        """
        Scrapes product URLs from the specified range of pages.

        :param page_start: Starting page number for scraping (default is 1).
        :param page_end: Ending page number for scraping (default is 331).
        """
        for i in range(page_start, page_end + 1):
            url = f"https://www.amazon.com/s?i=mobile-apps&rh=n%3A9209902011&fs=true&page={i}&qid=1710971883&ref=sr_pg_2"
            self.driver.get(url)
            time.sleep(2)  # Give the page time to load

            for j in range(1, 62):  # Adjust this range depending on the number of items per page
                try:
                    xpath = f"/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[{j}]/div/div/span/div/div/div[1]/span/a"
                    data = self.driver.find_element(by=By.XPATH, value=xpath)
                    product_url = data.get_attribute('href')
                    print(f"Page {i}, Product {j}: {product_url}")
                    self.urls.append(product_url)
                except Exception as e:
                    print(f"Failed to retrieve product on page {i}, position {j}: {str(e)}")

    def save_to_csv(self, filename="amazon_urls.csv"):
        """
        Saves the scraped product URLs to a CSV file.

        :param filename: The name of the output CSV file (default is 'amazon_urls.csv').
        """
        df = pd.DataFrame({"Urls": self.urls})
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def close_driver(self):
        """
        Closes the Selenium WebDriver once scraping is complete.
        """
        self.driver.quit()


if __name__ == "__main__":
    # Instantiate the scraper class
    scraper = AmazonScraper()
    
    # Scrape URLs from Amazon's mobile app section
    scraper.scrape_urls(page_start=1, page_end=331)
    
    # Save the URLs to a CSV file
    scraper.save_to_csv("amazon_urls.csv")
    
    # Close the WebDriver
    scraper.close_driver()

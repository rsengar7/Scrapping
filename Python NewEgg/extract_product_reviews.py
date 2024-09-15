import os
import time
import requests
import pandas as pd
from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NeweggReviewScraper:
    """
    A class to scrape product reviews from Newegg's website using Selenium and API requests.

    Attributes
    ----------
    driver : webdriver
        The Selenium WebDriver instance used to interact with the browser.
    product_url : list
        List to store product URLs.
    Rating : list
        List to store product ratings.
    InDate : list
        List to store review dates.
    Title : list
        List to store review titles.
    DisplayName : list
        List to store reviewer display names.
    EncryCustomerNumber : list
        List to store encrypted customer numbers.
    Comments : list
        List to store customer comments.
    Pros : list
        List to store review pros.
    Cons : list
        List to store review cons.
    failed_urls : list
        List to store URLs that failed during scraping.
    """

    def __init__(self):
        """
        Initializes the scraper with Firefox WebDriver and empty lists to store scraped data.
        """
        # Set up Firefox options
        firefox_options = Options()
        # Uncomment the next line to run headless Firefox if needed
        # firefox_options.add_argument("--headless")

        # Use GeckoDriverManager to handle FirefoxDriver installation
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)

        # Initialize data lists
        self.product_url = []
        self.Rating = []
        self.InDate = []
        self.Title = []
        self.DisplayName = []
        self.EncryCustomerNumber = []
        self.Comments = []
        self.Pros = []
        self.Cons = []
        self.failed_urls = []

    def _get_done_urls(self):
        """
        Reads merged CSV file to retrieve the list of already processed product URLs.

        :return: List of done URLs.
        """
        df1 = pd.read_csv('Data/merged_file.csv')
        done_url = list(set(df1['product_url'].values.tolist()))
        return done_url

    def scrape_reviews(self, csv_file="urls.csv"):
        """
        Scrapes reviews from Newegg for products listed in the provided CSV file.

        :param csv_file: The path to the CSV file containing the product URLs.
        """
        # done_url = self._get_done_urls()
        done_url = []
        df = pd.read_csv(csv_file)
        values = df.values.tolist()

        for pro_row in values:
            if pro_row[2] not in done_url:
                try:
                    self.driver.get(pro_row[2])
                    time.sleep(5)

                    # Click on the 'Reviews' tab
                    self._click_reviews_tab()
                    time.sleep(20)

                    # Process reviews until the next button is disabled
                    self._process_review_pages(pro_row[2])

                    # Capture and process network requests
                    self._capture_reviews(pro_row[2])

                except Exception as ex:
                    print(f"Exception occurred: {ex}")
                    self.failed_urls.append(pro_row[2])

                self._save_reviews_to_csv()

                time.sleep(5)

        self.driver.quit()
        print(self.failed_urls)

    def _click_reviews_tab(self):
        """
        Clicks on the 'Reviews' tab of the product page.
        """
        element = self.driver.find_element(By.XPATH, "//div[text()='Reviews']")
        element.click()

    def _process_review_pages(self, product_url):
        """
        Navigates through the review pages until the 'Next Page' button is disabled.

        :param product_url: URL of the product to scrape reviews for.
        """
        xpath_button = '//button[@title="Next Page"]'
        while True:
            try:
                button = self.driver.find_element(By.XPATH, xpath_button)
                if button.get_attribute('disabled') is not None:
                    print('Button is disabled')
                    break
                else:
                    button.click()
                    print(f'Clicked on the "Next Page" button for {product_url}')
                time.sleep(1)
            except:
                print(f"Failed to navigate pages for URL: {product_url}")
                self.failed_urls.append(product_url)
                break

    def _capture_reviews(self, product_url):
        """
        Captures and processes reviews from the network requests generated by Newegg.

        :param product_url: URL of the product to scrape reviews for.
        """
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        for request in self.driver.requests:
            if str(request.url).startswith("https://www.newegg.com/product/api/ProductReview"):
                print(f"Processing request: {request.url}")
                if request.response:
                    self._process_review_response(request.url, product_url)

    def _process_review_response(self, url, product_url):
        """
        Processes the review response from the API request.

        :param url: The API request URL.
        :param product_url: The URL of the product.
        """
        req = requests.get(url)
        search = req.json()['SearchResult']
        cust_reviews = search['CustomerReviewList']

        for row in cust_reviews:
            self.product_url.append(product_url)

            self.Rating.append(row.get('Rating', ""))
            self.InDate.append(row.get('InDate', ""))
            self.Title.append(row.get('Title', ""))
            self.DisplayName.append(row.get('DisplayName', ""))
            self.EncryCustomerNumber.append(row.get('EncryCustomerNumber', ""))
            self.Comments.append(row.get('Comments', ""))
            self.Pros.append(row.get('Pros', ""))
            self.Cons.append(row.get('Cons', ""))

    def _save_reviews_to_csv(self):
        """
        Saves the scraped reviews to a CSV file.
        """
        data = {
            "product_url": self.product_url,
            "CustomerID": self.EncryCustomerNumber,
            "Rating": self.Rating,
            "InDate": self.InDate,
            "Title": self.Title,
            "DisplayName": self.DisplayName,
            "Comments": self.Comments,
            "Pros": self.Pros,
            "Cons": self.Cons
        }

        df = pd.DataFrame(data)
        file_index = len(os.listdir("Data"))
        df.to_csv(f"Data/api_url{file_index}.csv", index=False)
        print(f"Data saved to Data/api_url{file_index}.csv")


if __name__ == "__main__":
    # Instantiate and run the scraper
    scraper = NeweggReviewScraper()
    scraper.scrape_reviews()
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class AmazonReviewScraper:
    """
    A class to scrape Amazon product reviews.

    Attributes
    ----------
    driver : webdriver.Chrome
        The Selenium WebDriver instance used to interact with the browser.
    data : dict
        Dictionary to store all scraped review data.

    Methods
    -------
    scrape_reviews(urls, upper_limit=14000, lower_limit=15000):
        Scrapes reviews from the list of Amazon product URLs within the given limits.
    _extract_text_by_xpath(xpath):
        Helper function to extract text by XPath.
    _calculate_page_num(rate, review_number):
        Helper function to determine the number of pages based on the review rate and number of reviews.
    save_to_csv(filename="amazon_reviews.csv"):
        Saves the scraped reviews to a CSV file.
    """

    def __init__(self):
        """
        Initializes the AmazonReviewScraper object by setting up the Chrome WebDriver
        and initializing an empty dictionary to store the scraped review data.
        """
        chrome_options = Options()
        # Uncomment the next line to run headless Chrome if needed
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Initialize dictionary to store review data
        self.data = {
            "ASIN": [],
            "User_id": [],
            "Names": [],
            "Review_rating": [],
            "Review_date": [],
            "Rating": [],
            "Review Location": [],
            "Review": [],
            "User_url": []
        }

    def scrape_reviews(self, urls, upper_limit=14000, lower_limit=15000):
        """
        Scrapes reviews from the list of Amazon product URLs within the given limits.

        :param urls: List of Amazon product URLs.
        """
        for index, baseurl in enumerate(urls):

            base_url = baseurl.split("/ref")[0].replace('dp', 'product-reviews')
            all_review_part = "/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&filterByStar={}&pageNumber={}"

            review_url = base_url + all_review_part
            try:
                for number, star in {1: 'one_star', 2: 'two_star', 3: 'three_star', 4: 'four_star', 5: 'five_star'}.items():
                    self._scrape_star_reviews(review_url, star, number)
            except Exception as ex:
                print(f"Error in scraping {baseurl}: {str(ex)}")

    def _scrape_star_reviews(self, review_url, star, star_number):
        """
        Scrapes reviews for the specific star rating.

        :param review_url: The base URL for the reviews.
        :param star: The star rating (e.g., 'one_star', 'two_star').
        :param star_number: The numeric value of the star rating.
        """
        for i in range(1, 11):  # Loop through up to 10 pages of reviews
            url = review_url.format(star, i)
            self.driver.get(url)
            time.sleep(1)

            for j in range(1, 11):  # Scrape up to 10 reviews per page
                self._scrape_individual_review(j, star_number)

    def _scrape_individual_review(self, review_position, star_number):
        """
        Scrapes an individual review from the given position on the page.

        :param review_position: The position of the review on the page.
        :param star_number: The numeric value of the star rating.
        """
        try:
            # Extract user name
            profile_name_xpath = f"/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{review_position}]/div/div/div[1]/a/div[2]/span"
            self.data["Names"].append(self._extract_text_by_xpath(profile_name_xpath))

            # Extract review rating
            rate_xpath = f"/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{review_position}]/div/div/div[2]/a"
            self.data["Review_rating"].append(self._extract_text_by_xpath(rate_xpath))

            # Extract user ID and profile URL
            profile_link_xpath = f"/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{review_position}]/div/div/div[1]/a"
            user_link = self.driver.find_element(by=By.XPATH, value=profile_link_xpath).get_attribute('href')
            self.data["User_url"].append(user_link)
            self.data["User_id"].append(user_link.split("account.")[1].split("/")[0])

            # Extract review date and location
            review_date_xpath = f"/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{review_position}]/div/div/span"
            review_date_text = self._extract_text_by_xpath(review_date_xpath)
            self.data["Review_date"].append(review_date_text.split("on")[1].strip())
            self.data["Review Location"].append(review_date_text.split("on")[0].strip())

            # Extract review text
            review_xpath = f"/html/body/div[1]/div[2]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[{review_position}]/div/div/div[4]/span"
            self.data["Review"].append(self._extract_text_by_xpath(review_xpath))

            # Append ASIN and star rating if review exists
            self.data["ASIN"].append(self.driver.current_url.split("/")[5])
            self.data["Rating"].append(star_number)

        except Exception as ex:
            print(f"Failed to scrape review {review_position}: {str(ex)}")

    def _extract_text_by_xpath(self, xpath):
        """
        Helper function to extract text by an XPath.

        :param xpath: XPath to locate the element.
        :return: Extracted text or an empty string if not found.
        """
        try:
            data = self.driver.find_element(by=By.XPATH, value=xpath).text
            return data
        except:
            return ""

    def save_to_csv(self, filename="amazon_reviews.csv"):
        """
        Saves the scraped reviews to a CSV file.

        :param filename: The name of the output CSV file (default is 'amazon_reviews.csv').
        """
        df = pd.DataFrame(self.data)
        df['Review'] = df['Review'].astype(str)
        df.dropna(subset=['Review'], inplace=True)  # Drop rows with missing reviews
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def close_driver(self):
        """
        Closes the Selenium WebDriver once scraping is complete.
        """
        self.driver.quit()


if __name__ == "__main__":
    # Load URLs from CSV
    df = pd.read_csv("amazon_urls.csv")
    urls = df['Urls'].tolist()

    # Instantiate the scraper
    scraper = AmazonReviewScraper()

    # Scrape reviews from Amazon product URLs
    scraper.scrape_reviews(urls, upper_limit=14000, lower_limit=15000)

    # Save the data to CSV
    scraper.save_to_csv("amazon_reviews_15000.csv")

    # Close the WebDriver
    scraper.close_driver()

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class AmazonGameScraper:
    """
    A class to scrape Amazon game product data and reviews.

    Attributes
    ----------
    driver : webdriver.Chrome
        The Selenium WebDriver instance used to interact with the browser.
    data : dict
        Dictionary to store all scraped game data.

    Methods
    -------
    scrape_product_info(urls):
        Scrapes product information and reviews from the list of Amazon game URLs.
    save_to_csv(filename="amazon_games_info.csv"):
        Saves the scraped data to a CSV file.
    """

    def __init__(self):
        """
        Initializes the AmazonGameScraper object by setting up the Chrome WebDriver
        and initializing an empty dictionary to store the scraped data.
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Initialize dictionary to store scraped data
        self.data = {
            "ASIN": [],
            "Names": [],
            "total_reviews": [],
            "overall_rating": [],
            "game_price": [],
            "game_size": [],
            "developed_by": [],
            "developer_email": [],
            "release_year": [],
            "amazon_listed_date": [],
            "language_supported": [],
            "Ai_Review": [],
            "Ai_tags": [],
            "product_description": [],
            "product_features": [],
            "minimum_operating": [],
            "application_permission": [],
            "reviews_url": []
        }

    def scrape_product_info(self, urls):
        """
        Scrapes product information and reviews from the list of Amazon game URLs.

        :param urls: List of Amazon game product URLs.
        """
        for index, url in enumerate(urls):
            print(f"Scraping product {index + 1}/{len(urls)}")
            base_url = url.split("/ref")[0].replace('dp', 'product-reviews')
            all_review_part = "/ref=cm_cr_arp_d_paging_btm_next_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
            review_url = base_url + all_review_part

            self.driver.get(url)
            time.sleep(1)

            # Extracting data fields
            self.data["ASIN"].append(url.split("/")[5])
            self.data["reviews_url"].append(review_url)
            self.data["Names"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/h1/span/span/span/span[2]"))
            self.data["Ai_Review"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[1]/p[1]"))
            self.data["game_price"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/span[2]/strong"))
            self.data["language_supported"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/span[2]"))
            self.data["Ai_tags"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div", join_lines=True))
            self.data["overall_rating"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[4]/div/div/div[1]/span[1]/div/div/div/div/div/div[2]/div/div[2]/div/span", split_first=True))
            self.data["game_size"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/div[1]/span[2]", split_first=True))
            self.data["minimum_operating"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/div[5]/span[2]", split_first=True))
            self.data["application_permission"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[2]/div[2]/div[12]/ul", split_first=True))
            self.data["developed_by"].append(self._extract_text_by_xpath("/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/span/a", split_first=True))

            # Extracting additional information
            self._extract_additional_info()

    def _extract_text_by_xpath(self, xpath, join_lines=False, split_first=False):
        """
        Helper function to extract text by an XPath.

        :param xpath: XPath to locate the element.
        :param join_lines: Whether to join multiple lines into a single string.
        :param split_first: Whether to split the text and take the first part.
        :return: Extracted text or an empty string if not found.
        """
        try:
            data = self.driver.find_element(by=By.XPATH, value=xpath).text
            if join_lines:
                return ", ".join(data.split("\n"))
            if split_first:
                return data.split(" ")[0]
            return data
        except:
            return ""

    def _extract_additional_info(self):
        """
        Extracts additional information such as release year, first listing date, review count,
        product description, developer email, and product features from the product page.
        """
        release, first_list, review_count, prod_desc, dev_email, prod_features = "", "", "", "", "", ""
        for i in range(1, 15):
            try:
                entry = self.driver.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[1]/div/div[2]/div[2]/div[{i}]").text
                if "Release Date" in entry:
                    release = entry.split(":")[1].strip()
                elif "Date first listed on Amazon" in entry:
                    first_list = entry.split(":")[1].strip()
                elif "Customer reviews" in entry:
                    review_count = entry.split("\n")[1].split(" ")[0]
                elif "Product description" in entry:
                    prod_desc = "\n".join(entry.split("\n")[1:])
                elif "Developer info" in entry:
                    dev_email = entry.split("\n")[1].strip()
                elif "Product features" in entry:
                    prod_features = "\n".join(entry.split("\n")[1:])
            except:
                pass

        self.data["release_year"].append(release if release else "")
        self.data["amazon_listed_date"].append(first_list if first_list else "")
        self.data["total_reviews"].append(review_count if review_count else "")
        self.data["product_description"].append(prod_desc if prod_desc else "")
        self.data["developer_email"].append(dev_email if dev_email else "")
        self.data["product_features"].append(prod_features if prod_features else "")

    def save_to_csv(self, filename="amazon_games_info.csv"):
        """
        Saves the scraped data to a CSV file.

        :param filename: The name of the output CSV file (default is 'amazon_games_info.csv').
        """
        df = pd.DataFrame(self.data)
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
    scraper = AmazonGameScraper()

    # Scrape product information from the URLs
    scraper.scrape_product_info(urls)

    # Save the data to CSV
    scraper.save_to_csv("amazon_games_info.csv")

    # Close the WebDriver
    scraper.close_driver()

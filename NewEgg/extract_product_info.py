import time
import sys
import pandas as pd
import requests as re


class NeweggProductScraper:
    """
    A class to scrape Newegg product information using Newegg API endpoints.

    Attributes
    ----------
    df : DataFrame
        DataFrame containing product URLs to scrape.
    product_url : list
        List of product URLs.
    ai_advantages : list
        List of AI-reviewed advantages for each product.
    ai_disadvantages : list
        List of AI-reviewed disadvantages for each product.
    ai_review : list
        List of AI-reviewed conclusions for each product.
    Brandid : list
        List of brand IDs.
    Brand : list
        List of brand names.
    shippingCountry : list
        List of countries where products are shipped from.
    Price : list
        List of product prices.
    product_title : list
        List of product titles.
    product_description : list
        List of product descriptions.
    product_imdescription : list
        List of product IM descriptions.
    product_BulletDescription : list
        List of product bullet descriptions.
    product_LineDescription : list
        List of product line descriptions.
    product_WebDescription : list
        List of product web descriptions.
    product_ShortTitle : list
        List of product short titles.
    product_SubcategoryId : list
        List of product subcategory IDs.
    product_sub_category : list
        List of product subcategory descriptions.
    product_ItemGroupID : list
        List of product item group IDs.
    product_group_num : list
        List of product group numbers.
    product_total_rating : list
        List of total product ratings.

    Methods
    -------
    get_product_data():
        Fetches product data for all URLs provided in the DataFrame.
    save_to_csv(filename):
        Saves the scraped product data to a CSV file.
    """

    def __init__(self, csv_file):
        """
        Initializes the NeweggProductScraper object by loading the CSV file and setting up empty lists
        to store the scraped data.

        :param csv_file: Path to the CSV file containing the product URLs.
        """
        self.df = pd.read_csv(csv_file)
        self.product_url = []
        self.ai_advantages = []
        self.ai_disadvantages = []
        self.ai_review = []
        self.Brandid = []
        self.Brand = []
        self.shippingCountry = []
        self.Price = []
        self.product_title = []
        self.product_description = []
        self.product_imdescription = []
        self.product_BulletDescription = []
        self.product_LineDescription = []
        self.product_WebDescription = []
        self.product_ShortTitle = []
        self.product_SubcategoryId = []
        self.product_sub_category = []
        self.product_ItemGroupID = []
        self.product_group_num = []
        self.product_total_rating = []

    def get_product_data(self):
        """
        Fetches product data for all URLs provided in the DataFrame and appends it to the respective lists.
        """
        failed_url = []
        values = self.df.values.tolist()

        for row in values:
            
            try:
                self.product_url.append(row[2])

                # Extract product ID from URL
                ids = row[2].split("/")[-1][-8:]
                num = ""
                for index, i in enumerate(ids):
                    if index in [1, 4]:
                        num += i + "-"
                    else:
                        num += i

                # API endpoints for AI review summary and product information
                summary_api = f"https://www.newegg.com/product/api/getAIReviewSummary?ItemNumber={num}"
                product_api = f"https://www.newegg.com/product/api/ProductRealtime?ItemNumber={num}&RecommendItem=&BestSellerItemList=&IsVATPrice=True"

                summary_data = re.get(summary_api).json()
                product_data = re.get(product_api).json()

                # Parse AI Review Data
                if len(summary_data['Data']) != 0:
                    ai_content = summary_data['Data'][0]['AIReviewContent']
                    self.ai_advantages.append(self._parse_ai_data(ai_content, "Advantages"))
                    self.ai_disadvantages.append(self._parse_ai_data(ai_content, "Disadvantages"))
                    self.ai_review.append(ai_content["Conclusion"])
                else:
                    self.ai_advantages.append("")
                    self.ai_disadvantages.append("")
                    self.ai_review.append("")

                # Parse Product Data
                product_desc = product_data.get('MainItem', {}).get('Description', {})
                self.product_description.append(product_desc)

                self.product_title.append(product_desc.get('Title', ""))
                self.product_imdescription.append(product_desc.get('IMDescription', ""))
                self.product_BulletDescription.append(product_desc.get('BulletDescription', ""))
                self.product_LineDescription.append(product_desc.get('LineDescription', ""))
                self.product_WebDescription.append(product_desc.get('WebDescription', ""))
                self.product_ShortTitle.append(product_desc.get('ShortTitle', ""))

                subcategory = product_data.get('MainItem', {}).get('Subcategory', {})
                self.product_SubcategoryId.append(subcategory.get('SubcategoryId', ""))
                self.product_sub_category.append(subcategory.get('SubcategoryDescription', ""))

                self.product_ItemGroupID.append(product_data.get('MainItem', {}).get('ItemGroupID', ""))
                self.product_group_num.append(product_data.get('MainItem', {}).get('Review', {}).get('CombineGroup', ""))
                self.product_total_rating.append(product_data.get('MainItem', {}).get('Review', {}).get('HumanRating', ""))

                manufactory = product_data.get('MainItem', {}).get('ItemManufactory', {})
                self.Brandid.append(manufactory.get('BrandId', ""))
                self.Brand.append(manufactory.get('Manufactory', ""))
                self.shippingCountry.append(product_data.get('MainItem', {}).get('ShipFromCountryName', ""))
                self.Price.append(product_data.get('MainItem', {}).get('OriginalUnitPrice', ""))

                time.sleep(1)
            except Exception as ex:
                print(f"In exception: {ex}")
                failed_url.append(row[2])
                print("Row : ", row)
                # sys.exit()

    def _parse_ai_data(self, ai_content, key):
        """
        Helper method to parse AI data (Advantages or Disadvantages) from the product data.

        :param ai_content: The AI review content from the API response.
        :param key: The key to extract (either 'Advantages' or 'Disadvantages').
        :return: A formatted string containing the parsed data.
        """
        data = ai_content.get(key, None)
        if data:
            return ", \n".join([item[key[:-1]] for item in data])
        return ""

    def save_to_csv(self, filename="product_info.csv"):
        """
        Saves the scraped product data to a CSV file.

        :param filename: The name of the output CSV file (default is 'product_info.csv').
        """
        data = {
            "Url": self.product_url,
            "ai_advantages": self.ai_advantages,
            "ai_disadvantages": self.ai_disadvantages,
            "ai_review": self.ai_review,
            "Brandid": self.Brandid,
            "Brand": self.Brand,
            "shippingCountry": self.shippingCountry,
            "Price": self.Price,
            "product_title": self.product_title,
            "product_description": self.product_description,
            "product_imdescription": self.product_imdescription,
            "product_BulletDescription": self.product_BulletDescription,
            "product_LineDescription": self.product_LineDescription,
            "product_WebDescription": self.product_WebDescription,
            "product_ShortTitle": self.product_ShortTitle,
            "product_SubcategoryId": self.product_SubcategoryId,
            "product_sub_category": self.product_sub_category,
            "product_ItemGroupID": self.product_ItemGroupID,
            "product_group_num": self.product_group_num,
            "product_total_rating": self.product_total_rating
        }

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


if __name__ == "__main__":
    # Instantiate the scraper class
    scraper = NeweggProductScraper("urls.csv")
    
    # Scrape product data
    scraper.get_product_data()
    
    # Save data to CSV file
    scraper.save_to_csv("product_info.csv")

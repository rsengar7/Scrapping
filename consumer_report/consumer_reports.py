from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
# breakpoint()
driver.get("https://www.consumerreports.org/cro/a-to-z-index/products/index.htm")
driver.implicitly_wait(30)
all_categories = driver.find_elements(By.XPATH, "//a[contains(@class, 'products-a-z__results__item')]")
driver.implicitly_wait(30)
category_urls = []
product_name_list = []
for category in all_categories:
    product_name_list.append(category.text)
    category_urls.append(category.get_attribute("href"))
for category_url in range(len(category_urls)):
    # breakpoint()
    driver.get(category_urls[category_url])
    sub_category_urls = []
    sub_categories = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-type-info-container')]/h3/a")
    if len(sub_categories) > 0:
        for sub_category in sub_categories:
            sub_category_urls.append(sub_category.get_attribute("href"))
        names = []
        abouts = []
        features = []
        descriptions = []
        shop_links = []
        for sub_category_url in range(len(sub_category_urls)):
            time.sleep(5)
            driver.get(sub_category_urls[sub_category_url])
            products_list = driver.find_elements(By.XPATH, "//div[contains(@class, 'crux-component-title list__model')]/div/a[@href]")
            product_urls = []
            # breakpoint()
            for product in products_list:
                product_urls.append(product.get_attribute("href"))
            for product_url in range(len(product_urls)):
                driver.implicitly_wait(30)
                print(product_url)
                # breakpoint()
                driver.get(product_urls[product_url])
                driver.implicitly_wait(30)
                name_list = driver.find_elements(By.XPATH, "//span[contains(@id, 'model-name')]")
                description = driver.find_elements(By.XPATH, "//div[contains(@class, 'context context-container shared-crux-text crux-body-copy crux-body-copy--small')]")
                links = driver.find_elements(By.XPATH, "//a[contains(@class, 'shopping-list-item-link')]")
                about = driver.find_elements(By.XPATH, "//div[contains(@class, 'crux-body-copy crux-body-copy--small')]/p")
                feature_key = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-sm-6 features-specs__key')]/span[contains(@class, 'crux-label-style')]")
                feature_value = driver.find_elements(By.XPATH, "//div[contains(@class, 'col-sm-6 features-specs__value')]/span[contains(@class, 'shared-crux-text crux-body-copy crux-body-copy--small')]")
                feature_text = ""
                feature_text_list = [i.text + ":" + j.text + "," for i, j in zip(feature_key, feature_value)]
                feature_text += " ".join(feature_text_list)
                if len(about) > 0:
                    new_text = ""
                    for a in about:
                        new_text += (a.text + " ") 
                    abouts.append(new_text)
                else:
                    abouts.append("Not Available")
                shop_link = ""
                if len(links) > 0:
                    for l in links:
                        shop_link += (l.get_attribute("href") + ",")
                else:
                    shop_link += "Not Available"
                if len(name_list) > 0:
                    for name in name_list:
                        names.append(name.text)
                else:
                    names.append("Not Available")
                features.append(feature_text)
                if len(description) > 0:
                    for d in range(len(description)):
                        descriptions.append(((description[d]).text).replace("\n", " "))
                else:
                    descriptions.append("Not Available")
                shop_links.append(shop_link)

            
            # with open("consumer_reports_new.csv", "a") as file:
            #     for i in range(len(names)):
            #         file.write(names[i] + ";" + descriptions[i] + ";" + abouts[i] + ";" + features[i] + ";" + shop_links[i] + ";" + "\n")
        final_data = {"Product Name": names, "Description": descriptions, "About": abouts, "Features & Specs": features, "Shopping links": shop_links}
        df = pd.DataFrame(final_data) 
        df.to_csv(f"{product_name_list[category_url]}.csv")       
driver.close()   

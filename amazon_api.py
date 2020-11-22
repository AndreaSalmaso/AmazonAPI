from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, datetime, requests, re, json
from bs4 import BeautifulSoup as bs


class AmazonAPI:

    def __init__(self, url):
        self.url = url

    def create_chrome_session(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)

    def get_items_available(self):
        self.create_chrome_session()
        # add product to cart
        self.driver.get(self.url)
        time.sleep(5)
        try:
            self.driver.find_element_by_id("sp-cc-accept").click()
        except:
            pass

        self.driver.find_element_by_id("add-to-cart-button").click() 
        time.sleep(3)

        # go to the cart
        try:
            self.driver.find_element_by_xpath('//span[@id="attach-sidesheet-view-cart-button"]/span/input').click()
        except NoSuchElementException:
            self.driver.get("https://www.amazon.it/gp/cart/view.html/ref=lh_cart")
        time.sleep(3)

        # select the option '10+' in quantity
        select = Select(self.driver.find_element_by_name("quantity"))
        select.select_by_visible_text("10+") # it already places the cursor inside the input box, so you don't need to click in it before deleting the value '1' in there

        # clear entry field and enter 999
        self.driver.find_element_by_name("quantityBox").send_keys(Keys.BACKSPACE)
        self.driver.find_element_by_name("quantityBox").send_keys("999")
        self.driver.find_element_by_name("quantityBox").send_keys(Keys.RETURN)
        time.sleep(3)

        status = None
        alert_xpath = "//div[@class='sc-quantity-update-message a-spacing-top-mini']/div/div/div/span"
        try:
            alert = self.driver.find_element_by_xpath(alert_xpath).text
            status = 'available' if alert.startswith('Questo') else 'not available'
        except:
            items_available = "999+"

        if status == 'available':
            # get number of items available
            for w in alert.split():
                try:
                    items_available = int(w)
                except ValueError:
                    continue
        elif status == 'not available':
            items_available = "NA"

        # print(f"Availability for product {self.url.split('/')[-1]} --> {items_available}")

        # claer the cart
        self.driver.find_element_by_xpath("//input[@value='Rimuovi']").click()
        self.driver.close()

        return items_available

    def get_reviews_ITA(self):
        # check and eventually remove the last '/' if present
        self.url = self.url[:-1] if self.url.endswith("/") else self.url

        asin = self.url.split('/')[-1]
        product_slug = self.url.split('/')[-3]
        pageNumber = 1

        while True:
            reviews_url = f"https://www.amazon.it/{product_slug}/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={pageNumber}"
            r = requests.get(reviews_url)
            content = str(bs(r.text, features="lxml"))

            if re.findall("Da altri Paesi", content):
                # reviews from other countries in the page
                foreign_reviews = len(re.findall("customer_review_foreign", content))
                rev_last_page = 10 - foreign_reviews

                tot_reviews_ITA = 10 * (pageNumber - 1) + rev_last_page
                break
            else:
                pageNumber += 1

        return tot_reviews_ITA
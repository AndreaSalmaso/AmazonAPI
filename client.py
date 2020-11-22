from amazon_api import AmazonAPI
import datetime, os


def method_999(urls):
    # loop through the products
    for asin, url in urls.items():
        amz_scraper = AmazonAPI(url)

        filename = asin + '.txt'
        pcs = amz_scraper.get_items_available()
        date = datetime.datetime.now().strftime("%d-%d-%Y;%H:%M:%S")

        bsr_folder = "Collected_BSRs"
        try:
            os.mkdir(bsr_folder)
        except FileExistsError:
            pass

        path = f"{bsr_folder}/{filename}"

        with open(path, 'a') as f:
            f.write(f"{date};{pcs}\n")

def reviews_ITA_marketplace(url):
    amz_scraper = AmazonAPI(url)
    reviews = amz_scraper.get_reviews_ITA()
    print(f"Total reviews in the Italian marketplace: {reviews}")


urls ={ 
    # "B01KNUQ39S": "https://www.amazon.it/dp/B01KNUQ39S",
    # "B08F7QCT8M": "https://www.amazon.it/gp/product/B08F7QCT8M",
    # "B003LSU2ZG": "https://www.amazon.it/WMF-12-8768-6040-Nutella-Spalmanutella-Inossidabile/dp/B003LSU2ZG",
    "B074Q15PXP": "https://www.amazon.it/BodyBoss-2-0-World-Portable-pacchetto/dp/B074Q15PXP",
}

'''
ATTENTION: the url must end with the ASIN code! If the link you copy and paste ends with a string like 'ref=...', cut that part out
Example: from this link
    'https://www.amazon.it/ACE2ACE-Autopulente-Toelettatura-Domestici-Graffiano/dp/B08881PMQB/ref=zg_bs_pet-supplies_26?_encoding=UTF8&psc=1&refRID=QK3JT0532HSJK3VF2SP7'
you need to remove the part, from the last '/' to the end. You can see the result in the variable assignment below
'''

url = "https://www.amazon.it/ACE2ACE-Autopulente-Toelettatura-Domestici-Graffiano/dp/B08881PMQB/"

# method_999(urls)
reviews_ITA_marketplace(url)
from bs4 import BeautifulSoup
import requests
import json
from PIL import Image
from io import BytesIO
from send_email import email

class product:
    def __init__(self):
        self.url = None
        self.title = None
        self.price = None
        self.image = None
        self.header = {
            "user-agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            'Accept':
                '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }

    def get_product_page(self, url):
        self.url = url
        page = requests.get(url, headers=self.header)
        soup = BeautifulSoup(page.content, 'lxml')
        self.title = self.get_title(soup)
        self.price = self.get_price(soup)
        img_url = self.get_image(soup)
        response = requests.get(img_url)
        self.image = Image.open(BytesIO(response.content))

    @staticmethod
    def get_title(soup):

        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"id": 'productTitle'})

            # Inner NavigableString Object
            title_value = title.string

            # Title as a string value
            title_string = title_value.strip()

        except AttributeError:
            title_string = ""

        return title_string

    # Function to extract Product Price
    @staticmethod
    def get_price(soup):

        try:
            price_whole = soup.find("span", attrs={'class': 'a-price-whole'})
            price_whole = price_whole.get_text()
            price_fraction = soup.find("span", attrs={'class': 'a-price-fraction'})
            price_fraction = price_fraction.get_text()
            price = price_whole+price_fraction
            price = float(price.encode('ascii', 'ignore'))

        except AttributeError:
            price = ""

        return price

    @staticmethod
    def get_image(soup):
        img_div = soup.find(id="imgTagWrapperId")
        img_str = img_div.img.get('data-a-dynamic-image')
        img_str = json.loads(img_str)
        # each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
        num_element = 0
        first_link = list(img_str.keys())[num_element]
        return first_link

    def check_price(self, prod, mail):
        if prod.url != self.url:
            return (None, "The url in to the same as the base product.")
        if not mail.loged_in:
            return (None, "You must login befor try to send mail.")
        if prod.price < self.price:
            text = "*************************************************\n" + \
                   "                   Price Drop                    \n" + \
                   f"The product: {self.title}\n" + \
                   f"The basic price was: {self.price}\n" + \
                   f"The price now is: {prod.price}\n" + \
                   "*************************************************"
            mail.set_text(text)
            mail.send()
            return (True, "")


# url = 'https://www.amazon.com/Joseph-Stainless-Steel-Extendable-Non-Scratch-Drainage/dp/B07YLGKFR9?crid=36RURT0Y47TE2&keywords=B07YLGKFR9&qid=1657626877&smid=ATVPDKIKX0DER&sprefix=b07ylgkfr9%2Caps%2C189&sr=8-3&linkCode=sl1&tag=onoo-20&linkId=5c5f01f89eceba19a530324d1cdb708e&language=en_US&ref_=as_li_ss_tl&th=1'
# # url = 'https://www.amazon.com/-/he/DEWALT-%D7%9E%D7%A9%D7%95%D7%9C%D7%91%D7%AA-%D7%90%D7%9C%D7%97%D7%95%D7%98%D7%99-%D7%A1%D7%95%D7%9C%D7%9C%D7%95%D7%AA-DCK44C2/dp/B082G2MKX8?ref_=Oct_DLandingS_D_bf6e40fe_68'
# pr = product()
# pr.title = "Test Product"
# pr.price = 30
# pr.url = "https://www.amazon.com/Joseph"
# pr_1 = product()
# pr_1.price = 28
# pr_1.url = "https://www.amazon.com/Joseph"
# mail = email('eliransharon@gmail.com')
# psw = ''
# mail.login('gmail', psw)
# pr.check_price(pr_1, mail)

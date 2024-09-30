

'''
class KitabaySpider(scrapy.Spider):
    name = "kitabay"
    start_urls = ["https://kitabay.com/collections/fiction-mystery-crime-thriller"]

    def parse(self, response):
        for book in response.css('div.grid__item'):
            title = book.css('div.grid-product__title a::text').get()
            author = book.css('div.grid-product__vendor::text').get()
            price = book.css('span.money::text').get()

            self.log(f'Found book: {title} by {author} priced at {price}')

            yield {
                'Title': title.strip(),
                'Author': author.strip(),
                'Price': price.strip(),
            }

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

import scrapy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time

class KitabaySpider(scrapy.Spider):
    name = 'kitabay'

    def __init__(self, *args, **kwargs):
        super(KitabaySpider, self).__init__(*args, **kwargs)
        # Initialize the ChromeDriver using webdriver-manager
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def start_requests(self):
        start_url = 'https://kitabay.com/collections/fiction-mystery-crime-thriller'
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        # Use Selenium to open the page
        self.driver.get(response.url)
        time.sleep(3)  # Let the page load completely

        # Get the page source after rendering JavaScript
        selenium_response = Selector(text=self.driver.page_source)

        # Extract book information
        for book in selenium_response.css('div.grid__item'):
            title = book.css('div.grid-product__title a::text').get()
            author = book.css('div.grid-product__vendor::text').get()
            price = book.css('span.money::text').get()

            if title and author and price:
                yield {
                    'Title': title.strip(),
                    'Author': author.strip(),
                    'Price': price.strip(),
                }

        # Check for the next page and navigate
        next_page = selenium_response.css('li.pagination-next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def closed(self, reason):
        # Close the Selenium driver when the spider is done
        self.driver.quit()

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


class KitabaySpider(scrapy.Spider):
    name = "kitabay"
    start_urls = ["https://kitabay.com/collections/fiction-mystery-crime-thriller"]

    def __init__(self, *args, **kwargs):
        super(KitabaySpider, self).__init__(*args, **kwargs)

        # Set up Selenium WebDriver with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Uncomment if you want to run Chrome in headless mode
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # Wait for the page to load

        # Extract book information
        books = self.driver.find_elements("css selector", ".product-card")

        book_data = []

        for book in books:
            title = book.find_element("css selector", ".product-card-title").text
            author = book.find_element("css selector", ".product-card-author").text
            price = book.find_element("css selector", ".product-card-price").text

            book_data.append({
                "Title": title,
                "Author": author,
                "Price": price
            })

        # Write data to CSV
        self.save_to_csv(book_data)
        print(book_data)
    def save_to_csv(self, book_data):
        # Specify the CSV file path
        csv_file_path = "kitabay_books.csv"

        # Writing to CSV
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Author", "Price"])
            writer.writeheader()
            for book in book_data:
                writer.writerow(book)

        self.log(f"Saved {len(book_data)} books to {csv_file_path}")

    def closed(self, reason):
        self.driver.quit()
'''
import scrapy
import csv

class KitabaySpider(scrapy.Spider):
    name = "kitabay"
    start_urls = ["https://kitabay.com/collections/fiction-mystery-crime-thriller"]
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Adding delay between requests to avoid being blocked
    }
    def parse(self, response):
        # Extract book information
        books = response.css('div.collection-main')

        book_data = []

        for book in books:
            title = book.css('div.product__grid__title__wrapper p.product__grid__title::text').get()
            author = book.css('div.product__grid__info.text-left p.author-name::text').get()
            price = book.css('div.product__grid__price.product__grid__price--nowrap span.price.on-sale::text').get()

            # Check if the extracted data is not None
            if title and author and price:
                book_data.append({
                    "Title": title.strip(),
                    "Author": author.strip(),
                    "Price": price.strip()
                })

        # Write data to CSV
        self.save_to_csv(book_data)

    def save_to_csv(self, book_data):
        # Specify the CSV file path
        csv_file_path = "kitabay_books.csv"

        # Writing to CSV
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Author", "Price"])
            writer.writeheader()
            writer.writerows(book_data)

        self.log(f"Saved {len(book_data)} books to {csv_file_path}")

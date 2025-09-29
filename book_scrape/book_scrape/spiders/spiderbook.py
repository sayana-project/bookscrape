import scrapy
from datetime import datetime

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # Suivre chaque lien de livre
        for product in response.css('article.product_pod'):
            link = response.urljoin(product.css('h3 a::attr(href)').get())
            yield response.follow(link, callback=self.parse_book)

        # Pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(response.urljoin(next_page), callback=self.parse)

    def parse_book(self, response):
        def extract_table_value(label):
            return response.xpath(f'//th[text()="{label}"]/following-sibling::td/text()').get()
        
        def convert_note(text):
            note_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            return note_map.get(text, 0)

        def process_field(value, func):
            return func(value)

        # Usage
        note_text = response.css('p.star-rating').attrib['class'].split()[-1]
        note = process_field(note_text, convert_note)


        yield {
            "title": response.css('div.product_main h1::text').get(),
            "genre": response.css('ul.breadcrumb li:nth-child(3) a::text').get(),
            "note": note,
            "stock_number": extract_table_value("Availability").split("(")[-1].split()[0],
            "datetime": datetime.now().isoformat(),
            "upc": extract_table_value("UPC"),
            "product_type": extract_table_value("Product Type"),
            "price_ht": extract_table_value("Price (excl. tax)").replace("£", ""),
            "price_taxed": extract_table_value("Price (incl. tax)").replace("£", ""),
            "review_number": extract_table_value("Number of reviews"),
            "description": response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()
        }

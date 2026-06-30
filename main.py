import json
import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com"]
    
    quotes_data = []
    authors_data = []
    seen_authors = set()

    def parse(self, response):
        for quote in response.css("div.quote"):
            tags = quote.css("div.tags a.tag::text").getall()
            author_name = quote.css("small.author::text").get().strip()
            quote_text = quote.css("span.text::text").get().strip()

            self.quotes_data.append({
                "tags": tags,
                "author": author_name,
                "quote": quote_text
            })

            author_url = quote.css("span a::attr(href)").get()
            if author_url and author_name not in self.seen_authors:
                self.seen_authors.add(author_name)
                yield response.follow(author_url, callback=self.parse_author)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        fullname = response.css("h3.author-title::text").get().strip()
        born_date = response.css("span.author-born-date::text").get().strip()
        born_location = response.css("span.author-born-location::text").get().strip()
        description = response.css("div.author-description::text").get().strip()

        self.authors_data.append({
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        })

    @classmethod
    def close(cls, spider, reason):
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(spider.quotes_data, f, ensure_ascii=False, indent=4)
            
        with open("authors.json", "w", encoding="utf-8") as f:
            json.dump(spider.authors_data, f, ensure_ascii=False, indent=4)
            
        print("\n✨ Скрапінг завершено! Файли quotes.json та authors.json успішно створені.")

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "LOG_LEVEL": "INFO"
    })
    process.crawl(QuotesSpider)
    process.start()
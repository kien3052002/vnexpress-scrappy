import scrapy
from vnexscrapy.items import CategoryItem

class CategorySpider(scrapy.Spider):
    name = 'category_spider'
    start_urls = ['https://vnexpress.net/kinh-doanh']

    def parse(self, response):

        CATEGORY_URL_SELECTOR = '.ul-nav-folder li a::attr(href)'

        # lấy danh sách url các category
        category_urls = response.css(CATEGORY_URL_SELECTOR).extract()

        # vào từng url cụ thể
        for url in category_urls:
            if url and url != 'https://ebox.vnexpress.net/':
                yield response.follow('https://vnexpress.net' + url, self.parse_category)

    def parse_category(self, response):
        CATEGORY_ID_SELECTOR = 'head meta[name=tt_category_id]::attr(content)'
        CATEGORY_TITLE_SELECTOR = 'head meta[name=tt_list_folder_name]::attr(content)'

        # lấy id và title của category
        category_item = CategoryItem()
        category_item['id'] = response.css(CATEGORY_ID_SELECTOR).get()
        category_item['title'] = response.css(CATEGORY_TITLE_SELECTOR).get().split(',')[2]

        yield category_item
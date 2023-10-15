import scrapy
from vnexscrapy.items import NewsItem

class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    start_urls = ['https://vnexpress.net/kinh-doanh']

    def parse(self, response):

        CATEGORY_URL_SELECTOR = '.ul-nav-folder li a::attr(href)'

        # lấy url từng category
        category_urls = response.css(CATEGORY_URL_SELECTOR).extract()

        # truy cập từng category để lấy news
        for url in category_urls:
            if url and url != 'https://ebox.vnexpress.net/':
                yield response.follow('https://vnexpress.net' + url, self.parse_category)

    def parse_category(self, response):
        CATEGORY_ID_SELECTOR = 'head meta[name=tt_category_id]::attr(content)'
        NEWS_SELECTOR = '#automation_TV0 > div > .item-news > .title-news > a::attr(href)'

        # lấy danh sách link các news
        news_links = response.css(NEWS_SELECTOR).extract()

        # lấy category_id của các news trong danh sách vừa lấy
        category_id = response.css(CATEGORY_ID_SELECTOR).get()
        if len(news_links) > 0:

            # truy cập từng link, truyền category_id vừa lấy
            for link in news_links:
                yield response.follow(link, self.parse_news, cb_kwargs={'category_id': category_id})

            # sang trang tiếp theo của cùng category
            # next_page = response.css('a.btn-page.next-page::attr(href)').get()
            # if next_page:
            #     yield response.follow(next_page, self.parse_category)

    def parse_news(self, response, category_id):
        ID_SELECTOR = 'head meta[name=tt_article_id]::attr(content)'
        # CATEGORY_ID_SELECTOR = 'head meta[name=tt_list_folder]::attr(content)'
        TITLE_SELECTOR = 'head title::text'
        AUTHOR_SELECTOR = '.fck_detail p.Normal:last-of-type strong::text, .fck_detail p.author_mail strong::text'
        PUBLISH_DATE_SELECTOR = 'head meta[name=pubdate]::attr(content)'
        LAST_MOD_SELECTOR = 'head meta[name=lastmod]::attr(content)'
        DESCRIPTION_SELECTOR = 'head meta[name=description]::attr(content)'
        CONTENT_SELECTOR = '.container article.fck_detail'
        CONTENT_TEXT_SELECTOR = '.container article.fck_detail *::text'
        KEYWORDS_SELECTOR = 'head meta[name=keywords]::attr(content)'

        news_item = NewsItem ()
        news_item['id'] = response.css(ID_SELECTOR).get()
        news_item['source'] = response.request.url
        news_item['title'] = response.css(TITLE_SELECTOR).get()
        # category_id truyền từ parse_category
        news_item['category_id'] = category_id
        news_item['author'] = response.css(AUTHOR_SELECTOR).get()
        news_item['publish_date'] = response.css(PUBLISH_DATE_SELECTOR).get()
        news_item['last_mod'] = response.css(LAST_MOD_SELECTOR).get()
        news_item['description'] = response.css(DESCRIPTION_SELECTOR).get()
        news_item['content'] = response.css(CONTENT_SELECTOR).get()
        news_item['content_text'] = " ".join(response.css(CONTENT_TEXT_SELECTOR).getall())
        news_item['keywords'] = response.css(KEYWORDS_SELECTOR).get()

        yield news_item

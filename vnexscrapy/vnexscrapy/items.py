from scrapy.item import Item, Field


class NewsItem(Item):
    id = Field()
    source = Field()
    title = Field()
    category_id = Field()
    author = Field()
    publish_date = Field()
    last_mod = Field()
    description = Field()
    content = Field()
    content_text = Field()
    keywords = Field()


class CategoryItem(Item):
    id = Field()
    title = Field()
import psycopg2
from vnexscrapy.config import DB_CONFIG

class DatabasePipeline:

    def __init__(self):
        self.connection = None
        self.cursor = None

        self.create_query_news = """
                        CREATE TABLE IF NOT EXISTS news (
                           id TEXT PRIMARY KEY,
                           source TEXT,
                           title TEXT,
                           category_id TEXT REFERENCES category(id) ON DELETE SET NULL,
                           author TEXT,
                           publish_date TEXT,
                           last_mod TEXT,
                           description TEXT,
                           content TEXT,
                           content_text TEXT,
                           keywords TEXT
                        );
                        """
        self.create_query_category = """
                        CREATE TABLE IF NOT EXISTS category (
                           id TEXT PRIMARY KEY,
                           title TEXT
                        );
                        """

    def open_spider(self, spider):
        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

        self.cursor.execute(self.create_query_category)
        self.cursor.execute(self.create_query_news)

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def process_item(self, item, spider):
        if spider.name == 'category_spider':
            self.insert_category(item)
        elif spider.name == 'news_spider':
            self.insert_news(item)
        return item

    def insert_category(self, category_item):
        insert_query = """INSERT INTO category (id, title) VALUES(%s, %s) ON CONFLICT (id) DO UPDATE SET 
                        title = EXCLUDED.title;"""
        data = (
            category_item['id'],
            category_item['title'],
        )

        self.cursor.execute(insert_query, data)

    def insert_news(self, news_item):
        insert_query = """
                        INSERT INTO news (id, source, title, category_id, author, publish_date, last_mod, description, content, content_text, keywords)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET 
                        source = EXCLUDED.source,
                        title = EXCLUDED.title,
                        category_id = EXCLUDED.category_id,
                        author = EXCLUDED.author,
                        publish_date = EXCLUDED.publish_date,
                        last_mod = EXCLUDED.last_mod,
                        description = EXCLUDED.description,
                        content = EXCLUDED.content,
                        content_text = EXCLUDED.content_text,
                        keywords = EXCLUDED.keywords;
                        """
        data = (
            news_item['id'],
            news_item['source'],
            news_item['title'],
            news_item['category_id'],
            news_item['author'],
            news_item['publish_date'],
            news_item['last_mod'],
            news_item['description'],
            news_item['content'],
            news_item['content_text'],
            news_item['keywords'],
        )

        self.cursor.execute(insert_query, data)

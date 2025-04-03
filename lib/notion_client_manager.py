from config.settings import NotionConfig
from notion_client import Client

def get_notion_client():
    return Client(auth=NotionConfig.NOTION_API_KEY)

# 加载配置
import os
from pathlib import Path
from dotenv import load_dotenv

# 到当前项目的根目录下
BASE_DIR = Path(__file__).parent.parent   
#加载 .env到环境变量
load_dotenv(BASE_DIR / "config" / ".env") 

class NotionConfig:
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    QUERY_DATABASE_ID = os.getenv("QUERY_DATABASE_ID")
    INSERT_DATABASE_ID = os.getenv("INSERT_DATABASE_ID")



class DeepSeekConfig:
    #ai
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    BASE_URL = "https://api.deepseek.com/v1"
    DEFAULT_TIMEOUT = 30
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
    RAW_VOCAB_ID = os.getenv("RAW_VOCAB_ID")
    MASTER_VOCAB_ID = os.getenv("MASTER_VOCAB_ID")
    REVIEW_VOCAB_ID = os.getenv("REVIEW_VOCAB_ID")
    RAW_AUDIO_ID=os.getenv("RAW_AUDIO_ID")
    MASTER_AUDIO_ID=os.getenv("MASTER_AUDIO_ID")
    REVIEW_AUDIO_ID=os.getenv("REVIEW_AUDIO_ID")

class DeepSeekConfig:
    #ai
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    BASE_URL = "https://api.deepseek.com/v1"
    DEFAULT_TIMEOUT = 30

class GithubConfig:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    AUDIO_REPO=os.getenv("AUDIO_REPO")
    PERSON_NAME=os.getenv("PERSON_NAME")
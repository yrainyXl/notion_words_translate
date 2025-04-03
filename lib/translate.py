from .ai_client  import AIClient
from typing import List
import json

# 系统提示词模板（只需定义一次）
SYSTEM_PROMPT = """
你是一个专业的词典助手，请根据用户提供的单词列表，严格按照以下要求返回数据：
1. 用英文解释单词的核心含义（不超过20个单词）
2. 提供国际音标（IPA格式）
3. 给出1个简单例句
4. 列出2个常用近义词 
5. 列出2个常用反义词

输出格式要求：
- 使用JSON格式
- 键名：word, meaning, pronunciation, examples, synonyms, antonyms
- 注意 meaning和examples设计到用引号的都用单引号
- 示例结构：
{
  "result": [
    {
      "word": "apple",
      "meaning": "a round fruit with red or green skin",
      "pronunciation": "/ˈæp.əl/",
      "examples": "I eat an apple every day.",
      "synonyms": "fruit, pome",
      "antonyms": "vegetable, meat"
    }
  ]
}
"""


def translate_words(words: List[str]):
    if not isinstance(words, list):
        raise ValueError("输入必须是单词列表")
    
    if len(words) < 1:
        print("单词列表为空")
        return []
    
    #构建用户信息
    user_prompt={
        "role": "user",
        "content": json.dumps({"words":words},ensure_ascii=False)
    }
    system_prompt={
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    
    aiClient = AIClient()
    data = json.loads(aiClient.request(system_prompt,user_prompt))
    print(f"json: {data}")
    return data['result']
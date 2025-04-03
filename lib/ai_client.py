import requests
from config.settings import DeepSeekConfig
from openai import OpenAI

class AIClient():
    def __init__(self):
        self.client= OpenAI(api_key=DeepSeekConfig.DEEPSEEK_API_KEY,base_url=DeepSeekConfig.BASE_URL)

    def request(self,system_prompt,user_prompt):
        response =  self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[system_prompt,user_prompt],
            stream=False,
            response_format={
                'type': 'json_object'
            }
        )
        return response.choices[0].message.content

from .notion_client_manager import get_notion_client

class NotionBlockClient:
    def __init__(self):
        self.client=get_notion_client()
    def get_block(self,block):
        return self.client.blocks.retrieve(block_id=block.block_id)
    def update_block(self,block):
        response = self.client.blocks.update(
            block_id=block.block_id,
            **block.to_api_body()
        )
        return response

class AudioBlock:
    def __init__(self,block_id,audio_url):
        self.block_id=block_id
        self.audio_url=audio_url
    
    def to_api_body(self):
        return {
            "audio": {  # 注意这里改为audio类型
                "external": {
                    "url": self.audio_url
                }
            }
        }
        
        

class LinkBlock:
    """
    按钮
    url:按钮跳转链接
    text:按钮文字
    """
    def __init__(self,block_id,url,button_text:str='查看'):
        self.block_id=block_id
        self.url=url
        self.button_text=button_text
    def to_api_body(self):
        return {
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": self.button_text,
                        "link": {"url": self.url}
                    },
                    "annotations": {
                        "bold": True,
                        "color": "default",
                        "italic": False,
                        "strikethrough": False,
                        "underline": False
                    }
                }]
            }
        }


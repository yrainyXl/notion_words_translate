# notion操作类，提供查询、创建、更新

from datetime import datetime
from .notion_client_manager import get_notion_client
from urllib.parse import unquote, urlparse

class NotionDataset:
    def __init__(self,database_id):
        self.client=get_notion_client()
        self.database_id=database_id       


    #查询数据库中的页面信息
    def query_page(self,filter_dict=None,sorts_dict=None,limit=None,page_size=100):
        has_more = True
        next_cursor = None
        all_results = []
        # 为空的话，可以筛选titile不为空，all_words_filter= {"property": "WORD", "title": {"is_not_empty": True}}
        if filter_dict is None: filter_dict={}
        if sorts_dict is None: sorts_dict = []

        while has_more :
            #如果有限制返回条件，直接用返回limit条
            if limit is not None: page_size = int(limit)
            #调用接口查询数据
            response = self.client.databases.query(
                database_id=self.database_id,  #数据库id
                page_size=page_size,          #每页数量
                start_cursor=next_cursor,  #分页游标
                filter=filter_dict,   #添加过滤条件
                sorts=sorts_dict #排序条件
            )

            #收集结果，这里给我们返回的是封装好了的 py数据结构对象list、map可以直接获取
            all_results.extend(response["results"])

            #如果限制返回这里直接退出循环
            if limit is not None : break

            #更新分页参数
            has_more = response["has_more"]
            next_cursor = response.get("next_cursor")

            print(f"已获取 {len(all_results)} 条记录")

        return all_results
    #根据属性字段创建新的数据库页面
    def create_page(self,properties):
        formatted_props = self._format_properties(properties)

        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=formatted_props
        )
        return response["id"]

    #更新数据库页面 
    def update_page(self,properties,page_id):
        formatted_props = self._format_properties(properties)

        self.client.pages.update(
            page_id=page_id,
            properties=formatted_props
        )

    #删除页面
    def delete_page(self,page_id):
        self.client.pages.update(
            page_id=page_id,
            archived=True #归档，删除页面
        )

    def _format_properties(self, properties):
        """将用户输入转换为Notion API格式"""
        formatted = {}
        for key, value in properties.items():
            field_type, data = value
            formatted[key] = self._format_field(field_type, data)
        return formatted

    def _format_field(self, field_type, data):
        """字段格式化逻辑"""
        if field_type == "title":
            return {"title": [{"text": {"content": data}}]}
        elif field_type == "rich_text":
            return {"rich_text": [{"text": {"content": data}}]}
        elif field_type == "select":
            return {"select": {"name": data }}
        elif field_type == 'multi_select':
            if isinstance(data,str):
                data = [data]
            return {"multi_select":[{"name":item} for item in data]}
        elif field_type == "date":
            return {"date": {"start": data.isoformat() if isinstance(data, datetime) else data}}
        elif field_type == "checkbox":
            return {"checkbox": bool(data)}
        elif field_type == "number":
            return {"number": float(data)}
        elif field_type == "url":
            return {"url": data}
        elif field_type == "status":
            return {"status": {"name":data} }
        elif field_type in ["file", "attachment"]:
            if isinstance(data, list):
                return {"files": [_file_item(url) for url in data]}
            else:
                return {"files": [_file_item(str(data))]}
        else:
            raise ValueError(f"不支持的字段类型: {field_type}")
def _extract_filename(url: str) -> str:
    """从 URL 提取文件名"""
    parsed = urlparse(unquote(url))
    filename = parsed.path.split("/")[-1]
    return filename or "unnamed_file"

# 处理文件类型
def _file_item(url: str) -> dict:
    return {
        "name": _extract_filename(url),
        "external": {"url": url}
    }
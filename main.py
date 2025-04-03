from lib.notion_database import NotionDataset
from lib.notion_resultes_page import *
from config.settings import *
from lib.properties import Properties
from lib.translate import *
import traceback
def main():
    query_dataset = NotionDataset(NotionConfig.QUERY_DATABASE_ID)
    #测试查询
    filter_condition= {
        "property": "translate",
        "checkbox": {"equals": False}
    }

    # 获取未翻译的words
    pages = query_dataset.query_page(filter_condition)
    for page in pages:
        print(get_title(page,'title'))



    try:
        # 调用翻译todo
        print("调用ai翻译")
        words=[]
        for page in pages:
            words.append(get_title(page,'title'))
        translate_result=translate_words(words)

        #记录到翻译数据库
        insert_dataset = NotionDataset(NotionConfig.INSERT_DATABASE_ID)
        for translate in translate_result:
            property = Properties()
            property.add_title("WORD",translate['word'])
            property.add_rich_text("MEANING",translate['meaning'])
            property.add_rich_text("PRONUNCIATION",translate['pronunciation'])
            property.add_rich_text("EXAPLE SENTENCE",translate['examples'])
            property.add_rich_text("SYNONYMS",translate['synonyms'])
            property.add_rich_text("ANTONYMS",translate['antonyms'])
            page_id = insert_dataset.create_page(property)
            print(f"插入page成功：{page_id}")


        # 更新翻译列表
        fileds = Properties()
        fileds.add_checkbox("translate",True)
        for page in pages:
            query_dataset.update_page(fileds,get_page_id(page))
    except Exception as e:
        print('exception ')
        traceback.print_exc() 

if __name__=='__main__':
    main()
from lib.notion_database import NotionDataset
from lib.notion_resultes_page import *
from config.settings import *
from lib.properties import Properties
from lib.translate import *
import traceback
def main():
    raw_vocab = NotionDataset(NotionConfig.RAW_VOCAB_ID)
    #测试查询
    filter_condition= {
        "property": "translate",
        "checkbox": {"equals": False}
    }

    # 获取未翻译的words
    pages = raw_vocab.query_page(filter_condition)
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
        master_vocab = NotionDataset(NotionConfig.MASTER_VOCAB_ID)
        for translate in translate_result:
            property = Properties()
            property.add_title("WORD",translate['word'])
            property.add_rich_text("MEANING",translate['meaning'])
            property.add_rich_text("PRONUNCIATION",translate['pronunciation'])
            property.add_rich_text("EXAPLE SENTENCE",translate['examples'])
            property.add_rich_text("SYNONYMS",translate['synonyms'])
            property.add_rich_text("ANTONYMS",translate['antonyms'])
            property.add_number("Number of reviews",1)
            property.add_status("Status","Not Learned")
            page_id = master_vocab.create_page(property)
            print(f"插入page成功：{page_id}")


        # 更新翻译列表
        fileds = Properties()
        fileds.add_checkbox("translate",True)
        for page in pages:
            raw_vocab.update_page(fileds,get_page_id(page))
    except Exception as e:
        print('exception ')
        traceback.print_exc() 

    #同步需要复习的单词
    get_lowest_review_words()
    


#从主词汇数据库里面，获取复习次数最少的10个
def get_lowest_review_words():
    master_vocab = NotionDataset(NotionConfig.MASTER_VOCAB_ID)
    review_size=10

    #1、查询复习次数大于15次的标记为完成
    finish_words_filter={
        "and":[
            {
                "property":"Number of reviews",
                    "number":{
                    "greater_than":14
                }
            },
            {
                "property":"Status",
                "status":{
                    "does_not_equal":"Learned"
                }
            }
        ]
        
    }
    finish_pages=master_vocab.query_page(finish_words_filter)
    for page in finish_pages:
        print(f"finish words: {get_title(page,'WORD')}")
        #更新状态
        update_words_status_and_review_times(
            master_vocab,
            page,
            "Learned",
            "Status",
            int(get_number(page,"Number of reviews")),
            "Number of reviews"
        )

    #2、查询需要复习的单词
    sorts=[
        {
            "property":"Number of reviews",
            "direction":"ascending"  #升序排序
         }
    ]
    need_review_words_filter={
        "or":[
            {
                "property":"Status",
                "status":{
                    "equals":"Not Learned"
                }
             },
             {
                "property":"Status",
                "status":{
                    "equals":"Learning"
                }
             }
        ]
    }
    need_review_pages = master_vocab.query_page(need_review_words_filter,sorts,review_size)

    #3、更新状态和复习次数
    for page in need_review_pages:
        print(get_title(page,'WORD'))
        update_words_status_and_review_times(
            master_vocab,
            page,
            "Learning",
            "Status",
            int(get_number(page,"Number of reviews"))+1,
            "Number of reviews"
        )

    #4、清除复习单词库
    review_vocab = NotionDataset(NotionConfig.REVIEW_VOCAB_ID)
    all_words_filter= {"property": "WORD", "title": {"is_not_empty": True}}
    review_pages=review_vocab.query_page(all_words_filter)
    for page in review_pages:
        print(f"delete page: {get_title(page,'WORD')}")
        review_vocab.delete_page(get_page_id(page))

    #5、将本次记忆单词更新到复习库
    for page in need_review_pages:
        property = Properties()
        property.add_title("WORD",get_title(page,"WORD"))
        property.add_rich_text("MEANING",get_rich_text(page,"MEANING"))
        property.add_rich_text("PRONUNCIATION",get_rich_text(page,"PRONUNCIATION"))
        property.add_rich_text("EXAPLE SENTENCE",get_rich_text(page,"EXAPLE SENTENCE"))
        property.add_rich_text("SYNONYMS",get_rich_text(page,"SYNONYMS"))
        property.add_rich_text("ANTONYMS",get_rich_text(page,"ANTONYMS"))
        property.add_number("Number of reviews",get_number(page,"Number of reviews"))
        property.add_status("Status",get_status(page,"Status"))
        page_id = review_vocab.create_page(property)
        print(f"插入page成功：{page_id}")

def update_words_status_and_review_times(vocab,page,status,status_name,review_times,review_name):
    status_property = Properties()
    status_property.add_status(status_name,status)
    status_property.add_number(review_name,review_times)
    vocab.update_page(status_property,get_page_id(page))



if __name__=='__main__':
    main()
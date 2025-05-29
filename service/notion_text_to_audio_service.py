from lib.notion_audio import generate_audio,upload_to_github
from lib.notion_block import *
from config.settings import *
from lib.notion_database import NotionDataset
from lib.properties import Properties
from lib.translate import *
import traceback,time
from lib.notion_resultes_page import *



"""
1、读取句子库中未转换的句子
2、转换为音频
3、上传到github
4、存储音频地址到notion中
5、更新句子库中的是否以转换
6、筛选句子推送到音频复习库
"""

base_path = ".\\tmp"
review_size=10

def text_to_audio():
    master_audio = NotionDataset(NotionConfig.MASTER_AUDIO_ID)
    raw_audio = NotionDataset(NotionConfig.RAW_AUDIO_ID)
    review_audio = NotionDataset(NotionConfig.REVIEW_AUDIO_ID)

    try:
        # 1、读取句子库中未转换的句子
        filter_condition = {
            "property": "to_audio",
            "checkbox": {"equals":False}
        }
        pages = raw_audio.query_page(filter_condition)

        # 2、to_audio
        index = 1
        for pages_item in pages:
            sentence = get_title(pages_item,'sentence')
            page_id = get_page_id(pages_item)
            print(f"{index} : {sentence}\n")
            index=index+1
            
            file_name= generate_unique_filename()
            local_output_dir=f"{base_path}{os.sep}{file_name}"
            generate_audio(sentence,local_output_dir)

            #3、push to github
            res_url = upload_to_github(local_output_dir)
            print(f"上传github成功，访问地址：{res_url}")

            
            #4、存储音频地址到notion中
            print(f"master_audio: {NotionConfig.MASTER_AUDIO_ID}")
            fields = Properties()
            fields.add_title('audio','audio')
            fields.add_rich_text('sentence',sentence)
            fields.add_number('Number of reviews',1)
            fields.add_file('media',res_url)
            master_audio.create_page(fields)
            print(f'记录音频库成功，{sentence}')

            #5、更新句子库为已转换
            update_properties = Properties()
            update_properties.add_checkbox('to_audio',True)
            raw_audio.update_page(update_properties,page_id)
            print(f"标记句子为已转换 : {sentence}")


        #6、推送到review，推送之前清空review
        all_words_filter= {"property": "index", "title": {"is_not_empty": True}}
        delete_pages = review_audio.query_page(all_words_filter)
        for page in delete_pages:
            review_audio.delete_page(get_page_id(page))

        print("\n清空review_audio库成功\n")

        #查询需要复习的单词
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
        need_review_pages = master_audio.query_page(need_review_words_filter,sorts,review_size)
        review_index=len(need_review_pages)
        for page in need_review_pages:
            sentence = get_rich_text(page,'sentence')
            numbers = get_number(page,'Number of reviews')
            properties = Properties()
            properties.add_title('index',str(review_index))
            properties.add_file('media',get_file_path(page,'media'))
            properties.add_rich_text("sentence",sentence)
            properties.add_number('Number of reviews',numbers)
            review_audio.create_page(properties)
            review_index=review_index-1
            print(f"插入review_pag成功: {sentence}")

            #更新master_audio中复习次数和状态
            update_pro = Properties()
            update_pro.add_status('Status','Learning')
            update_pro.add_number('Number of reviews',numbers + 1 if numbers is not None else 1)
            master_audio.update_page(update_pro,get_page_id(page))

        print('\n更新master状态成功')


        
    except Exception as e:
        traceback.print_exc() 


def generate_unique_filename():
    # 使用时间戳做为文件名
    timestamp = str(int(time.time()))
    filename = f"audio_{timestamp}.mp3"
    return filename
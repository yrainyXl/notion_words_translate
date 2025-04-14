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
5、筛选句子推送到音频复习库
"""

base_path = ".\\tmp"

def text_to_audio():
    try:
        # 1、
        raw_audio = NotionDataset(NotionConfig.RAW_AUDIO_ID)
        filter_condition = {
            "property": "to_audio",
            "checkbox": {"equals":False}
        }
        pages = raw_audio.query_page(filter_condition)

        # 2、to_audio
        index = 1
        for pages_item in pages:
            sentence = get_title(pages_item,'sentence')
            print(f"{index} : {sentence}")
            
            file_name= generate_unique_filename()
            local_output_dir=f"{base_path}{os.sep}{file_name}"
            generate_audio(sentence,local_output_dir)


            #push to github
            # upload_to_github(local_output_dir,)

        
    except Exception as e:
        traceback.print_exc() 









    # text = "Hello world! · I don't want the world to see me"
    # base_path = ".\\tmp"
    # file_name = generate_unique_filename("audio")
    # output_path = f"{base_path}\\{file_name}"
    # generate_audio(text, output_path)
    # print(f"音频文件已保存到{output_path}")

    # audio_github_url= upload_to_github(output_path,"yrainyXl/notion-audio-storage")
    # # audio_github_url = "https://yrainyXl.github.io/notion-audio-storage/audios/audio_1744528225.mp3"
    # print(f"音频文件已上传到GitHub仓库，链接为{audio_github_url}")


    # # 更新audio notion块
    # audio_block_id = "1d4a5d34222080f087aef6a9d3914803"
    # res = NotionBlockClient().update_block(AudioBlock(audio_block_id,audio_github_url))
    # print(res)

    # # 更新link notion块
    # paragraph_block_id = "1d4a5d342220807ea5ead1cd78027fac" 
    # audio_db_id='https://www.notion.so/1d4a5d34222080d19317c11b0f617967'
    # res = NotionBlockClient().update_block(LinkBlock(paragraph_block_id,audio_db_id))
    # print(res)



def generate_unique_filename():
    # 使用时间戳做为文件名
    timestamp = str(int(time.time()))
    filename = f"audio_{timestamp}.mp3"
    return filename
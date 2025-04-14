from service.notion_audio import generate_audio,upload_to_github,generate_unique_filename
from lib.notion_block import *

if __name__ == "__main__":
    text = "Hello world! · I don't want the world to see me"
    base_path = ".\\tmp"
    file_name = generate_unique_filename("audio")
    output_path = f"{base_path}\\{file_name}"
    generate_audio(text, output_path)
    print(f"音频文件已保存到{output_path}")

    audio_github_url= upload_to_github(output_path,"yrainyXl/notion-audio-storage")
    # audio_github_url = "https://yrainyXl.github.io/notion-audio-storage/audios/audio_1744528225.mp3"
    print(f"音频文件已上传到GitHub仓库，链接为{audio_github_url}")


    # 更新audio notion块
    audio_block_id = "1d4a5d34222080f087aef6a9d3914803"
    res = NotionBlockClient().update_block(AudioBlock(audio_block_id,audio_github_url))
    print(res)

    # 更新link notion块
    paragraph_block_id = "1d4a5d342220807ea5ead1cd78027fac" 
    audio_db_id='https://www.notion.so/1d4a5d34222080d19317c11b0f617967'
    res = NotionBlockClient().update_block(LinkBlock(paragraph_block_id,audio_db_id))
    print(res)



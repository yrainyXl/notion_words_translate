from service.notion_text_to_audio_service import text_to_audio
from service.notion_translate_words_service import translate
def main():
    # # 1、翻译单词
    translate()
    # 2、转换音频
    text_to_audio()

if __name__=='__main__':
    main()
获取notion中单词数据库，调用deepseek的ai接口翻译后，写入notion数据库中

test.py 获取句子，调用gtts的接口转换成语言，下载到本地，然后上传到github，更新语言链接到notion，定期推送复习到notinn中

依赖：

pip install gTTS

pip install openai notion-client requests python-dotenv

notion中涉及到的几个数据库

1、单词收集数据库，会在每日任务中创建副本

2、单词库，收集每日单词进行翻译后记录到单词库

3、复习库，每日从单词库中筛选固定个数单词，覆盖到复习库

4、句子库，会在每日任务中创建副本，每日定时将句子转换成音频，上传到github，然后记录链接到句子库

5、音频推送复习库，筛选句子推送到复习库中

from gtts import gTTS
import os
import requests
import base64
import time
from config.settings import GithubConfig


def generate_audio(text, output_path):
    tts = gTTS(text=text, lang='en', slow=False,tld='co.uk')
    tts.save(output_path)
    return output_path

def upload_to_github(file_path,branch="main"):
    target_dir="docs/audios"
    file_name=os.path.basename(file_path)
    api_url = f"https://api.github.com/repos/{GithubConfig.PERSON_NAME}/{GithubConfig.AUDIO_REPO}/contents/{target_dir}/{file_name}"
    print(f"api_url: {api_url}")

    with open(file_path, "rb") as f:
        content = f.read()
        encoded_content = base64.b64encode(content).decode("utf-8")
    

    response = requests.put(
        api_url,
        headers={
            "Authorization": f"Bearer {GithubConfig.GITHUB_TOKEN}",
            "Content-Type": "application/vnd.github.v3+json",
        },
        json={
            "message": "Upload audio file",
            "content": encoded_content,
            "branch": branch,
        }
    )
    if response.status_code == 201:
        print(f"文件上传成功: {response.json()['content']['download_url']}")
        return f"https://{GithubConfig.PERSON_NAME}.github.io/{GithubConfig.AUDIO_REPO}/audios/{os.path.basename(file_path)}"
    else:
        raise Exception(f"上传失败: {response.json()['message']}")



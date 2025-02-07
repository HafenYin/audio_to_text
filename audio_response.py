import requests


def baidu_audio_response(audio_data, config):
    """
    百度语音识别API
    """
    response = requests.post(
        url=config['baidu_api']['ASR_URL'],
        headers={'Content-Type': 'audio/wav; rate=16000',},
        params={
            'cuid': 'your_cuid',  # 用户唯一标识
            'token': config['baidu_api']['ACCESS_TOKEN'],  # 使用配置中的 access_token
            'dev_pid': 1537
        },
        data=audio_data)

    return response.json()


def graq_audio_response(wav_data, config):
    """
    Groq语音识别API
    """
    response = requests.post(
                url=config['graq_api']['ENDPOINT_URL'],
                headers={
                    "Authorization": f"Bearer {config['graq_api']['API_KEY']}"
                },
                files={'file': ('audio.wav', wav_data, 'audio/wav')},
                data={
                    'model': 'whisper-large-v3',
                    'language': 'zh',
                }
            )

    return response.json()

if __name__ == '__main__':
    print("hello")
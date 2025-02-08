import requests


def baidu_audio_response(audio_data, config):
    """
    百度语音识别API
    """
    response = requests.post(
        url=config['baidu_api']['server_url'],
        headers={'Content-Type': 'audio/wav; rate=16000',},
        params={
            'cuid': 'your_cuid',  # 用户唯一标识
            'token': config['baidu_api']['access_token'],  # 使用配置中的 access_token
            'dev_pid': 1537
        },
        data=audio_data)

    return response


def graq_audio_response(wav_data, config):
    """
    Groq语音识别API
    """
    response = requests.post(
                url=config['graq_api']['server_url'],
                headers={
                    "Authorization": f"Bearer {config['graq_api']['api_key']}"
                },
                files={'file': ('audio.wav', wav_data, 'audio/wav')},
                data={
                    'model': 'whisper-large-v3',
                    'language': 'zh',
                    'prompt': '除其他语言和数字、符号外，只要是中文都用简体中文输出'
                }
            )

    return response


def aliyun_audio_response(audio_data, config):
    """
    阿里云语音识别API
    """
    params = {
        'appkey': config['aliyun_api']['app_key'],
        'format': 'pcm',
        'sample_rate': 16000,
        'enable_punctuation_prediction': 'true',
        'enable_inverse_text_normalization': 'true'
    }

    response = requests.post(
        url=config['aliyun_api']['server_url'],
        headers={
            'X-NLS-Token': config['aliyun_api']['access_token'],
            'Content-Type': 'application/octet-stream'
        },
        params=params,
        data=audio_data
    )

    return response


if __name__ == '__main__':
    print("hello")
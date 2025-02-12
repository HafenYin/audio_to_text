import requests
import time
import base64
import hashlib
import hmac
import uuid
from urllib.parse import quote


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
    阿里云语音识别API（整点/半点刷新）
    """    
    # 生成Assess token请求参数
    params = {
        'AccessKeyId': config['aliyun_api']['access_key_id'],
        'Action': 'CreateToken',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid4()),
        'SignatureVersion': '1.0',
        'Timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        'Version': '2019-02-28',
        'Format': 'JSON'
    }

    # 生成签名
    sorted_params = sorted(params.items())
    query_string = '&'.join([f'{k}={quote(str(v), safe="")}' for k, v in sorted_params])
    string_to_sign = f'GET&%2F&{quote(query_string, safe="")}'
    
    signature = hmac.new(
        f"{config['aliyun_api']['access_key_secret']}&".encode(),
        string_to_sign.encode(),
        hashlib.sha1
    ).digest()
    signature = quote(base64.b64encode(signature).decode())

    # 获取新的access token
    url = f"http://nls-meta.cn-shanghai.aliyuncs.com/?Signature={signature}&{query_string}"
    response = requests.get(url)
    access_token = response.json()['Token']['Id']


    # 发送请求
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
            'X-NLS-Token': access_token,
            'Content-Type': 'application/octet-stream'
        },
        params=params,
        data=audio_data
    )

    return response


if __name__ == '__main__':
    print("hello")
    
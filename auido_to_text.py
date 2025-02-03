from flask import Flask, jsonify
import pyaudio
import requests
import threading
import time
import json
import os

app = Flask(__name__)


# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 根据当前路径，获取路径下的依赖文件路径
file_path = os.path.join(script_dir, 'serve_config.json')
with open(file_path) as file:
    config = json.load(file)


# 全局变量
audio = pyaudio.PyAudio()
stream = None
frames = []
is_recording = False

# 录音线程
def record_audio():
    global stream, frames, is_recording
    stream = audio.open(format=eval(config['recording']['FORMAT']), # 16位深度
                        channels=config['recording']['CHANNELS'], # 单声道
                        rate=config['recording']['RATE'], # 采样率
                        input=True,
                        frames_per_buffer=config['recording']['CHUNK']) # 每个缓冲区的帧数
    frames = []
    is_recording = True
    print("录音开始...")
    while is_recording:
        data = stream.read(config['recording']['CHUNK'])
        frames.append(data)
    print("录音结束")


# 开始录音路由
@app.route('/start_recording', methods=['POST'])
def start_recording():
    global is_recording
    if not is_recording:
        threading.Thread(target=record_audio).start()
        return jsonify({"message": "录音已开始"})
    else:
        return jsonify({"message": "录音已在进行中"})


# 结束录音并上传数据路由
@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global is_recording, stream, frames
    if is_recording:
        is_recording = False
        # time.sleep(0)  # 等待录音线程结束
        stream.stop_stream()
        stream.close()

        # 将录音数据转换为二进制格式
        audio_data = b''.join(frames)

        # 使用已有的 access_token 直接进行 API 请求
        headers = {
            'Content-Type': 'audio/wav; rate=16000',
        }

        params = {
            'cuid': 'your_cuid',  # 用户唯一标识
            'token': config['baidu_api']['ACCESS_TOKEN'],  # 使用配置中的 access_token
            'dev_pid': 1537
        }

        response = requests.post(url=config['baidu_api']['ASR_URL'],
                                 headers=headers,
                                 params=params,
                                 data=audio_data)

        return jsonify({"response": response.json()})
    else:
        return jsonify({"message": "没有正在进行的录音"})
    

if __name__ == '__main__':
    app.run(debug=True)

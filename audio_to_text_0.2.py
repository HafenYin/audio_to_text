from flask import Flask, jsonify
import pyaudio
import threading
import struct
import json
import sys
import os

app = Flask(__name__)

# 获取配置信息（保留其他配置）
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'serve_config.json')
with open(file_path) as file:
    config = json.load(file)

stream = None
frames = []
is_recording = False


def generate_wav_header(data_length, channels, sample_rate, bit_depth):
    """生成WAV文件头"""
    riff_chunk_size = 36 + data_length
    fmt_chunk_size = 16  # PCM格式的fmt块固定长度
    
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        riff_chunk_size,
        b'WAVE',
        b'fmt ',
        fmt_chunk_size,
        1,  # PCM格式
        channels,
        sample_rate,
        sample_rate * channels * (bit_depth // 8),  # 字节率
        channels * (bit_depth // 8),  # 块对齐
        bit_depth,
        b'data',
        data_length
    )
    return header

def record_audio():
    global stream, frames, is_recording

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    frames = []
    is_recording = True
    print("录音开始...")
    while is_recording:
        data = stream.read(1024)
        frames.append(data)
    print("录音结束")
    

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global is_recording

    if is_recording:
        return jsonify({"response": "录音已在进行中"})
    else:
        threading.Thread(target=record_audio).start()
        return jsonify({"response": "录音已开始"})


@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global is_recording, stream, frames

    if is_recording:
        # 停止录音流程
        is_recording = False
        stream.stop_stream()
        stream.close()

        # 拼接原始音频数据
        audio_data = b''.join(frames)
        # 生成WAV头
        wav_header = generate_wav_header(
            data_length=len(audio_data),
            channels=1,
            sample_rate=16000,
            bit_depth=16
        )
        # 构造完整WAV数据
        wav_data = wav_header + audio_data

        # 自动添加 main.py 所在目录到 sys.path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from audio_response import baidu_audio_response, aliyun_audio_response

        # 选择API并调用
        if config['selectedApi'] == 'aliyun_api':
            response = aliyun_audio_response(wav_data, config)
            result = response.json().get('result', '未识别到可用音频')
        elif config['selectedApi'] == 'baidu_api':
            response = baidu_audio_response(wav_data, config)
            result = response.json().get('result', '未识别到可用音频')
        else:
            print("serve_config.json未填写当前API")

        print(response.json())

        return jsonify({"response": response.json(), "result": result, "status": response.status_code})
    
    else:
        # 没有录音时的返回
        return jsonify({"response": "没有正在进行的录音"})


if __name__ == '__main__':
    app.run(debug=True)
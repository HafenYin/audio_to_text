from flask import Flask, jsonify
import pyaudio
import requests
import threading
import struct
import json
import os

app = Flask(__name__)

# 获取配置信息
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
        format=eval(config['recording']['FORMAT']),
        channels=config['recording']['CHANNELS'],
        rate=config['recording']['RATE'],
        input=True,
        frames_per_buffer=config['recording']['CHUNK']
    )
    frames = []
    is_recording = True
    print("录音开始...")
    while is_recording:
        data = stream.read(config['recording']['CHUNK'])
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
            channels=config['recording']['CHANNELS'],
            sample_rate=config['recording']['RATE'],
            bit_depth=16
        )
        
        # 构造完整WAV数据
        wav_data = wav_header + audio_data

        # 自动添加 main.py 所在目录到 sys.path
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from audio_response import graq_audio_response, baidu_audio_response
        # 使用graq_audio_response
        response = graq_audio_response(wav_data, config)
        # response = baidu_audio_response(wav_data, config)
        print(response)

        return jsonify({"response": response})
    
    else:
        # 没有录音时的返回
        return jsonify({"response": "没有正在进行的录音"})


if __name__ == '__main__':
    app.run(debug=True)
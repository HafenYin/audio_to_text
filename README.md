### 录音转文本


- 本项目基于flask路由能力，通过对start_recording和stop_recording路由的POST访问，实现启动录音和结束录音并转录成文本的功能
- 项目依赖的python第三方库：pyaudio、flask，请自行完善依赖（任何不懂，复制给AI）
- 本项目的配置文件需要自行修改，请打开serve_config.json修改ACCESS_TOKEN，参考资料：https://console.bce.baidu.com/ai-engine/old/#/ai/speech/app/list
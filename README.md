### 录音转文本


- 本项目基于flask路由能力，通过对start_recording和stop_recording路由的POST访问，实现启动录音和结束录音并转录成文本的功能
- 项目依赖的python第三方库：pyaudio、flask，请自行完善依赖（任何不懂，复制给AI）
- 本项目的配置文件需要自行修改，请打开serve_config.json修改ACCESS_TOKEN（暂时只需要修改一次），参考资料：https://console.bce.baidu.com/ai-engine/old/#/ai/speech/app/list
- 本项目同时基于quicker调用http服务的能力
- 本项目在windows上使用时，建议使用PM2进行后台留存处理：[使用PM2实现python flask后台保活、进程管理](https://segmentfault.com/a/1190000046064133)
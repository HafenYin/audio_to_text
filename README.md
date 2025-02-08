### 录音转文本


- 本项目基于flask路由能力，通过对start_recording和stop_recording路由的POST访问，实现启动录音和结束录音并转录成文本的功能
- 项目依赖的python第三方库：pyaudio、flask，请自行完善依赖（任何不懂，复制给AI）
- 本项目同时基于quicker调用http服务的能力
- 本项目在windows上使用时，建议使用PM2进行后台留存处理：[使用PM2实现python flask后台保活、进程管理](https://segmentfault.com/a/1190000046064133)

### api填写介绍
本项目依赖的api填写在serve_config.json文件中，请自行填写

- [阿里云api填写参考资料](https://help.aliyun.com/zh/isi/developer-reference/restful-api-2?spm=a2c4g.11186623.help-menu-30413.d_3_0_0_1.70c56b9b1eZZWd)：查看文章中“前提条件”一节，根据里面的指引，获取Appkey和Access Token，并填入本项目中的serve_config.json文件的相应位置即可
- [百度语音api填写参考资料](https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu)：查看文章中“access_token鉴权机制”一节，根据里面的指引，获取Access Token，并填入本项目中的serve_config.json文件的相应位置即可
- [graq语言api填写参考资料](https://console.groq.com/keys)：获取参考链接中的apikey，并填入本项目中的serve_config.json文件的相应位置即可

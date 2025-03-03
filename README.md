<h1 align="center">DailyInfo</h1>
<h6 align="center">基于企业微信的每日图文推送</h6>

**❗︎︎本项目采用[GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)协议，仅供个人学习和使用，未授权任何商业化、付费行为，包括但不限于源代码、教程、代建、代搭。严禁一切不尊重开发者、不尊重版权的行为，违者后果自负。使用本项目源码/教程即视为同意本条款，本人保留对一切违反本条款行为诉诸法律的权利。**

**❗︎2022年9月3日已更新，[更新日志](./docs/update.md)**

**❗︎[点此前往部署教程获取方式](https://www.kdocs.cn/l/csn6eqw93kQZ)** **或扫描文末二维码，关注微信公众号 “勃然大陆” ，回复 “教程” 即可**

**❗︎目前只支持云服务器或腾讯云函数等IP固定的平台部署**

**❗︎已知Bug：云服务器部署用户会因 ‘ 等字符的转义处理错误导致之后的内容无法显示**

## Introduction

- Bing必应 每日壁纸
- 金山词霸 每日一句
- ONE·一个 一图一句
- 和风天气 多地区天气预报
- 农历 / 公历多日期纪念日 / 单日提醒
- 可选的单图文 / 多图文推送模式
- 自带图文展示页
- 内容高度自定义 详细的拓展模板

## Preview

- 单图文

<img src="https://b2.kuibu.net/file/imgdisk/2022/08/30/WPS1.png"  />

- 多图文

![](https://b2.kuibu.net/file/imgdisk/2022/08/30/WPS2.png)

![](https://b2.kuibu.net/file/imgdisk/2022/08/30/WPS3.png)

## Preparation

|  环境变量  |                             含义                             |  备注  |
| :--------: | :----------------------------------------------------------: | :----: |
|   corpid   |                        企业微信企业ID                        |  必填  |
| corpsecret |                      企业微信应用Secret                      |  必填  |
|  agentid   |                     企业微信应用AgentId                      |  必填  |
|  qweather  |                       和风天气应用Key                        | 非必填 |
|    city    | 天气预报地址<br />格式：省/市-市/区/县，多地区以&&间隔<br />如：成都-双流&&江苏-江宁 | 非必填 |
| beginname  | 单日项目名称<br />只有某一年有的日子，多日期以&&分隔<br />如：跟XX在一起&&某某某出生 | 非必填 |
|  beginday  | 单日日期，公历格式20XX-XX-XX<br />农历年份前加n，多日期以&&分隔，注意与名称对应<br />如：n2020-08-11&&2021-08-26 | 非必填 |
| targetname | 纪念日名称<br />每年都有的日子，多日期以&&分隔<br />如：某某某的生日&&结婚纪念日 | 非必填 |
| targetday  | 纪念日日期，公历格式20XX-XX-XX<br />农历年份前加n，多日期以&&分隔，注意与名称对应<br />如：n2020-08-11&&2021-08-26 | 非必填 |
|  msgtype   |        图文类型，默认单图文<br />1为单图文，2为多图文        | 非必填 |
|    link    |                        图文详情页网址                        | 非必填 |
|    call    |                   自定义称呼，例如：宝贝~                    | 非必填 |
|   title    |              自定义标题，例如：今天的推送来啦！              | 非必填 |
|  content   |            自定义第一段内容，例如：记得喝水水哦~             | 非必填 |
|    pic     |               自定义头图链接，以http/https开始               | 非必填 |
|  pictype   | 随机头图类型，默认fengjing<br />meizi、dongman、fengjing、suiji、none<br />分别是妹子、动漫、风景、随机、单图文不显示 | 非必填 |

## Deployment

部署教程完整版：扫描文末二维码，关注微信公众号 “勃然大陆” ，回复 “教程” 即可获得最新教程地址

​                               [金山文档](https://www.kdocs.cn/l/csn6eqw93kQZ)   [酷安图文](https://www.coolapk.com/feed/38775487?shareKey=YTYyZmUyYjMxMGIxNjMwYTRkYTc~)

部署教程精简版：[部署步骤](./docs/deployment.md)

## Update

每次更新详情请看 [更新日志](./docs/update.md)

## Notice

- 采用**[GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)协议**，坚决反对一切不尊重开发者、不尊重版权的行为。
- **图文展示页**回归，采用自己搭建的方式，更加安全放心。
- 提供极为详细的**方法函数模板**[template.py](./template.py)用于大家自行拓展，玩得开心~
- 受企业微信的限制，2022年6月20日后新建应用必须配置企业可信IP，在此之前创建的应用不受此限制。建议使用**云服务器或腾讯云函数**等IP固定的方式，阿里云、华为云函数暂时均无此功能，可能无法正常运行本项目。
- 受企业微信API限制，超出字数限制部分文字将自动截断不展示。图文展示页面不受此限制，但仍受图片链接长度和文字长度的制约，**请合理安排多地区天气、多日期提醒等内容**。
- 腾讯云日志服务CLS将于2022年9月5日开始执行按量计费。请在配置并测试好云函数之后及时前往 **函数管理 - 函数配置** 中关闭日志投递，并在 **[日志服务 CLS 控制台](https://console.cloud.tencent.com/cls) - 日志主题** 中删除相应日志主题，避免后续产生不必要的费用。
- 所有环境变量均可通过直接修改 config.py 完成配置，系统环境变量优先级高于 config.py 。
- **日期提醒** 会自动排序，越接近的时间越显示在上方，以保证提醒的有效性。
- **和风天气预报** 会根据天气文本信息自动更换对应的天气emoji图标。
- **图文展示页** 来自我的项目 **Diary** —— 基于 Python Fastapi 的简易图文展示，通过URL传递参数实现，不存储任何数据。开源地址：Github：https://github.com/Thund1R/diary     Gitee：https://gitee.com/thund1r/diary


## Thanks

这是我第一个被这么多人使用的项目，还是有点子激动的

感谢小红书用户猪咪不是猪、纠结当道（Github：rxrw）、酷安用户limobb（Github：limoest）等大佬的创意与部分代码参考

感谢所有支持、使用、打赏的用户。

不足之处，大家多多包涵，有什么问题可以进群交流反馈

欢迎关注微信公众号“**勃然大陆**”，回复 “**教程**” 即可获得最新教程地址

欢迎Star、Fork、PR，也欢迎打赏，再次感谢

![](https://b2.kuibu.net/file/imgdisk/2022/09/03/d871239275b8d9cfdc6bfe632c0f8d02.png)

![](https://b2.kuibu.net/file/imgdisk/2022/08/30/WPS.png)




import os
import requests
import json
from datetime import datetime, date, timedelta
import re
import config
import random
from zhdate import ZhDate

nowdatetime = (datetime.utcnow() + timedelta(hours=8))
corpid = config.get("corpid")
corpsecret = config.get("corpsecret")
agentid = config.get("agentid")
qweather = config.get("qweather")
link = config.get("link")
title = config.get("title")
content = config.get("content")
call = config.get("call")
pic = config.get("pic")
pic_type = config.get("pictype") if config.get("pictype") else "fengjing"
msg_type = str(config.get("msgtype")) if config.get("msgtype") else "1"
city_name_list = config.get_list("city")
target_day_list = config.get_list("targetday")
target_name_list = config.get_list("targetname")
begin_day_list = config.get_list("beginday")
begin_name_list = config.get_list("beginname")


# 获取标题数据
def get_my_title():
    my_title = title
    if my_title:
        return my_title
    else:
        # 需要通过接口获取动态内容时，请替换下一行内容
        return None


# 获取自定义第一段内容数据
def get_my_content():
    my_content = content
    if my_content:
        return my_content
    else:
        # 需要通过接口获取动态内容时，请替换下一行内容
        return None


# # 获取天行彩虹屁作为第一段内容，启用时请删除或注释掉上方get_my_content
# def get_my_content():
#     my_content = content
#     if my_content:
#         return my_content
#     else:
#         try:
#             caihong_url = "http://api.tianapi.com/caihongpi/index?key="+"你的天行Key"
#             caihong_res = requests.get(caihong_url).json()
#             caihong_item0 = caihong_res["newslist"][0]["content"]
#             caihong_tip = "🌈 " + caihong_item0
#             return caihong_tip
#         except Exception as e:
#             print("获取彩虹屁数据出错:", e)
#             return None


# # 示例：获取木小果平台彩虹屁作为第一段内容，启用时请删除或注释掉上方get_my_content
# def get_my_content():
#     my_content = content
#     if my_content:
#         return my_content
#     else:
#         try:
#             # 接口地址
#             caihong_url = "https://api.muxiaoguo.cn/api/caihongpi?api_key=" + "你的木小果平台Key"
#             # 数据结果并转换成json格式
#             caihong_res = requests.get(caihong_url).json()
#             print("获取彩虹屁json数据:", caihong_res)
#             # 数据结果是{"code":200,"msg":"success","data":{"comment":"遇见你以后，我睁眼便是花田，闭眼便是星空。"}}
#             # 根据数据的层级数和Key获取彩虹屁数据
#             caihong_item0 = caihong_res["data"]["comment"]
#             # 拼接数据
#             caihong_tip = "🌈 " + caihong_item0
#             return caihong_tip
#         except Exception as e:
#             print("获取彩虹屁数据出错:", e)
#             return None


# 获取自定义图片数据
def get_my_pic():
    my_pic = pic
    if my_pic:
        return my_pic
    else:
        return None


# # 示例：获取随机图片作为头图(已经自带本功能，填写或者动态获取title、content都会触发)
# def get_my_pic():
#     my_pic = pic
#     if my_pic:
#         return my_pic
#     else:
#         try:
#             pic_url = f"https://api.btstu.cn/sjbz/api.php?format=json&lx=fengjing"
#             pic_res = requests.get(pic_url).json()
#             print("获取自定义图片json数据:", pic_res)
#             return pic_res["imgurl"]
#         except Exception as e:
#             print("获取随机图片数据出错:", e)
#             return None


# 获取金山词霸数据
def get_ciba():
    try:
        ciba_url = "http://open.iciba.com/dsapi/"
        r = requests.get(ciba_url).json()
        ciba_en = r["content"]
        ciba_zh = r["note"]
        ciba_pic = r["fenxiang_img"]
        ciba_tip = "🔤 "+ciba_en+"\n"+"🀄️ "+ciba_zh
        return {
            "ciba_tip": ciba_tip,
            "ciba_pic": ciba_pic
        }
    except Exception as e:
        print("获取金山词霸数据出错:", e)
        return None

# 获取XXX自定义图片与文字函数可以放置在此
# 参考上方获取金山词霸数据get_ciba()代码编写与位置放置，注意缩进
# 务必要在下方handle_message()里编写接收自定义数据的代码
# 具体内容请参考并使用template.py进行测试
# def get_XXX():
#     try:
#         XXX_url = "https://XXXX.XXX"
#         XXX_res = requests.get(XXX_url).json()
#         print("获取XXX自定义图片与文字json数据:", XXX_res)
#         XXX_item0 = XXX_res["键名"][n]["需要的数据键名"]
#         XXX_item1 = XXX_res["键名"][n]["需要的数据键名"]
#         XXX_pic = XXX_res["键名"][n]["需要的数据键名"]
#         XXX_tip = "✒️ " + XXX_item0 + "\n" + "🗓️ " + XXX_item1
#         res = {
#             # 没有图片就删除下面这一句
#             "XXX_pic": XXX_pic,
#             "XXX_tip": XXX_tip
#         }
#         print("获取XXX数据:", res)
#         return res
#     except Exception as e:
#         print("获取XXX数据出错:", e)
#         return None


# 获取随机图片链接数据
# 来自搏天API:https://api.btstu.cn/
def get_random_pic():
    lx = pic_type if pic_type != "none" else "fengjing"
    try:
        pic_url = f"https://api.btstu.cn/sjbz/api.php?format=json&lx={lx}"
        r = requests.get(pic_url).json()
        return r["imgurl"]
    except Exception as e:
        print("获取随机图片数据出错:", e)
        return None


# 获取当前日期与招呼数据
def get_today():
    ndt = nowdatetime
    d = ndt.strftime("%Y{y}%m{m}%d{d}").format(y='年', m='月', d='日')
    w = int(ndt.strftime("%w"))
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today_date = d + " " + week_list[w] + " "
    now_time = ndt.strftime("%H:%M:%S")
    time_tip = ""
    if "00:00:00" <= now_time < "06:00:00":
        time_tip = "凌晨好"
    elif "06:00:00" <= now_time < "09:00:00":
        time_tip = "早上好"
    elif "09:00:00" <= now_time < "12:00:00":
        time_tip = "上午好"
    elif "12:00:00" <= now_time < "13:00:00":
        time_tip = "中午好"
    elif "13:00:00" <= now_time < "18:00:00":
        time_tip = "下午好"
    elif "18:00:00" <= now_time < "23:59:59":
        time_tip = "晚上好"
    time_tip = time_tip + " ~ " + get_emoticon()
    today_tip = (call+time_tip) if call else time_tip
    return {
        "today_date": today_date,
        "today_tip": today_tip
    }


# 获取随机颜文字
def get_emoticon():
    emoticon_list = ["(￣▽￣)~*", "(～￣▽￣)～", "︿(￣︶￣)︿", "~(￣▽￣)~*", "(oﾟ▽ﾟ)o", "ヾ(✿ﾟ▽ﾟ)ノ", "٩(๑❛ᴗ❛๑)۶", "ヾ(◍°∇°◍)ﾉﾞ", "ヾ(๑╹◡╹)ﾉ", "(๑´ㅂ`๑)", "(*´ﾟ∀ﾟ｀)ﾉ", "(´▽`)ﾉ", "ヾ(●´∀｀●)",
                     "(｡◕ˇ∀ˇ◕)", "(≖ᴗ≖)✧", "(◕ᴗ◕✿)", "(❁´◡`❁)*✲ﾟ*", "(๑¯∀¯๑)", "(*´・ｖ・)", "(づ｡◕ᴗᴗ◕｡)づ", "o(*￣▽￣*)o", "(｀・ω・´)", "( • ̀ω•́ )✧", "ヾ(=･ω･=)o", "(￣３￣)a", "(灬°ω°灬)", "ヾ(•ω•`。)", "｡◕ᴗ◕｡"]
    return random.choice(emoticon_list)


# 获取bing每日壁纸数据
def get_bing():
    try:
        bing_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
        res = requests.get(bing_url).json()
        bing_pic = "https://cn.bing.com/"+res["images"][0]["url"]
        bing_title = res["images"][0]["title"]
        bing_content = re.sub(u"\\(.*?\\)", "", res["images"][0]["copyright"])
        bing_tip = bing_title+"——"+bing_content
        return {
            "bing_pic": bing_pic,
            "bing_tip": bing_tip
        }
    except Exception as e:
        print("获取必应数据出错:", e)
        return None


# 获取和风天气数据
def get_weather(city_name):
    try:
        city_id = None
        weather_list = []
        weather_info = None
        city = city_name.split("-")[0]
        county = city_name.split("-")[1]
        city_url = f"https://geoapi.qweather.com/v2/city/lookup?&adm={city}&key={qweather}&location={county}"
        city_json = requests.get(city_url).json()
        city_code = city_json["code"]
        if city_code.__eq__("200"):
            city_id = city_json["location"][0]["id"]
        else:
            print(
                f"没有找到{city_name}这个地方，请检查city值是否正确，格式是否为 省/市-市/区/县 ，例如 成都-双流&&江苏-江宁")
        if city_id:
            # 获取逐天天气预报，有很多天气类信息，可以根据自己需要进行获取和拼接
            # 具体请参考和风天气API开发文档https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
            weather_url = f"https://devapi.qweather.com/v7/weather/3d?key={qweather}&location={city_id}"
            weather_json = requests.get(weather_url).json()
            weather_code = weather_json["code"]
            if weather_code.__eq__("200"):
                temp = weather_json["daily"][0]
                textDay = temp["textDay"]
                tempMin = temp["tempMin"]
                tempMax = temp["tempMax"]
                weather_icon = get_weather_icon(textDay)
                weather_tip = weather_icon+" "+county+textDay+"，"+tempMin+"~"+tempMax+"℃"
                weather_list.append(weather_tip)
            # 获取生活指数，有很多生活类信息，可以根据自己需要进行获取和拼接
            # 具体请参考和风天气API开发文档https://dev.qweather.com/docs/api/indices/
            life_url = f"https://devapi.qweather.com/v7/indices/1d?type=0&location={city_id}&key={qweather}"
            life_json = requests.get(life_url).json()
            life_code = life_json["code"]
            if life_code.__eq__("200"):
                life_tip = "👔 "+life_json["daily"][2]["text"]
                weather_list.append(life_tip)
            # 需要和风天气其他接口的信息请参考以上代码格式进行获取和添加，所有开发文档https://dev.qweather.com/docs/api/

            weather_info = '\n'.join(weather_list)
        else:
            print(
                f"获取{city_name}ID失败，请检查qweather、city值是否正确，city格式是否为 省/市-市/区/县 ，例如 四川-成都&&江苏-江宁")
        return weather_info
    except Exception as e:
        print(f"获取{city_name}和风天气数据出错:", e)
        return None


# 获取天气icon
def get_weather_icon(text):
    weather_icon = "🌤️"
    weather_icon_list = ["☀️",  "☁️", "⛅️",
                         "☃️", "⛈️", "🏜️", "🏜️", "🌫️", "🌫️", "🌪️", "🌧️"]
    weather_type = ["晴", "阴", "云", "雪", "雷", "沙", "尘", "雾", "霾", "风", "雨"]
    for index, item in enumerate(weather_type):
        if re.search(item, text):
            weather_icon = weather_icon_list[index]
            break
    return weather_icon


# 获取所有天气数据
def get_map_weather(city_name):
    if qweather and city_name:
        map_weather_tip = None
        weather_list = list(map(get_weather, city_name))
        weather_list = list(filter(None, weather_list))
        if weather_list:
            map_weather_tip = "\n".join(weather_list)
        return map_weather_tip
    else:
        print("和风天气秘钥qweather或城市city配置缺失")
        return None


# 计算每年纪念日
def get_remain(target_day, target_name):
    ndt = nowdatetime
    today = date(ndt.year, ndt.month, ndt.day)
    this_year = datetime.now().year
    target_day_year = target_day.split("-")[0]
    if target_day_year[0] == "n":
        lunar_mouth = int(target_day.split("-")[1])
        lunar_day = int(target_day.split("-")[2])
        this_date = ZhDate(this_year, lunar_mouth,
                           lunar_day).to_datetime().date()
    else:
        solar_month = int(target_day.split("-")[1])
        solar_day = int(target_day.split("-")[2])
        this_date = date(this_year, solar_month, solar_day)
    if today == this_date:
        remain_day = 0
        remain_tip = f"🌟 {target_name}就是今天啦！"
    elif today > this_date:
        if target_day_year[0] == "n":
            lunar_next_date = ZhDate(
                (this_year + 1), lunar_mouth, lunar_day).to_datetime().date()
            next_date = date(
                (this_year + 1), lunar_next_date.month, lunar_next_date.day)
        else:
            next_date = date(
                (this_year + 1), solar_month, solar_day)
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        remain_tip = f"🗓️ 距离{target_name}还有 {remain_day} 天"
    else:
        next_date = this_date
        remain_day = int(str(next_date.__sub__(today)).split(" ")[0])
        remain_tip = f"🗓️ 距离{target_name}还有 {remain_day} 天"
    return (remain_tip, remain_day)


# 计算某天间隔天数
def get_duration(begin_day, begin_name):
    ndt = nowdatetime
    today = date(ndt.year, ndt.month, ndt.day)
    begin_day_year = begin_day.split("-")[0]
    if begin_day_year[0] == "n":
        lunar_year = int(begin_day_year[1:])
        lunar_mouth = int(begin_day.split("-")[1])
        lunar_day = int(begin_day.split("-")[2])
        begin_date = ZhDate(lunar_year, lunar_mouth,
                            lunar_day).to_datetime().date()
    else:
        solar_year = int(begin_day.split("-")[0])
        solar_month = int(begin_day.split("-")[1])
        solar_day = int(begin_day.split("-")[2])
        begin_date = date(solar_year, solar_month, solar_day)
    if today == begin_date:
        duration_day = 0
        duration_tip = f"🌟 {begin_name}就是今天啦！"
    elif today > begin_date:
        duration_day = int(str(today.__sub__(begin_date)).split(" ")[0])
        duration_tip = f"🗓️ {begin_name}已经 {duration_day} 天"
    else:
        duration_day = int(str(begin_date.__sub__(today)).split(" ")[0])
        duration_tip = f"🗓️ 距离{begin_name}还有 {duration_day} 天"
    return (duration_tip, duration_day)


# 获取第一个元素
def get_elemzero(elem):
    return elem[0]


# 获取第二个元素
def get_elemone(elem):
    return elem[1]


# 获取所有日期数据
def get_days_tip():
    days_list = []
    days_tip = ""
    target_res = ""
    if target_day_list or target_name_list:
        if len(target_day_list) == len(target_name_list):
            try:
                target_res = list(
                    map(get_remain, target_day_list, target_name_list))
                days_list.extend(target_res)
            except Exception as e:
                print("获取纪念日数据出错，请检查纪念日targetname与targetday填写是否正确", e)
                return None
        else:
            print("获取纪念日数据出错，请检查纪念日targetname与targetday数量是否相等")
    else:
        print("未配置纪念日")

    begin_res = ""
    if begin_day_list or begin_name_list:
        if len(begin_day_list) == len(begin_name_list):
            try:
                begin_res = list(
                    map(get_duration, begin_day_list, begin_name_list))
                days_list.extend(begin_res)
            except Exception as e:
                print("获取单日数据出错，请检查单日beginname与beginday填写是否正确", e)
                return None
        else:
            print("获取单日数据出错，检查单日beginname与beginday数量是否相等")
    else:
        print("未配置单日")

    days_list = list(filter(None, days_list))
    if days_list:
        days_list.sort(key=get_elemone)
        res = list(map(get_elemzero, days_list))
        days_tip = "\n".join(res)
    return days_tip


# 获取ONE一个图文数据
def get_one():
    try:
        one_url = "https://apier.youngam.cn/essay/one"
        r = requests.get(one_url).json()['dataList'][0]
        one_id = "VOL."+r['id']
        one_pic = r['src']
        one_tip = f"✒️ {one_id} {r['text']}"
        return {
            "one_pic": one_pic,
            "one_tip": one_tip
        }
    except Exception as e:
        print("获取ONE一个图文数据出错:", e)
        return None


# 处理多图文内容
def handle_extra(out_title, inner_title, content, pic, art_link):
    if msg_type == "2":
        if out_title or inner_title or content or pic or art_link:
            own_link = link
            if out_title is None and content:
                out_title = content
            elif out_title is None and inner_title:
                out_title = inner_title
            elif out_title is None:
                out_title = "查看图片"

            picurl = pic if pic else get_random_pic()
            inner_title = inner_title.replace(
                "\n", "\\n") if inner_title else None
            content = content.replace("\n", "\\n") if content else None
            url = art_link if art_link else f"{own_link}?t={inner_title}&p={picurl}&c={content}"
            return {
                "title": out_title,
                "url": url,
                "picurl": picurl
            }
        else:
            print("多图文没有任何内容，生成链接失败")
            return None
    else:
        return None


# 处理所有信息
def handle_message():
    lx = pic_type
    own_link = link
    own_title = get_my_title()
    own_content = get_my_content()
    own_pic = get_my_pic()
    # 接收必应数据
    bing_pic = ""
    bing_tip = ""
    bing_data = get_bing()
    if bing_data:
        bing_pic = bing_data["bing_pic"]
        bing_tip = bing_data["bing_tip"]

    info_list = []
    extra_content = []
    today_data = get_today()
    today_date = today_data["today_date"]
    today_tip = today_data["today_tip"]
    info_list.append("\n"+today_tip)
    if own_pic or own_title or own_content:
        art_pic = own_pic if own_pic else get_random_pic()
        art_title = today_date + "\n" + own_title if own_title else today_date
        if own_content:
            info_list.append(own_content)
        extra_content.append(handle_extra(
            art_title, art_title, own_content, art_pic, None))
    elif bing_tip and lx != "none":
        art_pic = bing_pic
        art_title = today_date + "\n" + bing_tip
        extra_content.append(handle_extra(
            today_date, today_date, bing_tip, bing_pic, None))
    else:
        art_title = today_date
        art_pic = get_random_pic()
        extra_content.append(handle_extra(
            art_title, art_title, own_content, art_pic, None))
    art_pic = art_pic if lx != "none" else None

    # 接收XXX数据请放置在下方，下列各数据放置的顺序即显示的顺序
    # 不需要的数据请在下面删除
    # 不需要出现在单图文的请删除info_list.append(XXX)
    # 不需要出现在多图文的请删除extra_content.append(XXX)
    # 都不要的数据直接删除一整段即可
    # 务必注意缩进，形式参考下方获取天气数据

    # # 接收XXX数据
    # XXX_data = get_XXX()
    # if XXX_data:
    #     XXX_tip = XXX_data["XXX_tip"]
    #     # 没有pic就删除下面这一句
    #     XXX_pic = XXX_data["XXX_pic"]
    #     # 单图文添加数据，不需要就删除下面这一句
    #     info_list.append(XXX_tip)
    #     # 多图文添加数据，不需要就删除下面这一整句
    #     extra_content.append(handle_extra(
    #         out_title, inner_title, content, pic, link))
    #     # 以上五个参数分别是多图文卡片标题（外标题）, 多图文展示页标题（内标题）, 多图文内容, 多图文头图, 自定义跳转链接
    #     # 前三个参数必填。后两个参数pic、link没有就填None

    # 接收天气数据
    weather_tip = get_map_weather(city_name_list)
    if weather_tip:
        info_list.append(weather_tip)
        extra_content.append(handle_extra(
            weather_tip, "Weather", weather_tip, None, None))

    # 接收日期数据
    days_tip = get_days_tip()
    if days_tip:
        info_list.append(days_tip)
        extra_content.append(handle_extra(
            days_tip, "Days", days_tip, None, None))

    # 接收金山词霸数据
    ciba_data = get_ciba()
    if ciba_data:
        ciba_tip = ciba_data["ciba_tip"]
        ciba_pic = ciba_data["ciba_pic"]
        info_list.append(ciba_tip)
        extra_content.append(handle_extra(
            ciba_tip, "iCiba", ciba_tip, ciba_pic, None))

    # 接收ONE一个数据
    one_data = get_one()
    if one_data:
        one_tip = one_data["one_tip"]
        one_pic = one_data["one_pic"]
        info_list.append(one_tip)
        extra_content.append(handle_extra(
            one_tip, "ONE·一个", one_tip, one_pic, None))

    # 处理文本格式
    info_content = "\n\n".join(info_list)
    info_detail = info_content.replace("\n", "\\n")
    page_title = art_title.replace("\n", "\\n")
    page_detail = info_detail
    page_pic = art_pic
    art_url = f"{own_link}?t={page_title}&p={page_pic}&c={page_detail}"

    # 封装数据
    article = [{
        "title": art_title,
        "description": info_content,
        "url":art_url,
        "picurl": art_pic
    }]

    if msg_type == "2":
        article = list(filter(None, extra_content))
    msg = {
        "touser": "@all",
        "toparty": "",
        "totag": "",
        "msgtype": "news",
        "agentid": agentid,
        "news": {
            "articles": article
        },
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    return msg


# 获取调用接口凭证
def get_token(corpid, corpsecret):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    values = {
        "corpid": corpid,
        "corpsecret": corpsecret,
    }
    res = requests.get(url, params=values).json()
    if res["errcode"] == 0:
        return res["access_token"]
    else:
        print("企业微信access_token获取失败: " + str(res) +
              "请检查corpid、corpsecret、agentid单词拼写是否正确，值是否有多余空格")
        return None


# 处理图文详情页
def handle_html(url_data):
    with open(os.path.join(os.path.dirname(__file__), "show.html"), 'r', encoding='utf-8') as f:
        html = f.read()
    p = url_data.get("p")
    t = url_data.get("t")
    c = url_data.get("c")
    if p and p != "none" and p != "None":
        html = html.replace(".pic{display:none}", "").replace("<&p&>", p)
    if t and t != "none" and t != "None":
        t = t.replace("\\n", "<br/>")
        html = html.replace(".title{display:none}", "").replace("<&t&>", t)
    if c and c != "none" and c != "None":
        c = c.replace("\\n", "<br/>")
        html = html.replace(".content{display:none}", "").replace("<&c&>", c)
    return html


# 主函数
def main():
    if corpid and corpsecret and agentid:
        data = handle_message()
        token = get_token(corpid, corpsecret)
        if token is None:
            return 0
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
        res = requests.post(url, json=data).json()
        if res["errcode"] == 0:
            print("企业微信消息发送成功")
            return 1
        elif res["errcode"] != 0:
            print("企业微信消息发送失败: "+str(res))
            return 0
    else:
        print("企业微信配置缺失，请检查corpid、corpsecret、agentid是否配置，单词拼写是否正确")
        return 0


# 腾讯云入口函数
def main_handler(event, context):
    url_data = event.get("queryString")
    if url_data:
        html = handle_html(url_data)
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }
    else:
        res = main()
        if res:
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {"Content-Type": "text/html"},
                "body": '{"code":"200","message":"企业微信消息发送成功"}'
            }
        else:
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": {"Content-Type": "text/html"},
                "body": '{"code":"404","message":"企业微信消息发送失败"}'
            }


# 其他云函数入口
def handler(event, context):
    main()


# 本地运行入口
if __name__ == "__main__":
    main()

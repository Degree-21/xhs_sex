# -*- encoding=utf8 -*-
__author__ = "Administrator"

import time

from airtest.aircv import *
from airtest.core.api import *
from urllib import parse
import requests
import json

import traceback

appId = ""
appSecret = ""
token = "24.459a31ea245ff91f270b9db089aaed29.2592000.1611999145.282335-23471459"
selectTitle = "运动健身"


def get_token():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s&" % (
    appId, appSecret)
    res = requests.get(url)
    json_info = json.loads(res.content)
    return json_info["access_token"]

def is_sex(img_base):
    img_base = str(img_base).replace("\n","")
    f = open("./ta.txt", "w")
    f.write("data:image/png;base64,"+img_base)
    f.close()
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined?access_token=%s" % token
    data = "image=%s" % img_base
    head = {"Content-Type": "application/x-www-form-urlencoded"}
    form_data = {
        "image": img_base
    }
    data = parse.urlencode(form_data)
    res = requests.post(url, headers=head, data=data.encode("utf-8"))
    json_info = json.loads(res.content)
    print(json.dumps(json_info))
    if json_info["conclusionType"] == 1:
        return False

    # 返回true证明是个超级美女 所以需要收藏 ！！！！
    return True



# 滑动一屏 屏幕
def swipe_windows(w, h):
    touch([0.5 * w, 0.5 * h])  # 点击手机中心位置
    swipe((0.5 * w, 0.8 * h), vector=(0, -0.5), duration=0.1)  # 在0.1s内上划0.5个屏幕


def swipe_left(w, h):
    touch([0.5 * w, 0.5 * h])  # 点击手机中心位置
    swipe((0.9 * w, h / 2), (0.1 * w, h / 2), vector=(0, -0.5), duration=0.1)  # 在0.1s内上划0.5个屏幕


def swipe_right(w, h):
    touch([0.5 * w, 0.5 * h])  # 点击手机中心位置
    swipe((0.1 * w, h / 2), (0.9 * w, h / 2), vector=(0, -0.5), duration=0.1)  # 在0.1s内上划0.5个屏幕


try:
    devices = init_device("Android")

    XHS_APP = 'com.xingin.xhs'
    # or use connect_device api with default params
    connect_device("Android:///")

    from poco.drivers.android.uiautomation import AndroidUiautomationPoco

    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    w, h = poco.get_screen_size()
    stop_app(XHS_APP)
    start_app(XHS_APP)

    # 点击运动健身 美女如云 也可以注释 从首页开始 获取
    while True:
        if poco(text="首页").exists():
            poco(text="首页").click()
            poco(selectTitle).click()
            break
        continue
            
    while True:
        print("进入了")
        time.sleep(2)
        
        window_count = poco("com.xingin.xhs:id/dyk").child("android.widget.LinearLayout").offspring(
            "androidx.drawerlayout.widget.DrawerLayout").offspring("com.xingin.xhs:id/avi").offspring(
            "com.xingin.xhs:id/c63").child("com.xingin.xhs:id/a5k")
        
        if window_count.exists() is False:
            continue

        print(window_count)

        for v in window_count:
            save_img = "save_%s.jpg" % time.time()
            if v.exists() is False:
                continue
            v.click()
            b64img, fmt = poco.snapshot(width=720)
            time.sleep(2)
            if len(b64img) <= 0:
                print("没有获取到图片跳过")
                swipe_right(w, h)
                continue

            try:
                # todo 调用百度ai api 查询是是否是性感图片 如果是则收藏点赞
                # 真正用来判断是一个视频还是一个文章    先不考虑 是否已经收藏过了
                is_sex_res = is_sex(b64img)
#                 is_sex_res = Falsea
                print("查看到底是不是一个性感的美女呢 %s" %  str(is_sex_res))
                if is_sex_res is True:
                    # 证明是一个性感的美女  所以进行收藏
                    if poco("com.xingin.xhs:id/matrixFollowView").exists():
                        poco("com.xingin.xhs:id/bsv").click()
                        print("是一个视频，已经点击收藏了")
                    else:
                        poco("com.xingin.xhs:id/cs5").click()
                        print("是一个文章，已经点击收藏来")
                else:
                    print("不是性感美女跳过！！！！")

                # 如果存在弹窗的话 把他关闭
                if poco("com.xingin.xhs:id/c6i").exists() is True:
                    poco("com.xingin.xhs:id/c6i").click()

                # 查询如果存在评分弹窗的话 进行点击
    #             if poco("android.widget.FrameLayout").offspring("android:id/content").child("android.widget.LinearLayout").offspring("com.xingin.xhs:id/cdc").child("android.widget.ImageView")[4].exists() is True:
    #                 poco("android.widget.FrameLayout").offspring("android:id/content").child("android.widget.LinearLayout").offspring("com.xingin.xhs:id/cdc").child("android.widget.ImageView")[4].click()
                if poco("com.xingin.xhs:id/c5_").exists() is True:
                    poco("com.xingin.xhs:id/c5_").click()
            except Exception as e:
                traceback.print_exc()
            finally:
                 
                # 不管性不性感都需要回去刷新数据
                if poco("com.xingin.xhs:id/rc").exists() is True:
                    print("可能是个video也可能是个文章")
                    poco("com.xingin.xhs:id/rc").click()
                else:
                    if poco(text=selectTitle).exists():
                        print(selectTitle + "选中")
                    else:
                        print("后退")
                        swipe_right(w, h)
        swipe_windows(w, h)
       


except Exception as e:
    traceback.print_exc()
    print(e)




















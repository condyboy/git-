import requests
from urllib.parse import urlencode
import json
from requests.exceptions import RequestException
import os
from hashlib import md5

#获取系统当前路径
path=os.getcwd()


def get_page(offest,keyword):

        headers={
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
                "cookie":"tt_webid=6718643773326738952; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6718643773326738952; csrftoken=b595c67b0e1dcf9cae8414a80d1d6129; UM_distinctid=16c37e9ef1716c-0d23e69f99fbb8-c343162-144000-16c37e9ef183fb; __user_from=mobile_qq; __tasessionId=ars5fa5341564389009880; CNZZDATA1259612802=1553206227-1564301942-https%253A%252F%252Fwww.toutiao.com%252F%7C1564386774; s_v_web_id=28cf25b2e4e150dfffee289bdad1dec4"
        }
        data={
        "aid": 24,
        "app_name": "web_search",
        "offset": offest,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": "20",
        "en_qc": 1,
        "cur_tab": 1,
        "from": "search_tab",
        }
        url="https://www.toutiao.com/api/search/content/?"+urlencode(data)
        try:
                response=requests.get(url,headers=headers)
                if(response.status_code==200):
                        print("请求成功")
                        #使用response.encoding来改变爬虫的中文编码，通过document.charset可以查看网页编码
                        response.encoding="utf-8"
                        return response.text
        except RequestException:
                print("出现异常")
                return None


def parse_page_index(html):
        data = json.loads(html)
        if data and "data" in data:
                for i in data.get("data"):
                        if(i.get("title")==None):
                                continue
                        #获取img_list
                        img_list=i.get("image_list")
                        if not os.path.exists(path+'\picture\{}'.format(i.get("title"))):
                                os.mkdir(path+'\picture\{}'.format(i.get("title")))
                        #图片路径
                        pic_file=path+'\picture\{}'.format(i.get("title"))
                        for img in img_list:
                                littleimg=img.get("url")
                                imgcontent=requests.get(littleimg)
                                img_path=pic_file+'\{}'.format(md5(imgcontent.content).hexdigest())+".jpg"
                                if not os.path.exists(img_path):
                                        with open(img_path,"wb") as f:
                                                f.write(imgcontent.content)
                                                print("写入照片{}成功".format(pic_file+'\{}'.format(md5(imgcontent.content).hexdigest())+".jpg"))
                                                f.close()
                        



                        

def main():
        print(path)
        for i in range(0,100,20):
                html=get_page(i,"街拍")
                parse_page_index(html)
                        
if __name__ == "__main__":
    main()

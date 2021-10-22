from selenium import webdriver
import requests
from PIL import Image
from io import BytesIO
import time
import json
import tqdm
import os
import datetime
import pandas as pd
import re
import random
from selenium.common.exceptions import NoSuchElementException



'''
from weiboSpiderv1 import *

# 初始化浏览器对象
executable_path='E:\EdgeDownload\chromedriver_win32\chromedriver.exe'
options= webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(executable_path = executable_path,options=options)
driver.maximize_window()
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
})
# 加载新浪以及cookies
driver.get('https://weibo.com/')


fp = open('cookies//weiboCookie.json','r')
cookies = json.load(fp)
fp.close()
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()
driver.get('https://weibo.com/')

# 点击热点事件
hot_blog_btn = driver.find_element_by_xpath('//*[@id="v6_pl_leftnav_group"]/div[2]/div[1]/div[5]/div[1]/a')
hot_blog_btn.click()

# 爬取数据代码
weibo_hot_crawler(driver)

# 结束时保存cookies
cookies = driver.get_cookies()
fp = open('cookies//weiboCookie.json','w')
json.dump(cookies,fp)
fp.close()

for i in range(10):
    crawler_weibo_by_label(driver)
'''


class UserAgent:
    def __init__(self):
        self.agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
        "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        ]
    def __str__(self):
        return 'Agents:'+'\n\t'.join(self.agents)
    
    def __repr__(self):
        return self.__str__()
    
    def get_headers(self):
        # 随机选取User-Agent
        random_user = random.choice(self.agents)
        # 创建headers
        headers = {'User-Agent' : random_user}
        return headers



def get_avatar(element_object,uid,headers,avater_path = 'F:\\Datasets\\social-data\\Avatar\\'):
    '''用于保存用户头像，并且命名为用户id
    参数：
        element_object: 读取好的用户消息对象
        uid: 用户id
        headers： 用于伪造请求头的字典
        avater_path: 保存的位置
    返回:
        无
    Tips:
        使用requests库读取用户的头像链接，并且重命名为  用户id.png
    '''
    # 获取用户头像的函数
    r = requests.get(element_object.get_attribute('src'),headers=headers)
    img = Image.open(BytesIO(r.content))
    img.save(avater_path + str(uid) + '.png')

def save_image(element_object,pic_id,headers,image_path='F:\\Datasets\\social-data\\image\\'):
    '''保存消息里的单个图片，并且以链接中的照片id命名
    参数:
        element_object: 浏览器里的照片对象
        pic_id: src链接里的照片id
        headers： 用于伪造请求头的字典
        image_path: 保存的位置
    返回:
        无
    Tips：
        需要在获取src以后，将地址换成mw690用于显示大图片，例如 //wx2.sinaimg.cn/thumb150/b398fe37gy1gqj1z7611fj20zj1betqq.jpg是小图，
            而//wx2.sinaimg.cn/mw690/b398fe37gy1gqj1z7611fj20zj1betqq.jpg就是大图片
    '''
    src_list = re.split(r'/',element_object.get_attribute('src'))
    src_list = src_list[0:3] + ['mw690'] + src_list[4:]
    src = '/'.join(src_list)
    r = requests.get(src,headers=headers)
    #print(src)
    img = Image.open(BytesIO(r.content))
    img.save(image_path + str(pic_id) + '.png')

#path = '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/div[3]/div[6]/div/ul/li/div[2]/div/video'
#ele = driver.find_element_by_xpath(path)

def save_video(element_object,video_name,headers,video_path='F:\\Datasets\\social-data\\video\\'):
    src = element_object.get_attribute('src')
    r = requests.get(src,headers=headers)
    with open(video_path + video_name,'wb') as file:
        file.write(r.content)


def process_home_message(driver,xpath,headers,label=None,wait=3):
    '''爬取一个选项卡的数据
    参数：
        driver：浏览器对象
        xpath： 选项卡的路径
        wait： 等待的时长
        headers: 用于伪造的请求头
    返回：
        source： 平台，这里默认还是新浪微博
        mid：消息id，也就是 选项卡的主码
        key_word： 关键词，这里因为是热门信息，所以没有关键词，设置为None
        message_type： 消息类型，默认还是博文
        user_id： 用户id
        user_name： 用户昵称
        article： 文本内容
        like_num： 点赞数量
        comment_num： 评论数量
        retweet_num： 转发数量
        timestamp： 时间戳，这里可以直接获取，所以抛弃了之前的相对时间的做法
        flag： 这里因为是热门微博，所以默认为True
        img_list： 包含的图像列表，使用图像的id作为主码进行重命名保存
        video_list： 这条消息包含的视频的id
        platform： 消息发布的平台，这跟用户设置有关系
    Tips:
        额外读取用户头像与用户发布的图片，并且保存在特定的文件夹中。对于图片个数设置上限为9，因为大部分人最多发布九宫格就结束了，更多的也不进行获取。
    '''
    source = 'sina_weibo'
    message_type = 'blog_article'
    key_word = 'None'
    # 获取显示的条目并获取mid
    root_item = driver.find_element_by_xpath(xpath)
    mid = root_item.get_attribute('mid')
    # 获取oid，不清楚oid和uid有什么区别
    user_id = re.split(r'\=',root_item.get_attribute('tbinfo'))[1]
    # 判断用户是否有皮肤卡
    user_info_obj = driver.find_element_by_xpath(xpath + '/div[1]/div[2]')
    if user_info_obj.get_attribute('class') == 'WB_face W_fl':
        avatar_path = '/div[2]'
        date_path = '/div[3]'
    else:
        avatar_path = '/div[3]'
        date_path = '/div[4]'
    # 获取用户名
    user_avatar_obj = driver.find_element_by_xpath(xpath + '/div[1]' + avatar_path +'/div[1]/a/img')
    user_name = user_avatar_obj.get_attribute('title')
    # 保存头像并且以用户id命名
    get_avatar(user_avatar_obj,user_id,headers=headers)
    # 获取时间戳
    date_obj = driver.find_element_by_xpath(xpath + '/div[1]' + date_path +'/div[2]/a[1]')
    timestamp = date_obj.get_attribute('date')
    # 获取平台
    try:
        platform_obj = driver.find_element_by_xpath(xpath + '/div[1]' + date_path +'/div[2]/a[2]')
    except NoSuchElementException:
        platform = ''
    else:
        platform = platform_obj.text
    # 获取全文
    try:
        more_btn = driver.find_element_by_xpath(xpath + '/div[1]' + date_path + '/div[4]/a')
    except:
        article_path = '/div[4]'
        picture_path = '/div[6]'
    else:
        # 判断是否是获取全文按钮
        if more_btn.get_attribute('class') == 'WB_text_opt':
            more_btn.click()
            # 点击后等待
            time.sleep(wait)
            article_path = '/div[5]'
            picture_path = '/div[7]'
        else:
            article_path = '/div[4]'
            picture_path = '/div[6]'
    # 获取文字
    article_obj = driver.find_element_by_xpath(xpath + '/div[1]' + date_path + article_path)
    article = article_obj.text
    # 默认是热点信息
    flag = True
    # 获取点赞评论转发
    retweet_num = driver.find_element_by_xpath(xpath + '/div[2]/div/ul/li[2]/a/span/span/span/em[2]').text
    if re.search(r'\d+',retweet_num) is None:
        retweet_num = 0
    comment_num = driver.find_element_by_xpath(xpath + '/div[2]/div/ul/li[3]/a/span/span/span/em[2]').text
    if re.search(r'\d+',comment_num) is None:
        comment_num = 0
    like_num = driver.find_element_by_xpath(xpath + '/div[2]/div/ul/li[4]/a/span/span/span/em[2]').text
    if re.search(r'\d+',like_num) is None:
        like_num = 0
    img_list = []
    # 获取图片，最多获取九个
    for li in range(1,10):
        try:
            image_obj = driver.find_element_by_xpath(xpath +'/div[1]' + date_path + picture_path + '/div/ul/li[{}]/img'.format(li))
        except:
            break
        else:
            img_id = re.split(r'\.',re.split(r'/',image_obj.get_attribute('src'))[-1])[0]
            img_list.append(img_id)
            save_image(image_obj,img_id,headers=headers)
    #print(img_list)
    # 获取视频
    video_path = xpath +'/div[1]' + date_path + picture_path + '/div/ul/li/div[2]/div/video'
    try:
        video_element = driver.find_element_by_xpath(video_path)
    except:
        video_list = []
    else:
        src = video_element.get_attribute('src')
        if re.search(r'blob:https',src) is not None:
            video_list = []
        else:
            video_name = re.split(r'/',re.split(r'\?',src)[0])[-1]
            print(src)
            save_video(video_element,video_name,headers)
            video_list = [re.split(r'\.',video_name)[0]]
    return [source,mid,key_word,message_type,user_id,user_name,article,like_num,comment_num,retweet_num,timestamp,flag,img_list,video_list,platform,label]



def load_data(driver,max_length=310,wait = 3,sleep_time=5,retry=3,scroll=5000,step=100,smallwait = 0.3):
    '''加载一次数据的代码，用于提前加载数据
    参数：
        driver：浏览器对象
        max_length=310： 加载数据的最大长度，默认为310，微博一次最多加载310条数据
        wait = 3： 每次加载更多的等待时间
        sleep_time=5： 每次点击加载的等待时间
        retry=3： 重新尝试的次数
        scroll = 5000： 每次加载滑动的总像素长度
        step： 每次下拉的步长
        smallwait： 每一步下拉的等待时间
    返回：
        i： 本次加载最多成功加载了多少条数据
            输出条数与用时
    '''
    print('Loading Data!')
    start=datetime.datetime.now()
    # 微博一个页面最多一次加载300条，存在限制
    try:
        for i in tqdm.tqdm(range(1,max_length)):
            #print('index',i)
            # 下拉加载数据
            try:
                element = driver.find_element_by_xpath('//*[@id="Pl_Core_NewMixFeed__3"]/div/div[2]/div[{}]'.format(i))
            except:
                # 缓慢下拉才能加载视频
                for k in range(int(scroll//step)):
                    driver.execute_script('window.scrollBy(0, {})'.format(step))
                    time.sleep(smallwait)
            else:
                for j in range(retry):
                    if j != 0:
                        element = driver.find_element_by_xpath('//*[@id="Pl_Core_NewMixFeed__3"]/div/div[2]/div[{}]'.format(i))
                    if element.get_attribute('class') == 'WB_cardwrap S_bg2':
                        try:
                            more_btn = driver.find_element_by_xpath('//*[@id="Pl_Core_NewMixFeed__3"]/div/div[2]/div[{}]/a'.format(i))
                        except:
                            time.sleep(wait)
                            #print(j,'waiting')
                        else:
                            more_btn.click()
                            time.sleep(sleep_time)
                            #print(j,'sleep')
                    else:
                        #time.sleep(wait)
                        break
    finally:
        end=datetime.datetime.now()
        print(i,' Message Loaded,','Running Time: %s Seconds.'%(end-start))
        return i

#i = load_data(driver)

def crawler_hot_data(driver,length,agents,label=None,retry=3,wait=1):
    '''爬取一次热点数据的代码
    参数：
        driver： 浏览器对象
        length： 加载到的消息个数
        agents： 用于伪造的消息头
        retry=3： 每次爬取失败重新尝试的次数
        wait=1： 等待时间
    返回：
        一个dataframe对象，包含了每条微博的基本信息
    '''
    print('Crawler Data!')
    columns = ['source','mid','key_word','message_type','user_id','user_name','article','like_num','comment_num','retweet_num','timestamp','flag','img_list','video_list','platform','label']
    infomation_list = []
    start=datetime.datetime.now()
    for i in tqdm.tqdm(range(1,length+1)):
        xpath = '//*[@id="Pl_Core_NewMixFeed__3"]/div/div[2]/div[{}]'.format(i)
        flag = True
        for j in range(retry):
            try:
                infos = process_home_message(driver,xpath,headers=agents.get_headers(),label=label)
            except:
                time.sleep(wait)
                flag = False
                continue
            else:
                flag = True
                break
        if j == retry-1 and flag == False:
            print('error,continue!')
            continue
        else:
            infomation_list.append(infos)
    df_datas = pd.DataFrame(infomation_list,columns = columns)
    end=datetime.datetime.now()
    print(df_datas.shape[0],' Message Got,','Running Time: %s Seconds.'%(end-start))
    return df_datas

#df_datas = crawler_hot_data(driver,i,UserAgent())

def save_data(filename,df_datas):
    # 如果文件存在，则合并
    if os.path.exists(filename):
        old_data_df = pd.read_json(filename)
        df_datas = old_data_df.append(df_datas)
    # 重置索引
    df_datas.reset_index(drop=True, inplace=True)
    print(df_datas.shape[0],' data has been saved!')
    json_str = df_datas.to_json(force_ascii=False)
    # 写入
    with open(filename,'w',encoding='utf-8') as f:
        f.write(json_str)


def weibo_hot_crawler(driver,label=None,reload = 5,wait = 3,filename = 'F:\\Datasets\\social-data\\main\\weibodata.json'):
    agents = UserAgent()
    for i in tqdm.tqdm(range(reload)):
        driver.refresh()
        time.sleep(wait)
        # 加载数据
        l = load_data(driver)
        # 爬取数据
        df_datas = crawler_hot_data(driver,l,agents=agents,label=label)
        # 写入数据
        save_data(filename,df_datas)

# /html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/div/ul/li[2]/a/span
#//*[@id="Pl_Discover_TextList__4"]/div/div/div[2]/div/div/ul/li[48]
def crawler_weibo_by_label(driver,retry=3,sleep_time=5):
    #'//*[@id="Pl_Discover_LeftNav__2"]/div/div/div/div[1]/a'
    #//*[@id="Pl_Discover_TextList__6"]/div/div/div[2]/div/div/ul/li[2]/a
    # /html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div/div/ul/li[1]
    # /html/body/div[1]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div/ul/li[6]
    # //*[@id="Pl_Discover_TextList__6"]/div/div/div[2]/div/div/ul/li[6]
    # //*[@id="Pl_Discover_TextList__6"]/div/div/div[2]/div/div/ul/li[43]
    #['社会', '国际', '科技', '科普', '数码', '财经', '股市', '明星', '综艺', '电视剧', '电影', '音乐', '汽车', '体育', '运动健身', '健康', '瘦身', '养生', '军事', '历史', '美女模特', '摄影', '情感', '搞笑', '辟谣', '正能量', '政务', '游戏', '旅游', '育儿', '校园', '美食', '房产', '家居', '星座', '读书', '三农', '设计', '艺术', '时尚', '美妆', '动漫', '宗教', '萌宠', '婚庆', '法律', '舞蹈']
    label_list = [
        "Society", "International", "Technology", "Science", "Digital",
        "Finance", "Stock Market", "Star", "Variety", "TV Drama",
        "Movie", "Music", "Car", "Sports", "Sports Fitness", 
        "Health", "Slimming", "Health", "Military", "History", 
        "Beauty Model", "Photography", "Emotion", "Funny", " Open up rumors", 
        "Positive energy", "Government", "Games", "Tourism", "Parenting", 
        "Campus", "Food", "House", "Home", "Constellation", 
        "Reading", "Three agriculture", "Design", "Art", "Fashion", 
        "Beauty makeup", "Animation", "Religion", "Cute pet", "Wedding", 
        "Law", "Dance"
    ] 
    element_loc_list = ['//*[@id="Pl_Discover_TextList__6"]/div/div/div[2]/div/div/ul/li[{}]'.format(i) for i in range(2,49)]
    for loc,label in zip(element_loc_list,label_list):
        for i in range(retry):
            try:
                label_btn = driver.find_element_by_xpath(loc)
                label_btn.click()
                time.sleep(sleep_time)
            except:
                driver.refresh()
                time.sleep(sleep_time)
                continue
            else:
                break
        weibo_hot_crawler(driver,label=label,reload=1)
    


'''
old_data_df = pd.read_json(filename)
new_df = pd.DataFrame([[None] for i in range(11121)],columns = ['label'])
data = pd.concat([old_data_df,new_df],axis=1)
data = data[columns]

filename = 'F:\\Datasets\\social-data\\main\\weibodata.json'
json_str = data.to_json(force_ascii=False)
# 写入
with open(filename,'w',encoding='utf-8') as f:
    f.write(json_str)

'''
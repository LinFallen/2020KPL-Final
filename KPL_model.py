#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-12-16 10:49:32
# @Author  : Muxiaoxiong
# @email   : xiongweinie@foxmail.com

"""
王者荣耀比赛预测
#2020KPL秋季赛
比赛模型预测
"""
import time
import random

import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from tqdm import tqdm

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"]
#爬取比赛的信息
def spyder():
    headers = {'User-Agent': random.choice(user_agent)}
    # 爬取比赛代号
    schedule=[i for i in range(66028,66148)]  #常规赛
    schedule1=[i for i in range(66652,66664)]  #季后赛
    schedule.extend(schedule1)
    match_list=[]
    for i in tqdm(schedule):
        url='https://www.wanplus.com/schedule/%s.html'%i
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        all_match = soup.find_all('li', status='done')
        for match in all_match:
            matchnum=match['match']
            match_list.append(matchnum)
    df=pd.DataFrame(columns=['match','teama','teamb','label','moneya','moneyb','killa','killb','towera','towerb','bana1','bana2','bana3','bana4','banb1','banb2','banb3','banb4','heroa1','heroa2','heroa3','heroa4','heroa5','herob1','herob2','herob3','herob4','herob5','kdaa1','kdaa2','kdaa3','kdaa4','kdaa5','kdab1','kdab2','kdab3','kdab4','kdab5','moneya1','moneya2','moneya3','moneya4','moneya5','moneyb1','moneyb2','moneyb3','moneyb4','moneyb5','playera1','playera2','playera3','playera4','playera5','playerb1','playerb2','playerb3','playerb4','playerb5'])
    for match in tqdm(match_list):
        url='https://www.wanplus.com/match/%s.html#data'%match
        try:
            result_info=get_match_info(match,headers,url)
            df=df.append(result_info,ignore_index=True)
        except:
            print('爬取失败，可以手动访问https://www.wanplus.com/match/%s.html#data补充'%match)

    df.to_excel('./KPL1.xlsx',index=False)


def get_match_info(match,headers,url):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, 'lxml')
    win=0
    #获得AB队名称
    teama=soup.find('span',class_='tl bssj_tt1').get_text()
    teamb=soup.find('span',class_='tr bssj_tt3').get_text()
    #判断谁赢了
    if '胜' in teama:
        win=1
    else:
        win=0
    teama=teama.replace('胜','').strip()
    teamb=teamb.replace('胜','').strip()
    # #获得金钱数
    summer=soup.find_all('div',class_='bssj_tt')
    moneya=summer[0].find('span',class_='tl').get_text()
    moneyb=summer[0].find('span',class_='tr').get_text()
    # #获得击杀数
    killa=summer[1].find('span',class_='tl').get_text()
    killb=summer[1].find('span',class_='tr').get_text()
    # #获得推塔数
    towera=summer[2].find('span',class_='tl').get_text()
    towerb=summer[2].find('span',class_='tr').get_text()
    # #获得ban位英雄
    ban=soup.find('div',class_='las_box').find_all('img')
    try:
        bana1=ban[0]['alt']
    except:
        bana1=''
    try:
        bana2=ban[1]['alt']
    except:
        bana2=''
    try:
        bana3=ban[2]['alt']
    except:
        bana3=''
    try:
        bana4=ban[3]['alt']
    except:
        bana4=''
    try:
        banb1=ban[4]['alt']
    except:
        banb1=''
    try:
        banb2=ban[5]['alt']
    except:
        banb2=''
    try:
        banb3=ban[6]['alt']
    except:
        banb3=''
    try:
        banb4=ban[7]['alt']
    except:
        banb4=''
    # #获得英雄信息
    hero=soup.find_all('div',class_='bans_tx fl')
    heroa1=hero[0].find_all('a')[1].get_text()
    heroa2=hero[2].find_all('a')[1].get_text()
    heroa3=hero[4].find_all('a')[1].get_text()
    heroa4=hero[6].find_all('a')[1].get_text()
    heroa5=hero[8].find_all('a')[1].get_text()
    herob1=hero[1].find_all('a')[1].get_text()
    herob2=hero[3].find_all('a')[1].get_text()
    herob3=hero[5].find_all('a')[1].get_text()
    herob4=hero[7].find_all('a')[1].get_text()
    herob5=hero[9].find_all('a')[1].get_text()

    # #获得选手信息
    playera1=hero[0].find_all('a')[0].get_text()
    playera2=hero[2].find_all('a')[0].get_text()
    playera3=hero[4].find_all('a')[0].get_text()
    playera4=hero[6].find_all('a')[0].get_text()
    playera5=hero[8].find_all('a')[0].get_text()
    playerb1=hero[1].find_all('a')[0].get_text()
    playerb2=hero[3].find_all('a')[0].get_text()
    playerb3=hero[5].find_all('a')[0].get_text()
    playerb4=hero[7].find_all('a')[0].get_text()
    playerb5=hero[9].find_all('a')[0].get_text()

    # #获得英雄kda
    info=soup.find_all('div',class_='bans_m')
    kdaa1=info[0].find('span',class_='tr').get_text()
    kdaa2=info[1].find('span',class_='tr').get_text()
    kdaa3=info[2].find('span',class_='tr').get_text()
    kdaa4=info[3].find('span',class_='tr').get_text()
    kdaa5=info[4].find('span',class_='tr').get_text()
    kdab1=info[0].find('span',class_='tl').get_text()
    kdab2=info[1].find('span',class_='tl').get_text()
    kdab3=info[2].find('span',class_='tl').get_text()
    kdab4=info[3].find('span',class_='tl').get_text()
    kdab5=info[4].find('span',class_='tl').get_text()

    # #获得英雄金钱
    moneya1=info[0].find_all('span',class_='tr')[1].get_text()
    moneya2=info[1].find_all('span',class_='tr')[1].get_text()
    moneya3=info[2].find_all('span',class_='tr')[1].get_text()
    moneya4=info[3].find_all('span',class_='tr')[1].get_text()
    moneya5=info[4].find_all('span',class_='tr')[1].get_text()
    moneyb1=info[0].find_all('span',class_='tl')[1].get_text()
    moneyb2=info[1].find_all('span',class_='tl')[1].get_text()
    moneyb3=info[2].find_all('span',class_='tl')[1].get_text()
    moneyb4=info[3].find_all('span',class_='tl')[1].get_text()
    moneyb5=info[4].find_all('span',class_='tl')[1].get_text()


    temp={'match':match,'teama':teama,'teamb':teamb,'label':win,'moneya':moneya,'moneyb':moneyb,'killa':killa,'killb':killb,'towera':towera,'towerb':towerb,'bana1':bana1,'bana2':bana2,'bana3':bana3,'bana4':bana4,'banb1':banb1,'banb2':banb2,'banb3':banb3,'banb4':banb4,'heroa1':heroa1,'heroa2':heroa2,'heroa3':heroa3,'heroa4':heroa4,'heroa5':heroa5,'herob1':herob1,'herob2':herob2,'herob3':herob3,'herob4':herob4,'herob5':herob5,'kdaa1':kdaa1,'kdaa2':kdaa2,'kdaa3':kdaa3,'kdaa4':kdaa4,'kdaa5':kdaa5,'kdab1':kdab1,'kdab2':kdab2,'kdab3':kdab3,'kdab4':kdab4,'kdab5':kdab5,'moneya1':moneya1,'moneya2':moneya2,'moneya3':moneya3,'moneya4':moneya4,'moneya5':moneya5,'moneyb1':moneyb1,'moneyb2':moneyb2,'moneyb3':moneyb3,'moneyb4':moneyb4,'moneyb5':moneyb5,'playera1':playera1,'playera2':playera2,'playera3':playera3,'playera4':playera4,'playera5':playera5,'playerb1':playerb1,'playerb2':playerb2,'playerb3':playerb3,'playerb4':playerb4,'playerb5':playerb5}
    return temp



if __name__ == '__main__':
    spyder()

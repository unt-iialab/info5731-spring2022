#!/usr/bin/env python
# encoding: utf-8
'''
@author: haihua
@contact: haihua.chen@unt.edu
@file:review_crawler2.py
@time:  8:58 PM
@desc:

'''
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as BS
import re
import numpy as np
import pandas as pd

def get_tablelist(html,userUrl,pageUrl):
    #print(userUrl)
    user_id=userUrl.replace('/reviews','')[26:].strip()
    #print(user_id)
    html_soup = BS(html, 'html.parser')

    reviews = html_soup.find_all("div", {"class": "lister-item-content"})

    review_details = []

    for review in reviews:
        #print(review)
        movie_title = review.find_all("a", href=True)[0].text.strip()

        movie_id = review.find_all("a", href=True)[0]['href'].split("\n")[0].strip()[7:16]
        #print(movie_id)
        review_title = review.find_all("a", href=True)[1].text.strip()
        #print(review_title)
        review_date = review.find_all("span", {"class": "review-date"})[0].text.strip()
        try:
            review_content = review.find("div", {"class": "text show-more__control"}).text.strip()
        except:
            review_content = review.find("div", {"class": "text show-more__control clickable"}).text.strip()
        #review_content = review.find_all("div", {"class": "text show-more__control clickable"})[0].text.strip()
        #print(review_content)
        try:
            review_helpfullness = review.find("div", {"class": "actions text-muted"}).text.split("\n")[1].strip()
            review_id = review.find_all("a", href=True)[3]['href'].split("\n")[0].strip()[8:16]
        except:
            review_helpfullness =''
            review_id =''
        try:
            review_score = review.find_all("span")[2].text
            review_score = int(review_score)
            review_score = str(review_score)
        except:
            # print("Skip! No review score")
            review_score=''

        review_details.append(
            [pageUrl, user_id, movie_id, movie_title, review_id, review_score, review_date, review_title, review_content,
             review_helpfullness])
    return review_details

# Change the movie review page url here
f = open('/home/iialab/PycharmProjects/openCLIR.unt.edu/yushimovie/urls/userURL2','r')
for line in f:
    base_url = "https://www.imdb.com/"
    key = ""
    line = f.readline()
    print(line.strip())
    res = requests.get(line.strip())
    res.encoding = 'utf-8'
    soup = BS(res.text, 'html.parser')
    #print(res)
    allTablelist=[]
    #soup.select(".lister-list")
    tablelist = get_tablelist(res.text, line, line.strip())
    #print(tablelist)
    for i in tablelist:
        allTablelist.append(i)

    #print(allTablelist)
    load_more = soup.select(".load-more-data")

    flag = True
    if len(load_more):
        #print(load_more)
        ajaxurl = load_more[0]['data-ajaxurl']
        base_url = base_url + ajaxurl + "?ref_=undefined&paginationKey="
        try:
            key = load_more[0]['data-key']
        except KeyError:
            flag = False
    else:
        flag = False

    while flag:
        url = base_url + key
        print("url = ", url)
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BS(res.text, 'html.parser')
        tablelist2 = get_tablelist(res.text, line, url)
        #print(tablelist2)
        for i in tablelist2:
            allTablelist.append(i)

        load_more = soup.select(".load-more-data")
        #print(len(load_more))
        if len(load_more):
            key = load_more[0]['data-key']
            #print(key)
        else:
            flag = False

    user_id = allTablelist[0][1]
    print(user_id)
    data = np.array(allTablelist)
    df = pd.DataFrame(data, columns=['user_url', 'user_id', 'movie_id', 'movie_title', 'review_id', 'review_score', 'review_date',
                                     'review_title', 'review_content', 'review_helpfullness'])
    df.to_csv("all_data_collected_new/" + user_id + ".csv", sep=',', index_label='serial')

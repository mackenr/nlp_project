
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as soupify


#standard imports

import numpy as np



header={'User-Agent': 'hamsandwich'}


def get_blog_urls(base_url):
    soup = soupify(get(base_url, headers=header).content)
    return [link['href'] for link in soup.select('a.more-link')]




def get_blog_content(base_url):
    blog_links = get_blog_urls(base_url)
    all_blogs = []
    for blog in blog_links:
        blog_soup = soupify(
            get(blog,
                headers=header).content)
        blog_content = {'title': blog_soup.select_one(
            'h1.entry-title').text,
        'content': blog_soup.select_one(
            'div.entry-content').text.strip()}
        all_blogs.append(blog_content)
    return all_blogs





def get_cats(base_url):
    soup = soupify(get(base_url).content)
    return [cat.text.lower() for cat in soup.find_all('li')[1:]]

def get_all_shorts(base_url):
    cats = get_cats(base_url)
    all_articles = []
    for cat in cats:
        cat_url = base_url + '/' + cat
        print(get(cat_url))
        cat_soup = soupify(get(cat_url).content)
        cat_titles = [
            title.text for title in cat_soup.find_all('span', itemprop='headline')
        ]
        cat_bodies = [
            body.text for body in cat_soup.find_all('div', itemprop='articleBody')]
        cat_articles = [{'title': title,
        'category': cat,
        'body': body} for title, body in zip(
        cat_titles, cat_bodies)]
        print('cat articles length: ',len(cat_articles))
        all_articles.extend(cat_articles)
        print('length of all_articles: ', len(all_articles))
    return all_articles










def souphtmltags(soup):
    '''    
    
    returns a dictionary which has every indpendent html tag with a set of every possible css tag with respect to the soup you are looking at
    if you wish you coould easily extend this to pull every unique webset listed within a soup
    
    
    '''
    tagset=set()
    attributes_set=set()
    aggtagdict={}

    for tag in soup.findAll(True):
        x=list(tag.attrs.keys())
        c=len(attributes_set)
        attributes_set.update(x)
        d=len(attributes_set)
        a=len(tagset)
        tagset.update([tag.name])
        b=len(tagset)
        if (a!=b) or (c!=d):
            if tag.name in list(aggtagdict.keys()):
                aggtagdict[tag.name].update(x)
            else:
                aggtagdict.update({tag.name:set(x)})

    x=(list(aggtagdict.values()))
    a=set()
    x=list(filter((lambda i:len(i)>0),x))
    for i in x:
        a|=i

    attsdiff=a.symmetric_difference(attributes_set)
    keysetdiff=set(aggtagdict.keys()).symmetric_difference(tagset)

    if len(attsdiff.symmetric_difference(keysetdiff))!=0:
        print('logic error')
    return aggtagdict
   

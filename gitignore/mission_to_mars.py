
# coding: utf-8

# In[39]:


#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import requests


# In[40]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[41]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[42]:


#visiting the page
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
browser.html
news = bs(browser.html,"html.parser")


# In[43]:


list_text = news.find("div", class_="list_text")


# In[44]:


title = list_text.find("a").get_text()


# In[47]:


title


# In[48]:


paragraph = list_text.find("div", class_="article_teaser_body").get_text()


# In[60]:


paragraph


# In[69]:


#visiting the page
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[70]:


time.sleep(2)
image_button = browser.find_by_id("full_image").click()


# In[71]:


time.sleep(2)
more_info_button = browser.find_link_by_partial_text("more info").click()


# In[72]:


image = bs(browser.html, "html.parser")


# In[75]:


image_url=image.find("figure", class_="lede").find("img")["src"]
image_url


# In[77]:


final_url = "https://www.jpl.nasa.gov" + image_url
final_url


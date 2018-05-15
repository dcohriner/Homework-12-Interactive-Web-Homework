
# coding: utf-8

# In[ ]:


#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time
import requests


# In[ ]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[ ]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# # NASA Mars News


# # NASA Mars News

# In[ ]:


#visiting the page
url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)
browser.html
news = bs(browser.html,"html.parser")


# In[ ]:


list_text = news.find("div", class_="list_text")


# In[ ]:


title = list_text.find("a").get_text()


# In[ ]:


title


# In[ ]:


paragraph = list_text.find("div", class_="article_teaser_body").get_text()


# In[ ]:


paragraph


# In[ ]:


#visiting the page
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[ ]:


time.sleep(2)
image_button = browser.find_by_id("full_image").click()


# In[ ]:


time.sleep(2)
more_info_button = browser.find_link_by_partial_text("more info").click()


# In[ ]:


image = bs(browser.html, "html.parser")


# In[ ]:


image_url=image.find("figure", class_="lede").find("img")["src"]
image_url


# In[ ]:


final_url = "https://www.jpl.nasa.gov" + image_url
final_url


# # JPL Mars Space Images - Featured Image

# In[ ]:


url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
browser.visit(url_image)


# In[ ]:


#Getting the base url
from urllib.parse import urlsplit
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
print(base_url)


# In[ ]:


#Design an xpath selector to grab the image#Design 
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"


# In[ ]:


#Use splinter to click on the mars featured image
#to bring the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()


# In[ ]:


#get image url using BeautifulSoup
html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", class_="fancybox-image")["src"]
full_img_url = base_url + img_url
print(full_img_url)


# # Mars Weather

# In[ ]:


#get mars weather's latest tweet from the website
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)


# In[ ]:


html_weather = browser.html
soup = bs(html_weather, "html.parser")
#temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)
#temp


# # Mars Facts

# In[ ]:


url_facts = "https://space-facts.com/mars/"


# In[ ]:


table = pd.read_html(url_facts)
table[0]


# In[ ]:


df_mars_facts = table[0]
df_mars_facts.columns = ["Parameter", "Values"]
df_mars_facts.set_index(["Parameter"])


# In[ ]:


mars_html_table = df_mars_facts.to_html()
mars_html_table = mars_html_table.replace("\n", "")
mars_html_table


# # Mars Hemisperes

# In[ ]:


url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)


# In[ ]:


#Getting the base url
hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
print(hemisphere_base_url)


# # Cerberus-Hemisphere-image-url

# In[ ]:


hemisphere_img_urls = []
results = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[1]/a/img").click()
time.sleep(2)
cerberus_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
cerberus_image = browser.html
soup = bs(cerberus_image, "html.parser")
cerberus_url = soup.find("img", class_="wide-image")["src"]
cerberus_img_url = hemisphere_base_url + cerberus_url
print(cerberus_img_url)
cerberus_title = soup.find("h2",class_="title").text
print(cerberus_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
cerberus = {"image title":cerberus_title, "image url": cerberus_img_url}
hemisphere_img_urls.append(cerberus)


# # Schiaparelli-Hemisphere-image-url

# In[ ]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[2]/a/img").click()
time.sleep(2)
schiaparelli_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
schiaparelli_image = browser.html
soup = bs(schiaparelli_image, "html.parser")
schiaparelli_url = soup.find("img", class_="wide-image")["src"]
schiaparelli_img_url = hemisphere_base_url + schiaparelli_url
print(schiaparelli_img_url)
schiaparelli_title = soup.find("h2",class_="title").text
print(schiaparelli_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
schiaparelli = {"image title":schiaparelli_title, "image url": schiaparelli_img_url}
hemisphere_img_urls.append(schiaparelli)


# # Syrtis Major Hemisphere

# In[ ]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[3]/a/img").click()
time.sleep(2)
syrtis_major_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
syrtis_major_image = browser.html
soup = bs(syrtis_major_image, "html.parser")
syrtis_major_url = soup.find("img", class_="wide-image")["src"]
syrtis_major_img_url = hemisphere_base_url + syrtis_major_url
print(syrtis_major_img_url)
syrtis_major_title = soup.find("h2",class_="title").text
print(syrtis_major_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
syrtis_major = {"image title":syrtis_major_title, "image url": syrtis_major_img_url}
hemisphere_img_urls.append(syrtis_major)


# # Valles Marineris Hemisphere

# In[ ]:


results1 = browser.find_by_xpath( "//*[@id='product-section']/div[2]/div[4]/a/img").click()
time.sleep(2)
valles_marineris_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
time.sleep(1)
valles_marineris_image = browser.html
soup = bs(valles_marineris_image, "html.parser")
valles_marineris_url = soup.find("img", class_="wide-image")["src"]
valles_marineris_img_url = hemisphere_base_url + syrtis_major_url
print(valles_marineris_img_url)
valles_marineris_title = soup.find("h2",class_="title").text
print(valles_marineris_title)
back_button = browser.find_by_xpath("//*[@id='splashy']/div[1]/div[1]/div[3]/section/a").click()
valles_marineris = {"image title":valles_marineris_title, "image url": valles_marineris_img_url}
hemisphere_img_urls.append(valles_marineris)


# In[ ]:


hemisphere_img_urls


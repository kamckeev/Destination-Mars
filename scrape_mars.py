from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    return Browser("chrome", headless=False)

def scrape():
    browser=init_browser()
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=bs(html,'html.parser')
    news_p=soup.find('div', class_='article_teaser_body').get_text()
    news_title=soup.find('div', class_='content_title').get_text()

    #image scraping
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(1)

    html=browser.html
    soup=bs(html, 'html.parser')

    base_url='https://www.jpl.nasa.gov'
    featured_image=soup.find('a', id='full_image').get('data-fancybox-href')
    featured_image_url=base_url+featured_image
    
    #weather scraping
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(1)

    html=browser.html
    soup=bs(html, 'html.parser')

    mars_weather=soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    remove_twitterlink=mars_weather.find('a')
    remove_twitterlink.extract()
    mars_weather=mars_weather.text
    
    #facts scraping
    url='https://space-facts.com/mars/'
    facts_table = pd.read_html(url)
    facts_df=facts_table[0]
    facts_df=facts_df.rename(columns={0:'Description',1:'Value'})
    facts_df=facts_df.set_index("Description")
    facts_html=facts_df.to_html()
    facts_html=facts_html.replace('\n', '')
    facts_df
    
    # #hemisphere scraping
    hemispheres=[]
    #finding all image pages
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html=browser.html
    soup=bs(html, 'html.parser')
    pages=soup.find_all('div', class_='item')
    #looping through pages
    base_url='https://astrogeology.usgs.gov/'
    for page in pages:
        pic_url=page.find('a').get('href')
        full_page_url=base_url+str(pic_url)
        browser.visit(full_page_url)
        time.sleep(1)
        html=browser.html
        soup=bs(html,'html.parser')
        image_url=soup.find('img',class_='wide-image').get('src')
        full_image_url=base_url+str(image_url)
        title=soup.find('h2',class_='title').get_text()
        hemi_dict={}
        hemi_dict['title']=title
        hemi_dict['img_url']=full_image_url
        hemispheres.append(hemi_dict)

        
    #creating dictionary
    scrape_dict={}
    scrape_dict['latest_headline']=news_title
    scrape_dict['latest_article']=news_p
    scrape_dict['featured_image']=featured_image_url
    scrape_dict['weather']=mars_weather
    scrape_dict['facts_table']=facts_html
    scrape_dict['hemispheres']=hemispheres

    #close browser
    browser.quit()
    return scrape_dict


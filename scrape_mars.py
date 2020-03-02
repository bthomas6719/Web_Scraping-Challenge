# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# import dependencies

import requests
import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


# %%
# open chrome driver browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # %% [markdown]
    # Latest Mars News from NASA

    # %%
    # define url
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    # create beautiful soup object 
    html = browser.html
    soup = bs(html, 'html.parser')


    # %%
    # find the first news title

    news_title = soup.body.find("div", class_="content_title").text
    # find the paragraph associated with the first title
    news_paragraph = soup.body.find("div", class_="article_teaser_body").text
    # close the browser
    print(f"The title is: \n{news_title}")
    print()
    print(f"The paragraph is:  \n{news_paragraph}")

    # %% [markdown]
    # Mars Images

    # %%
    # define the url and visit it with browser
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)


    # %%
    #Click on the the button to get to the full image
    image_full=browser.find_by_id('full_image')
    image_full.click()
    time.sleep(5)
    browser.click_link_by_partial_text('more info')


    # %%
    #find the image url to the full size
    html_image = browser.html
    soup = bs(html_image, 'html.parser')


    # %%
    #Retrieve image from style tag/scrape url
    img_url = soup.find('img', class_ = 'main_image')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + img_url
    print(featured_image_url)

    # %% [markdown]
    # Weather-MARS

    # %%
    # Visit Twitter url for latest Mars Weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Extract latest tweet
    tweet_text_container = soup.find('div', class_="js-tweet-text-container")
    print(tweet_text_container)
    # Loop through latest tweets and find the tweet that has weather information
    
    mars_weather = tweet_text_container
    print(mars_weather)

    # %% [markdown]
    # Mars Facts

    # %%
    # define url
    mars_facts_url = "https://space-facts.com/mars/"
    # read html into pandas
    tables = pd.read_html(mars_facts_url)

    # convert to a dataframe and clean up 
    df1 = tables[0]
    df1.columns = ["Description", "Value"]

    df1


    # %%
    # convert to html table
    mars_facts_html=df1.to_html()
    mars_facts_html


    # %%


    # %% [markdown]
    # Mars Hemispheres

    # %%
    # define url and open in browser
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    # %% [markdown]
    # Sciaperelli Hemishere

    # %%
    # define url and open in browser
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    # Print image title and url
    print(hemisphere_image_urls)

    # %% [markdown]
    # Dictionaries for hemispheres

    # %%
    mars_data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image_url": featured_image_url,
            "current_weather": mars_weather,
            "mars_facts": mars_facts_html,
            "hemisphere_image_urls": hemisphere_image_urls
    }


    # %%
    browser.quit()
    return mars_data
    

    # %%

if __name__ == '__main__':
    scrape()


# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time #sleep 5 second after browser.visit commands to insure that the browser has loaded

# Create Dictionary to collect all of the data
mars= {}

# Define Function Scrape
def scrape():
    
    # Define Function for opening browser
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)

    # # NASA Mars News
    # Visit Nasa news url through splinter module
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)

    # Parse HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')


    # Scrape (https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Add Data
    mars['news_title'] = news_title
    mars['news'] = news_p


    # # JPL Mars Space Images - Featured Image
    # Specify url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Parse HTML Object 
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # Retrieve background-image url from style tag 
    image = soup.find('article', class_='carousel_item')['style']
    featured_image_url =image.split("'")[1]

    # Concatinate base and relative url
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + featured_image_url
    mars['featured_image_url'] = featured_image_url 


    # # Mars Weather
    # Specify url
    url = 'https://twitter.com/marswxreport?lang=en'

    # Parse HTML Object 
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # Find all elements that contain tweets
    tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Search through tweets
    for tweet in tweets: 
        mars_weather = tweet.find('p').text
    
        # exclude non weather related tweets
        if 'high' and 'pressure' in mars_weather:
            # Seperate the link from the tweet and reformate
            weather=tweet.find('p')
            link=weather.find('a').extract()
            break
        else: 
            pass
    
    # Store weather text
    mars['weather']=weather.text
    mars['weather_link']=link.text


    # # Mars Facts
    # Visit the mars facts site and parse
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    # Find Mars Facts DataFrame and assign comlumns
    df = tables[0]
    df.columns = ['Description', 'Value']

    # Convert to HTML and Store
    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
    mars['table']=html_table


    # # Mars Hemispheres



    # Specify url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Parse HTML Object 
    response = requests.get(url)
    soup=bs(response.text, 'lxml')
    
    # Find items
    items=soup.find_all('div',class_='item')

    # initialize url list
    hemisphere_image_urls = []

    # Store the base ul 
    base_url = 'https://astrogeology.usgs.gov'

    for i in items: 
        # Store title and link
        title = i.find('h3').text
        relative_url=i.find('a', class_='itemLink product-item')['href']
        
        # Parse HTML Object for each hemisphere
        url=base_url + relative_url
        response = requests.get(url)
        soup = bs(response.text, 'lxml')
        
        # find image source and add to dict
        relative_img_url=soup.find('img', class_='wide-image')['src']
        img_url = base_url +relative_img_url
        
        # Add dict to list
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # store hemisphere_image_urls
    mars['hemisphere_image_urls']= hemisphere_image_urls

    # Return data and quit broswer
    return mars
    browser.quit()






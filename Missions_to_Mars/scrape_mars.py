# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time #sleep 5 second after browser.visit commands to insure that the browser has loaded

def init_browser():
    # Define Function for opening browser
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)

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
    # Visit Specified URL
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    time.sleep(5)

    # Parse HTML Object 
    html_image = browser.html
    soup = bs(html_image, "html.parser")

    # base URL
    main_url = "https://www.jpl.nasa.gov"

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Concatenate URLs and store final
    featured_image_url = main_url + featured_image_url
    mars['featured_image_url'] = featured_image_url 


    # # Mars Weather
    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)

    # Parse HTML Object 
    html_weather = browser.html
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    tweets = soup.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in tweets: 
        mars_weather = tweet.find('span').text
        if 'high' and 'pressure' in mars_weather:
            break
        else: 
            pass
    
    # Store weather text
    mars['weather']=mars_weather


    # # Mars Facts
    # Visit the mars facts site and parse
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(5)
    tables = pd.read_html(url)

    # Find Mars Facts DataFrame and assign comlumns
    df = tables[0]
    df.columns = ['Description', 'Value']

    # Convert to HTML and Store
    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
    mars['table']=html_table


    # # Mars Hemispheres
    # Visit USGS Astrogeology site 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(5)

    # Parse HTML Object
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # initialize url list
    hemisphere_image_urls = []

    # Store the base ul 
    base_url = 'https://astrogeology.usgs.gov'

    # Loop through the items
    for i in items: 
        # Store title and link
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(base_url + partial_img_url)
        time.sleep(5)
    
        # Parse HTML Object for each hemisphere
        hemi_img_html = browser.html
        soup = bs(hemi_img_html, 'html.parser')
    
        # find image source and add to list
        img_url = base_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # store hemisphere_image_urls
    mars['hemisphere_image_urls']= hemisphere_image_urls

    # Return data and quit broswer
    return mars
    browser.quit()






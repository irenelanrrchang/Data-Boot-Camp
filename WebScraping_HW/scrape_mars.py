
# In[1]:



# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


    # In[2]:
def scrape ():

    # Mars NEWs
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)


    # In[3]:


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    articles = soup.find_all('div', class_='list_text')

    # Iterate through each news
    for article in articles:
            
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            # Collect the latest News Title and Paragragh Text. Assign the text to variables that can be referenced
            news_p = article.find ('div', class_='article_teaser_body').text
        
            link = article.find('a')
            href = link['href']
            news_title = link.text
            print('-----------')
            print(news_title)
            print('...........')
            print(news_p)
            print('https://mars.nasa.gov/' + href)


    # In[4]:


    # Use splinter to navigate JPL and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[5]:


    url ='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # In[6]:


    # browser.click_link_by_id('full image')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)


    # In[7]:


    browser.click_link_by_partial_text('more info')


    # In[8]:


    link = browser.find_link_by_partial_href("/spaceimages/images/largesize/")


    # In[9]:


    featured_image_url = link["href"]
    featured_image_url


    # In[10]:


    # Mars Weather Twitter account
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport'
    browser.visit(url)


    # In[11]:


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # In[12]:


    # Scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.
    news = soup.find_all('div', class_= "js-tweet-text-container")
    for a_news in news:   
        mars_weather = a_news.find('p', class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        print('-----------')
        print(mars_weather)


    # In[13]:


    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://space-facts.com/mars/'
    # Use Pandas to convert the data to a HTML table string`
    tables = pd.read_html(url)
    tables


    # In[14]:


    df = tables [0]
    df


    # In[15]:


    html = df.to_html(index=False)
    html


    # In[16]:


    fact_html = html.replace("\n", "")
    fact_html


    # In[17]:


    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # Define a function to get img_url and title
    def hemisphere_info():
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        # HTML object
        html = browser.html 
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        individual_links= soup.find_all('div', class_= "description")
        
        title_list =[]
        link_list = []
        
        # Make a for loop to get hemisphere title
        for individual_link in individual_links:
            link = individual_link.a["href"]
            href = "https://astrogeology.usgs.gov/" + link
            link_list.append(href)
        
            title= individual_link.h3.text
            clean_title = title.replace("Enhanced", "")
            title_list.append(clean_title)
        
        hemisphere_img_urls = []
        dic ={}
        
        # Make a for loop to get hemisphere_img_url 
        for i in range (len(link_list)):
                executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
                browser = Browser('chrome', **executable_path, headless=False)
                url = link_list[i]
                browser.visit(url)
                image_link = browser.find_link_by_text("Sample")
                full_image = image_link["href"]
                
                # Create a render list of dictionary for future html
                dic= {
                    "title_list": title_list[i],
                    "hemisphere_img_url" : full_image,
                    
                    }
                hemisphere_img_urls.append(dic)
        
        return hemisphere_img_urls


    

    scrape_info= {"news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_img_urls" : hemisphere_img_urls,
        "fact_html" : fact_html
                    }
    return scrape_info
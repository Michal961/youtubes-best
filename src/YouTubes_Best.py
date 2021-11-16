from selenium import webdriver
from selenium.webdriver.common.by import By
import Configuration
import time 
import csv
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC


class YouTubes_Best:
    """
        A class used to get the data of the 10 All-Time Most Viewed Music Videos
        from YouTube by using web scraping with selenium.
        (from YouTube Records page and not by YouTube Data API)
        

        Attributes
        ----------
            links : dictionary
                a dictionary to store the links of the songs
                {inex(rank) : url_link}

            data : dictionary
                a dictionary to store the data from each song
                {inex: {'rank': , 'name': , 'date': , 'views': , 'likes': ,
                        'dislikes': , 'comments': , 'channel': , 'subscribers': }}
            
        Methods
        -------
            get_links():
                Returns the dictionary of links

            get_data()
                Returns the dictionary of data

            make_file(file_name='best_ten'):
                file_name - the name of the file (default best_ten)
                Creates a CSV file from the data dictionary


    """


    __links={}
    __data={}

    def __init__(self):
        
        # driver initialization
        driver = webdriver.Chrome(Configuration.DRIVER_PATH)
        driver.get(Configuration.URL)
        time.sleep(3) # or by WebDriverWait

        #find and store the url's
        for i in range(1,11):
            self.__links[i]=driver.find_element(By.XPATH,'//*[@id="id-drawer-index-1-0"]/ul[2]/li['+str(i)+']/a').get_attribute("href")
        print(self.__links)


        for i in range(1,11):
            temp={}
            temp['rank']=i
            #switch to the page of the song:
            driver.get(self.__links[i])
            time.sleep(3) # or by WebDriverWait

            #stop the music
            play=driver.find_element(By.CSS_SELECTOR,'#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button')
            play.click()
            driver.execute_script("arguments[0].setAttribute('disabled','true')", play)
            
            #scroll dowen to load the rest of the page (or by wait)
            driver.execute_script("window.scrollTo(0, 600);")
            time.sleep(3) #load - or by WebDriverWait
            
            #get the relevant data and store it
            name=driver.find_element(By.CSS_SELECTOR,'#container > h1 > yt-formatted-string').text
            temp['name']=name
            date=driver.find_element(By.CSS_SELECTOR,'#info-strings > yt-formatted-string').text
            temp['date']=date
            views=int(driver.find_element(By.CSS_SELECTOR,'#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer').text.split()[0].replace(",",''))
            temp['views']=views
            likes=int(driver.find_element(By.XPATH,'//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[1]/a/yt-formatted-string').get_attribute("aria-label").split(" ")[0].replace(",",''))
            temp['likes']=likes
            dislikes=int(driver.find_element(By.XPATH,'//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[2]/a/yt-formatted-string').get_attribute("aria-label").split(" ")[0].replace(",",''))
            temp['dislikes']=dislikes
            comments = int(driver.find_element(By.XPATH,'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]').text.replace(",",''))
            temp['comments']=comments
            channel=driver.find_element(By.CSS_SELECTOR,'#text > a').text
            temp['channel']=channel                                  
            subscribers=int(float(driver.find_element(By.CSS_SELECTOR,'#owner-sub-count').text.split(" ")[0].replace("M",''))*100000)
            temp['subscribers']=subscribers
            self.__data[i]=temp

        #close
        driver.quit()

    def get_links(self):
        """
        returns the links dictionary

        """
        return self.__links

    def get_data(self):
        """
        returns the data dictionary

        """
        return self.__data

    def make_file(self, file_name='best_ten'):
        """
        file_name - the name of the file (default best_ten)
        
        Creates a CSV file from the data dictionary

        """
        with open(file_name+'.csv', 'w', encoding='utf_8', newline='') as f: 
            w = csv.DictWriter(f, self.__data[1].keys())
            w.writeheader()
            for i in self.__data:
                    w.writerow(self.__data[i])

        

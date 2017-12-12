# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 16:37:47 2017

@author: Renuka

Description: save user profile page for all the users who have submitted reviews
"""

import time
import os.path
import requests
import csv

def grabUser(name,url):
    pageNum=1 # number of pages to collect,we are just collecting a single page
    userid=url.replace('/user_details?userid=','')
    for p in range(1,pageNum+1): # for each page 
        print ('again page',p)
        pageLink="https://www.yelp.com"+url
        with open(os.path.join('users',userid+".html"), "wb") as review_page:
            html=None
            
            print(pageLink)
            for i in range(5): # try 5 times
                try:
                    response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html=response.content # get the html
                    break # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print ('failed attempt',i)
                    time.sleep(2) # wait 2 secs
				
		
            if not html:continue # couldnt get the page, ignore
            time.sleep(2)
            #save user profile page
            review_page.write(html)
            review_page.close()


if __name__=='__main__':
    try:
        os.mkdir("users")
    except Exception:
        pass    	
    #for every user who has submitted review
    with open('Reviews.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name']!='NA':
                grabUser(row['Name'],row['Link'])
    
            

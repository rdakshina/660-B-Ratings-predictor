# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 19:46:22 2017

@author: Renuka

Description: This scrapes and saves html files for all other establishments the user has given reviews for
"""
import time
import os.path
import requests
import csv

def scrapeRest(Rname,uid,url):
    restId=url.replace('/biz/','')#get restaurant id
    #save html files under subfolder
    with open(os.path.join('others',uid+'__'+restId+ ".html"), "wb") as review_page:
        html=None
        pageLink="https://www.yelp.com"+url # url for page 1
        print(pageLink)
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 sec
        time.sleep(2)
        #save the html
        review_page.write(html)
        review_page.close()
   
if __name__=='__main__':
    try:
        os.mkdir("others")
    except Exception:
        pass    	
    with open('Ofile.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name']!='NA':
                scrapeRest(row['Restaurant'],row['Userid'],row['Link'])



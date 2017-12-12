# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:40:42 2017

@author: Renuka

Description: This extracts reviews from the html files saved for all the restaurants in our list
"""

from bs4 import BeautifulSoup
import re
import csv

import os.path

def extractRating(url,Rname):
    pageNum=10 # number of pages to collect reviews from for each restaurant
    
    address=str(os.getcwd())+'\\'+Rname+'\\'
    
    for p in range(1,pageNum+1): # for each page of the restaurant
        print ('again page',p)
        review_page=open(address+'/'+str(p)+'.html','rb')
        html=review_page.read()
        #apply beautiful soup to decode the html
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        
        #extract restaurant average rating
        top=soup.find('div',{'class':re.compile('i-stars--large')})
        avg=top.get('title')
        
        #find all the reviews in the page
        names=soup.findAll('div', {'class':re.compile('review--with-sidebar')}) # get all the review divs,re:compile does partial match
        #we are given an iterator to the results
        for name in names:

            critic,location,rating,link='NA','NA','NA','NA'
            
            #find this user/critic's name
            criticChunk=name.find('a',{'class':re.compile('user-display-name')})
            if criticChunk:
                critic1=criticChunk.text
                critic=critic1.replace('\n','')
                link=criticChunk.get('href')
                
            #find this user/critic's location  
            locChunk=name.find('li',{'class':re.compile('user-location')})
            if locChunk:
                location1=locChunk.text
                location=location1.replace('\n','')
            
            #find the rating given by this user
            ratingChunk=name.find('div',{'class':re.compile('i-stars')})
            if ratingChunk:
                rating=ratingChunk.get('title')
            
            #write the review to Reviews.csv
            writer.writerow({'Restaurant': Rname,'Name':critic, 'Location':location, 'Avg_Rest_Rating':avg,'Rating':rating, 'Link':link})    
    				
        review_page.close()

def extract(fRestuarant,fLinks):
    #read restaurant names and links
    lines=open(fRestuarant,'r').readlines()
    words=open(fLinks,'r').readlines()
    i=0
    #for each restaurant
    for word in words:
        extractRating(word,lines[i].strip())
        i+=1
    
if __name__=='__main__':
    csvfile=open('Reviews.csv','w')
    fieldnames = ['Restaurant','Name', 'Location','Avg_Rest_Rating','Rating','Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    extract("names.txt","links.txt")
    csvfile.close()

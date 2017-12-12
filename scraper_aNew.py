# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:37:43 2017

@author: Renuka

Description: Find top 50 American (New) restaurants in Boston and save their first 10 review pages as html files
"""

from bs4 import BeautifulSoup
import re
import time
import os.path
import requests

def run(url):

    pageNum=5 # number of pages to search results to collect
    fn=open('names.txt','w')# output file
    fl=open('links.txt','w')# output file
    for p in range(1,pageNum+1): # for each page 
        print ('page',p)
        html=None
        end=(p-1)*10 
        if p==1: pageLink=url # url for page 1
        #modify url to match the url pattern used by yelp and access consecutive pages
        else: pageLink=url+'&start='+str(end)
        print(pageLink)# make the page url
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
        if not html:continue  # couldnt get the page, ignore

        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html ,lxml indicates the type of data(webpage)

        names=soup.findAll('span', {'class':re.compile('indexed-biz-name')}) # get all the review divs,re:compile does partial match
        #dictionary for the second filter where we extract only class indexed-biz-name
        #we are given an iterator to the results
        for name in names:

            restaurant,link='NA','NA' # initialize restaurant and link  
            temp=name.text
            #clean restaurant name
            splitted = re.split(r'\s{2,}', temp)
            restaurant=splitted[1]
            
            link_chunk=name.find('a',{'href':re.compile('/biz/')})
            if link_chunk:   
                link=link_chunk.get('href')#.encode('ascii','ignore')
                
            #save restaurant name and links in separate files
            fn.write(restaurant)
            fl.write(link+'\n')

    fn.close()
    fl.close()
 
def scrape(url,name):
    pageNum=10 # number of pages to collect for each restaurant
    try:
        os.mkdir(name)#create directory with restaurant name
    except Exception:
        pass    	
    for p in range(1,pageNum+1): # for each page 
        print ('again page',p)
        #save review pages as <<pagenumber>>.html
        with open(os.path.join(name, str(p) + ".html"), "wb") as review_page:
            html=None
            if p==1: pageLink="https://www.yelp.com"+url # url for page 1
            else:
                URL=url.replace("osq=American+%28New%29\n","start=")
                #replace with "osq=American+%28Traditional%29\n" for american (Traditional) restaurants
                rpage=(p-1)*20
                #modify url to match the url pattern used by yelp and access consecutive pages
                pageLink= "https://www.yelp.com"+URL+str(rpage)
                print(pageLink)
            for i in range(5): # try 5 times
                try:
                    #use the browser to access the url
                    response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html=response.content # get the html
                    break # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print ('failed attempt',i)
                    time.sleep(2) # wait 2 secs
				
		
            if not html:continue # couldnt get the page, ignore
            time.sleep(2)
            #save the html file
            review_page.write(html)
            review_page.close()

def extract(fRestuarant,fLinks):
    #open saved restaurant names and links
    lines=open(fRestuarant,'r').readlines()
    words=open(fLinks,'r').readlines()
    i=0
    #scrape review pages for each restaurant
    for word in words:
        scrape(word,lines[i].strip())
        i+=1
    
if __name__=='__main__':
    url="https://www.yelp.com/search?find_desc=American+%28New%29&find_loc=Boston%2C+MA&ns=1"
    #replace "https://www.yelp.com/search?find_desc=American+(Traditional)&find_loc=Boston,+MA" for american (Traditional) restaurants
    run(url)
    extract("names.txt","links.txt")


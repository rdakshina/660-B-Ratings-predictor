# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 20:22:42 2017

@author: Renuka

Description: Extract other establishment's average rating
"""

from bs4 import BeautifulSoup
import re
import csv

import os.path

def extractRest(Rname,Uname,uid,location,rating,avgU,url):   
    address=str(os.getcwd())+'\\others\\'
    rest=url.replace('/biz/','')
    review_page=open(address+'/'+uid+"__"+rest+'.html','rb')
    html=review_page.read()
    #apply beautiful soup to decode the html
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
    avg='NA'
    
    #extract average rating for the other establishment
    top=soup.find('div',{'class':re.compile('i-stars--large')})
    if top:
        avg=top.get('title')
          
    writer.writerow({'Restaurant': Rname,'Name':Uname, 'Userid':uid, 'Location':location, 'Avg_Rest_Rating':avg,'Rating':rating, 'Avg_User_rating':avgU, 'Link':url})    			
    review_page.close()

    
if __name__=='__main__':
    Ffile=open('OFinal.csv','w')
    fieldnames = ['Restaurant','Name','Userid', 'Location','Avg_Rest_Rating','Rating','Avg_User_rating','Link']
    writer = csv.DictWriter(Ffile, fieldnames=fieldnames)
    writer.writeheader()
    
    #For each of the other establishment get the average rating
    with open('Ofile.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name']!='NA':
                extractRest(row['Restaurant'],row['Name'],row['Userid'],row['Location'],row['Rating'],row['Avg_User_rating'],row['Link'])
    csvfile.close()
    Ffile.close()

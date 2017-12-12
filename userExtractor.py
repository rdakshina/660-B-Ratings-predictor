# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:40:42 2017

@author: Renuka

Description: Extract User average rating and other reviews submitted by the user
"""

from bs4 import BeautifulSoup
import re
import csv
import os.path

def extractUser(Rname,Uname,location,avg,rating,link):
    pageNum=1 # number of pages to collect
    star1_rating,star2_rating,star3_rating,star4_rating,star5_rating,avg_star_rating='NA','NA','NA','NA','NA','NA'
    
    #extract user id from user profile link
    userid=link.replace('/user_details?userid=','')
    address=str(os.getcwd())+'\\users\\'
    for p in range(1,pageNum+1): # for each page 
        print ('again page',p)
        review_page=open(address+'/'+userid+'.html','rb')
        
        #read saved html file and apply beautiful soup
        html=review_page.read()
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        
        #calculate average user rating using histogram on user profile
        hist1=soup.find('tr', {'class':re.compile('histogram_row--5')})
        if hist1:
            star1_ratingChunk=hist1.find('td',{'class':'histogram_count'})
            if star1_ratingChunk:
                star1_rating=star1_ratingChunk.text
        
        
        hist2=soup.find('tr', {'class':re.compile('histogram_row--4')})
        if hist2:
            star2_ratingChunk=hist2.find('td',{'class':'histogram_count'})
            if star2_ratingChunk:
                star2_rating=star2_ratingChunk.text
        
        hist3=soup.find('tr', {'class':re.compile('histogram_row--3')})
        if hist3:
            star3_ratingChunk=hist3.find('td',{'class':'histogram_count'})
            if star3_ratingChunk:
                star3_rating=star3_ratingChunk.text
        
        hist4=soup.find('tr', {'class':re.compile('histogram_row--2')})
        if hist4:
            star4_ratingChunk=hist4.find('td',{'class':'histogram_count'})
            if star4_ratingChunk:
                star4_rating=star4_ratingChunk.text
        
        hist5=soup.find('tr', {'class':re.compile('histogram_row--1')})
        if hist5:
            star5_ratingChunk=hist5.find('td',{'class':'histogram_count'})
            if star5_ratingChunk:
                star5_rating=star5_ratingChunk.text
        
        if star1_rating!='NA':
            total_star_rating=(int(star5_rating)*5)+(int(star4_rating)*4)+(int(star3_rating)*3)+(int(star2_rating)*2)+(int(star1_rating)*1)
            total_count=int(star5_rating)+int(star4_rating)+int(star3_rating)+int(star2_rating)+int(star1_rating)
            avg_star_rating=total_star_rating/total_count
            writer.writerow({'Restaurant': Rname,'Name':Uname, 'Userid':userid, 'Location':location, 'Avg_Rest_Rating':avg,'Rating':rating,'Avg_User_rating':avg_star_rating,'Link':link})    
        
        names=soup.findAll('div', {'class':('review')})
        #dictionary for the second filter where we extract only class review
        #we are given an iterator to the results
        
        for name in names:
            Oname,Olink,Orating='NA','NA','NA'
            check=0
            biznameChunk=name.find('a',{'class':re.compile('biz-name')}) #re:compile does partial match
            if biznameChunk:
                Oname=biznameChunk.text
                Olink=biznameChunk.get('href')
                
            ratingChunk=name.find('div',{'class':re.compile('i-stars--regular')})
            if ratingChunk:
                Orating=ratingChunk.get('title')
                words=open('names.txt','r').readlines()
                #check if establishment belongs to our list of restaurants
                for word in words:
                    if word==Oname:check=1
                if check==0:
                    Owriter.writerow({'Restaurant': Oname,'Name':Uname,'Userid':userid, 'Location':location, 'Avg_Rest_Rating':'NA','Rating':Orating,'Avg_User_rating':avg_star_rating,'Link':Olink})    
        
        review_page.close()
            
    
if __name__=='__main__':
    Ffile=open('Final.csv','w')#data for our list of restaurants
    Ofile=open('Ofile.csv','w')#data for other establishments that each user has submitted review for
    fieldnames = ['Restaurant','Name','Userid', 'Location','Avg_Rest_Rating','Rating','Avg_User_rating','Link']
    writer = csv.DictWriter(Ffile, fieldnames=fieldnames)
    Owriter=csv.DictWriter(Ofile, fieldnames=fieldnames)
    writer.writeheader()
    Owriter.writeheader()
    #for every user who has submitted review
    with open('Reviews.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name']!='NA':
                extractUser(row['Restaurant'],row['Name'],row['Location'],row['Avg_Rest_Rating'],row['Rating'],row['Link'])
    csvfile.close()
    Ffile.close()

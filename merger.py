# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 16:17:52 2017

@author: Renuka

Description: Simple program to clean and merge the csv files
"""

import csv

#merge the csv files
def merger():
    
    with open('Final.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name']!='NA':
                    writer.writerow({'Restaurant': row['Restaurant'],'Name':row['Name'], 'Userid':row['Userid'], 'Location':row['Location'], 'Avg_Rest_Rating':row['Avg_Rest_Rating'],'Rating':row['Rating'],'Avg_User_rating':row['Avg_User_rating']})
    csvfile.close()
    with open('OFinal.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name']!='NA':
                    writer.writerow({'Restaurant': row['Restaurant'],'Name':row['Name'], 'Userid':row['Userid'], 'Location':row['Location'], 'Avg_Rest_Rating':row['Avg_Rest_Rating'],'Rating':row['Rating'],'Avg_User_rating':row['Avg_User_rating']})
    csvfile.close()
        
if __name__=='__main__':
    Cfile=open('Cleaned_file.csv','w')
    fieldnames = ['Restaurant','Name','Userid', 'Location','Avg_Rest_Rating','Rating','Avg_User_rating']
    writer = csv.DictWriter(Cfile, fieldnames=fieldnames)
    writer.writeheader()
    merger()
    Cfile.close()
    
#remove duplicates
from more_itertools import unique_everseen
with open('Cleaned_file.csv','r') as f, open('Clean.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
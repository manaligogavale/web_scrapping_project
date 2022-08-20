from pickle import FALSE
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

# Create webscrapper function
def webscrapper():
    allurls=[]                                                      # to store all urls
    all_data=[]                                                     # create a list to append the dictionary
    baseurl="https://www.timesjobs.com/candidate/job-search.html?from=submit&searchType=Home_Search&luceneResultSize=25&postWeek=60&cboPresFuncArea=35&pDate=Y&sequence=&startPage=1"
    # create loop to pagination
    for val in range(1,51):     
        allurls.append(baseurl[0:155]+str(val)+baseurl[155:])

    #to convert data string into html using beautifulsoup
    for url in allurls:
        all_url_data=requests.get(url).text
        all_soup_data = BeautifulSoup(all_url_data,"lxml")
        all_lists = all_soup_data.find_all('li',class_='clearfix job-bx wht-shd-bx')
        for item in all_lists:
            job_title=item.find('h2').text                                                                          #  to get job title
            company_name=item.find('h3',class_="joblist-comp-name").text                                            # to get company name
            expereince=item.find('li').text                                                                         # gives the all data in li tag
            expereince=expereince[11:]                                                                              # get experience we use slicing 
            location=item.find('ul',class_="top-jd-dtl clearfix").text                                              # gives the all data in ul tag
            location=location.split("\n")                                                                           # split the string to find location
            location=location[4:6]                                                                                  # used silicing for limited data
            for i in location:                                                                                      # loop for remove the space and "location_on"
                if i=="location_on":
                    location.remove('location_on')
                elif i==' ':
                    location.remove(' ')
            location1=" ".join(location)

            job_description=item.find('ul',class_="list-job-dtl clearfix").text                                     # same as location
            job_description=job_description.split("\n")
            job_description=job_description[3]
            key_skills=item.find('ul',class_="list-job-dtl clearfix").text
            key_skills=key_skills.split("\n")
            key_skills=key_skills[9]
            job_url=item.find("a")['href']
            

            # create dictionary to append data in list
            all_job_data={          
                'Job Title':job_title,
                'Company_name':company_name,
                'Expereince':expereince,
                'Location':location1,
                'Job Description':job_description,
                'Key Skills':key_skills,
                'Job Detail Link':job_url
                }
            all_data.append(all_job_data)


    data=pd.DataFrame(all_data)                                                                                     #convert data in rows and column using panadas
    print(data)
    data.to_excel('dataexcel.xlsx',index=FALSE)                                                                     # convert data in excelfile

webscrapper()                                                                                                       #function call
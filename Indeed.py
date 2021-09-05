# Indeed Jobs Scraping
# Tutorial from John Watson Rooney YouTube Channel

import requests
import pprint
from bs4 import BeautifulSoup
from requests.api import head
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=python%20developer&l=Los%20Angeles%2C%20CA&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    # return len(divs)
    for item in divs:
        title = item.find('h2', class_= 'jobTitle').text
        company = item.find('span', class_= 'companyName').text
        try:
            salary = item.find('span', class_= 'salary-snippet').text
            #print(salary)
        except AttributeError:
            salary = ''
            #print('No salary listed')
        location = item.find('div', class_= 'companyLocation').text
        summary = item.find('div', class_= 'job-snippet').text.strip().replace('\n', '')
        #print('*' * 30)
    
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'location': location,
            'summary': summary,
        }

        joblist.append(job)

    return


joblist = []

# Do a while loop if you want all of the job postings to get the len and then handle exceptions. 
# Middle number is the page number. 0 = 1st page, 10 = 2nd page, 20 = 3rd page, and so on. 

for i in range(0, 90, 10):
    print(f'Getting page, {i}')
    c = extract(0)
    # print(transform(c))
    transform(c)
    #pprint.pprint(joblist)
#print(len(joblist))

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('Indeed_Jobs.csv')
df.to_json('Indeed_Jobs.json')




# NOTES: 
# If not a class_ and rather an id, you can pass in a dictionary. Example:
# ('div', {'id': 'companyName'})
# this works for class as well. Example:
# ('div', {'class': 'companyName'})

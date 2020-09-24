from bs4 import BeautifulSoup as bs
import requests as re
import csv

save = []

# for item in range(800,990,10):

#     # url = 'https://au.indeed.com/jobs?q=Change+Manager&l=Sydney&start=' + str(item)

#     # print(url)

#     # while True:
#     #     try:
#     #         res = re.get(url)
#     #         break
#     #     except:
#     #         print('lost')

#     url = 'https://au.indeed.com/jobs?q=Change+Manager&l=Sydney'

#     res = re.get(url)


#     soup = bs(res.text, 'lxml')

#     h2 = soup.find_all('div', {'data-tn-component':'organicJob'})

#     for item in h2:
#         name = item.find('a').get('title')
#         link = 'https://au.indeed.com' + item.find('a').get('href')

#         try:
#             company = item.find('a', {'data-tn-element':'companyName'}).text.strip()
#         except AttributeError:
#             company = item.find('div', class_='sjcl').find('span').text.strip()


        
#         save.append({
#             'Job name':name,
#             'Company name':company,
#             'link':link,
#         })

#         print(f'job:{name} // company:{company} // link:{link}')

# with open('job5.csv', 'w', newline='') as job:

#     write = csv.DictWriter(job, fieldnames=save[0].keys())
#     write.writeheader()

#     for item in save:
#         write.writerow(item)
        
#     job.close()
    


url = 'https://au.indeed.com/jobs?q=Change+Manager&l=Sydney'

res = re.get(url)


soup = bs(res.text, 'lxml')

h2 = soup.find_all('div', {'data-tn-component':'organicJob'})

for item in h2:
    name = item.find('a').get('title')
    link = 'https://au.indeed.com' + item.find('a').get('href')

    try:
        company = item.find('a', {'data-tn-element':'companyName'}).text.strip()
    except AttributeError:
        company = item.find('div', class_='sjcl').find('span').text.strip()


    
    save.append({
        'Job name':name,
        'Company name':company,
        'link':link,
    })

    print(f'job:{name} // company:{company} // link:{link}')

    

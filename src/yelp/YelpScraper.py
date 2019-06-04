import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

restaurant = 'subway'
base_urls = []
with open("{}.txt".format(restaurant), "r") as fp:
   line = fp.readline()
   cnt = 0
   while line:
       if line.strip() not in base_urls:
            base_urls.append(line.strip())
       cnt += 1
       line = fp.readline()

print(base_urls.__len__())

# proxies = {'https': 'https://132.148.150.41:80'}
# proxy_support = urllib.request.ProxyHandler(proxies)
# opener = urllib.request.build_opener(proxy_support)
# req = opener.open('https://www.yelp.com/biz/subway-copley')
# print(req)
# urllib.request.install_opener(opener)

review_count = 1
location_index = 0
start = 0
try:
    with open('{}_recover.json'.format(restaurant)) as json_file:
        try:
            data = json.load(json_file)
            if 'location_index' in data and 'review_count' in data and 'start' in data:
                review_count = data['review_count']
                location_index = data['location_index']
                start = data['start']
        except Exception as ex:
            print(ex)
            json_file1 = open('{}_recover.json'.format(restaurant), 'w+')
            recovery_object = {'location_index': 0, 'review_count': 1, 'start': 0}
            json_file1.write(json.dumps(recovery_object))
except Exception as ex:
    json_file1 = open('{}_recover.json'.format(restaurant), 'w+')
    recovery_object = {'location_index': 0, 'review_count': 1, 'start': 0}
    json_file1.write(json.dumps(recovery_object))


for index, base_url in enumerate(base_urls, start=0):
    if location_index == 0 or index >= location_index:
        text_file = open("{}_review.txt".format(restaurant), "a+")
        csv_file = open('{}_review.csv'.format(restaurant), '+a')
        print(base_url)
        html = urlopen(base_url)
        print(base_url)
        soup = BeautifulSoup(html, 'html.parser')
        limit = soup.find("div", {"class" : "page-of-pages arrange_unit arrange_unit--fill"})
        totalPage = int(limit.text.strip().split(' ')[3])
        for i in range(start, totalPage):
            html = urlopen(base_url + "?start={}".format(i*20))
            print(base_url + "?start={}".format(i*20))
            soup = BeautifulSoup(html, 'html.parser')
            review_divs = soup.findAll("div", {"class": "review-content"})
            for div in review_divs:
                star_rating = div.div.div.div['title'].split(' ')[0]
                text_file.write("{} : {} \n ".format(review_count, div.p.text))
                course = [review_count, div.p.text, star_rating]
                writer = csv.writer(csv_file,  delimiter='|')
                writer.writerow(course)
                review_count += 1
            start_value = i+1
            recovery_object = {'location_index': index, 'review_count': review_count, 'start': start_value}
            fp = open("{}_recover.json".format(restaurant), "w+")
            fp.write(json.dumps(recovery_object))
            fp.close()
            print(recovery_object)
        text_file.close()
        csv_file.close()
        start = 0
        next_index = index + 1
        recovery_object = {'location_index': next_index, 'review_count': review_count, 'start': start}
        fp = open("{}_recover.json".format(restaurant), "w+")
        fp.write(json.dumps(recovery_object))
        fp.close()
        print(recovery_object)
        print("Percentage: {} Finished: {} BaseUrl Completed: {} ".format((index/base_urls.__len__())*100, index, base_url))
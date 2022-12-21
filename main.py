import requests
from time import sleep
import xml.etree.cElementTree as et
import csv
import pandas as pd

# oclcNumber = ['93', '966034982', '966041949', '822695808']
url = 'http://www.worldcat.org/webservices/catalog/content/libraries/'  # URL of library locations API
qParams = '?location=53201&maximumLibraries=500&frbrGrouping=off&wskey='  # query parameters. see also api documentation to modify
key = 'key'  # request a key from OCLC

data = pd.read_csv(
    'yourInputCSV.csv')  # input CSV should have one column containing OCLC numbers in single quotes. Header column should be labeled Number.

numberList = list(data['Number'].values)

count = 0

with open('yourOutputCSV.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['OCLC NUMBER', 'HOLDINGS', 'LOCATION1', 'LOCATION2', 'LOCATION3'])
    for n in numberList:
        count += 1
        query = url + str(n) + qParams + key
        sleep(1.0)
        if count % 400 == 0:
            sleep(60)
        response = requests.get(query)
        root = et.fromstring(response.content)
        holdings = root.findall('holding')
        counter = 0
        physLocations = []
        for location in root.iter('physicalLocation'):
            locationOne = location.text
            physLocations.append(locationOne)
        for copies in root.iter('copiesCount'):
            copiesCount = copies.text
            counter = counter + 1
        for item in holdings:
            try:
                # writer.writerow([n, item.find('physicalLocation').text, copiesCount])
                # print(item.findall('holdingSimple')[1].find('copiesSummary').text)
                print(n)
                writer.writerow([n, counter, physLocations[1], physLocations[2], physLocations[3]])
                break
            except IndexError as error:
                writer.writerow(["n", "-", "-", "-", "-"])
                print("OCLC number error")

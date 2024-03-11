import requests
import json
import os
from clint.textui import progress
import urllib.parse
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()
secret_key = os.getenv("SECRET_KEY")

download_dir = "dnld/"

headers = {
    'authority': 'www.pexels.com',
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,mr;q=0.6',
    'authorization': '',
    'content-type': 'application/json',
    'referer': 'https://www.pexels.com/search/lion/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'secret-key': secret_key,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-client-type': 'react',
    'x-forwarded-cf-connecting-ip': '',
    'x-forwarded-cf-ipregioncode': '',
    'x-forwarded-http_cf_ipcountry': ''
}

fil_type_mappings = {
    1: "small",
    2: "medium",
    3: "large"
}


def download_file(url, filepath):
    try:
        r = requests.get(url, stream=True, headers=headers)
        if os.path.isfile(filepath) == False:
            with open(filepath, 'wb') as f:
                total_length = int(r.headers.get('content-length'))
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                    if chunk:
                        f.write(chunk)
                        f.flush()
    except Exception as e:
        print("problem while downloading...", e)


search_topic = ""
print("***************************************")
while True:
    search_topic = input("Enter subject to search: ")
    if search_topic == "" or search_topic == " ":
        print("please enter search topic: ")
        continue
    else:
        break

type_of_image = ""
print("***************************************")
while True:
    try:
        type_of_image = int(
            input("Enter type of images (1:small 2:medium 3:large) "))
        if type_of_image not in [1, 2, 3]:
            print("please enter type of images between 1,2,3")
            continue
        else:
            break
    except:
        print("please enter type of images between 1,2,3")
        continue

number_of_images = 1
print("***************************************")
while True:
    try:
        number_of_images = int(input("Enter number of images: "))
        if number_of_images == "" or number_of_images == " ":
            print("please enter number of images:")
            continue
        else:
            break
    except:
        print("please enter number of images")
        continue


enocoded_search_topic = urllib.parse.quote(search_topic)
url = "https://www.pexels.com/en-us/api/v3/search/photos?page=1&per_page="+str(number_of_images)+"&query=" + \
    enocoded_search_topic+"&orientation=all&size=all&color=all&sort=popular&seo_tags=true"

file_type_str = fil_type_mappings.get(type_of_image)
filepath = os.path.join(download_dir, search_topic, file_type_str)

if not os.path.exists(filepath):
    os.makedirs(filepath)
else:
    print("folder already exists")

response = requests.request("GET", url, headers=headers)
op = json.loads(response.text)

for count, ele in enumerate(op["data"]):

    id = ele["id"]
    image_url_selector = ele["attributes"]["image"]

    file_link = image_url_selector[file_type_str]

    parsed_url = urlparse(file_link)
    filename = os.path.basename(parsed_url.path)
    filepath_current_file = os.path.join(filepath, filename)

    download_file(file_link, filepath_current_file)

    if count >= number_of_images:
        break

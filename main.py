import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)'
}


def download(url):
    resp = requests.get(url, stream=True)
    r = open('C:\\Users\\Vedis\\MyProject\\parsing\\images\\' + url.split('/')[-1], 'wb')  # write bait
    for value in resp.iter_content(1024*1024):  # запись количество байт за один проход
        r.write(value)
    r.close()


def get_url():
    for count in range(1, 8):

        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        data_1 = soup.find_all('div', class_="w-full rounded border")

        for d in data_1:
            cart_url = 'https://scrapingclub.com' + d.find('a').get('href')
            yield cart_url


def get_data():
    for cart_url in get_url():
        response = requests.get(url=cart_url, headers=headers)
        sleep(3)
        soup = BeautifulSoup(response.text, 'lxml')

        data = soup.find('div', class_="my-8 w-full rounded border")
        name = data.find('img', class_="card-img-top").get('alt')
        price = data.find('h4', class_="my-4 card-price").text
        description = data.find('p', class_="card-description").text
        photo = 'https://scrapingclub.com' + data.find('img', class_="card-img-top").get('src')
        download(photo)

        yield name, price, description, photo

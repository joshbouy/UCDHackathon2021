from flask import Flask,render_template,request
from selectorlib import Extractor
from bs4 import BeautifulSoup
from flask import jsonify
import requests
import json
from time import sleep

app = Flask(__name__)

class Item:
    def __init__(self, productName, price):
        self.productName = productName
        self.price = price
    def display(self):
        res = []
        res.append(self.productName, str(self.price))
        return res


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():

    #search_key = request.form['text']    
    url = 'https://www.amazon.com/s?k=' + "+".join( (request.form['text']).split() )

    e = Extractor.from_yaml_file('selectors.yml')
    def scrape(url):
        #inStock = False
        items = []
        fakePerson = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding":"gzip, deflate",     
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"}
        print("Downloading %s"%url)
        req = requests.get(url, headers=fakePerson)
        if req.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in req.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d"%(url,req.status_code))
            return None
        soup = BeautifulSoup(str(req.text), 'html.parser')
        productName = soup.find_all('span', class_="a-size-base-plus a-color-base a-text-normal")
        productPrices = soup.find_all('span', class_="a-price-whole")
        productPricesDec = soup.find_all('span', class_="a-price-fraction")
        for i in range(len(productName)):
            priceString = "0.0"
            try:
                priceString = str(productPrices[i].next) + "." + str(productPricesDec[i].next)
            except IndexError:
                pass
            items.append(Item(str(productName[i].next), float(priceString)))
        return items

@app.route('/scrap')
def getStoreJSON():
    return outfile

if __name__ == '__main__':
    app.run() 
from flask import Flask,render_template,request
from selectorlib import Extractor
from flask import jsonify,Markup
from bs4 import BeautifulSoup
import requests
import json

class Item:
    def __init__(self, productName: str, price: float, link: str):
        self.productName = productName
        self.price = price
        self.link = link
    def display(self):
        res = []
        res.append(self.productName, str(self.price))
        return res

app = Flask(__name__)

def scrape(url: str):
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
    productLinks = soup.find_all('a',class_="a-link-normal a-text-normal")
    for i in range(len(productName)):
        priceString = "0.0"
        try:
            priceString = str(productPrices[i].next) + "." + str(productPricesDec[i].next)
        except IndexError:
            pass
        items.append(Item(str(productName[i].next), str(priceString), "amazon.com" + str(productLinks[i].get('href'))))
    return items


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
 
    global url 
    url = 'https://www.amazon.com/s?k=' + "+".join( (request.form['text']).split())
    return render_template('data.html')
        #return outfile


@app.route('/scrap')
def getStoreJSON():
    outfile = ""
    stuff = []
    items = scrape(url)
    if items:
        for each in items:
            stuff.append(json.loads(json.dumps(each.__dict__)))
        amazon = {"data": stuff}
        outfile = json.dumps(amazon)
    return outfile

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data')
def data():
    return render_template('data.html')

if __name__ == '__main__':
    app.run() 
from flask import Flask,render_template,request
from selectorlib import Extractor
from flask import jsonify
import requests
import json
from time import sleep

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')

#url = 'https://www.amazon.com/Amazon-Brand-Solimo-Toilet-Sheets/dp/B07FGBSF45/ref=sr_1_1_sspa?dchild=1&keywords=toilet+paper&qid=1610836195&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExS0Y3VDhGQVo4Mkg3JmVuY3J5cHRlZElkPUEwNDE5NTI0MUdEV0E0NUczRFYwWiZlbmNyeXB0ZWRBZElkPUEwNjE3NTQ5M0xXNVE1SEVRRDZOSiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

#WEBrequest = requests.get(url)
"""
e = Extractor.from_yaml_file('selectors.yml')
def scrape(url):
    inStock = False
    fakePerson = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    print("Downloading %s"%url)
    req = requests.get(url, headers=fakePerson)
    if req.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in req.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,req.status_code))
        return None
    if "In Stock" in str(req.text):
        print("yes")
        inStock = True
    else:
        print("no")
    return (e.extract(req.text), inStock)
# product_data = []
outfile = ""
data, stockStatus = scrape(url)
if data:
    outfile = str(json.dumps(data))
    jsonOBJ = json.loads(outfile)
    jsonOBJ.update({"InStock": stockStatus})
    outfile = json.dumps(jsonOBJ)
    # sleep(5)
"""

@app.route('/', methods=['POST'])
def my_form_post():
    
    url = request.form['text']
    e = Extractor.from_yaml_file('selectors.yml')
    
    def scrape(url):
        inStock = False
        fakePerson = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0;   Win64;     x64; rv:66.0) Gecko/20100101 Firefox/66.0",    "Accept-Encoding":"gzip, deflate",     "Accept":"text/html,    application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",     "DNT":"1","Connection":"close",     "Upgrade-Insecure-Requests":"1"}
        print("Downloading %s"%url)
        req = requests.get(url, headers=fakePerson)
        if req.status_code > 500:
            if "To discuss automated access to Amazon data please   contact" in req.text:
                print("Page %s was blocked by Amazon. Please try    using better proxies\n"%url)
            else:
                print("Page %s must have been blocked by Amazon as  the status code was %d"%(url,req.status_code))
            return None
        if "In Stock" in str(req.text):
            print("yes")
            inStock = True
        else:
            print("no")
        return (e.extract(req.text), inStock)
    # product_data = []
    outfile = ""
    data, stockStatus = scrape(url)
    if data:
        outfile = str(json.dumps(data))
        jsonOBJ = json.loads(outfile)
        jsonOBJ.update({"InStock": stockStatus})
        outfile = json.dumps(jsonOBJ)
        # sleep(5)
    
    return outfile

@app.route('/scrap')
def getStoreJSON():
    return outfile

if __name__ == '__main__':
    app.run()
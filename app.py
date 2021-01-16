from flask import Flask
from selectorlib import Extractor
from flask import jsonify
import requests
import json
app = Flask(__name__)


url = 'https://www.amazon.com/dp/B07SVB39J2/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B07SVB39J2&pd_rd_w=fBpel&pf_rd_p=45e679f6-d55f-4626-99ea-f1ec7720af94&pd_rd_wg=i8iyA&pf_rd_r=MSG0RC5GAHH9FD7VSNDV&pd_rd_r=a7ae652d-a41c-45c1-872f-25a1f027c1b2&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzVk9DMzdOVjY1MENXJmVuY3J5cHRlZElkPUEwMjQwMzA1MTU1TUc0RFA0S0dVSyZlbmNyeXB0ZWRBZElkPUEwNzEzMjk1MjVNRkdNNjdPUFZBSyZ3aWRnZXROYW1lPXNwX2RldGFpbCZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='
#WEBrequest = requests.get(url)
e = Extractor.from_yaml_file('selectors.yml')
def scrape(url):
    inStock = False
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
    if "In Stock" in str(req.text):
        inStock = True
    return (e.extract(req.text), inStock)
# product_data = []
outfile = ""
data, stockStatus = scrape(url)
if data:
    outfile = str(json.dumps(data))
    jsonOBJ = json.loads(outfile)
    jsonOBJ.update({"InStock": stockStatus})
    outfile = json.dumps(jsonOBJ)

@app.route('/')
def getStoreJSON():
    return outfile

if __name__ == '__main__':
    app.run()
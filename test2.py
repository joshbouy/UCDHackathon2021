from flask import Flask, render_template, jsonify
 
app = Flask(__name__)
 
@app.route('/index')
@app.route('/')
def index():
  return render_template('index.html')
 
@app.route('/index_get_data')
def stuff():
  # Assume data comes from somewhere else
  data = {
    "data": [
      {
         "productName":"Cottonelle Professional Bulk Toilet Paper for Business (17713), Standard Toilet Paper Rolls, 2-PLY, White, 60 Rolls / Case, 451 Sheets / Roll",
         "price":54.71,
         "link":"amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&adId=A091815737SIF0749AFL0&url=%2FCottonelle-Professional-Toilet-Business-Standard%2Fdp%2FB0014C440U%2Fref%3Dsr_1_1_sspa%3Fdchild%3D1%26keywords%3Dtoilet%2Bpaper%26qid%3D1610926913%26sr%3D8-1-spons%26psc%3D1&qualifier=1610926913&id=2551844196154844&widgetName=sp_atf"
      },
      {
         "productName":"Scott Essential Professional Bulk Toilet Paper for Business (04460), Individually Wrapped Standard Rolls, 2-PLY, White, 80 Rolls / Case, 550 Sheets / Roll",
         "price":61.93,
         "link":"amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_atf_aps_sr_pg1_1?ie=UTF8&adId=A09180333G62JRGOM3G5V&url=%2FEssential-Professional-Business-Individually-Standard%2Fdp%2FB001AZFA0O%2Fref%3Dsr_1_2_sspa%3Fdchild%3D1%26keywords%3Dtoilet%2Bpaper%26qid%3D1610926913%26sr%3D8-2-spons%26psc%3D1&qualifier=1610926913&id=2551844196154844&widgetName=sp_atf"
      }]
  }
  return jsonify(data)
 
 
if __name__ == '__main__':
  app.run()
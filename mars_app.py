from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape
from scrape_mars import init_browser

app=Flask(__name__)

mongo=PyMongo(app,uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_data=mongo.db.mars.find_one()
    return render_template("index2.html", mars=mars_data)

@app.route('/scrape')
def data():
    mars_data_variable = scrape()
    
    mongo.db.mars.update({},mars_data_variable,upsert=True)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
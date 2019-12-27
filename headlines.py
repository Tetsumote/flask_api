import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib

app = Flask(__name__)

#https://openexchangerates.org/account/app-ids
#https://home.openweathermap.org/api_keys

exchange = "https://openexchangerates.org//api/latest.json?app_id=6649142c4d9b495bbe34570ae62d6355"

RSS_FEEDS = {
    'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
    'world':'http://feeds.bbci.co.uk/news/world/rss.xml',
    'tech':'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
}


@app.route("/", methods=['GET','POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html",articles=feed['entries'])

@app.route("/weather" , methods=['GET','POST'])
def get_weather():
    query = request.form.get("city")
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=01b4098397b9017a7f25bd7424b588bd"
    #query = urllib.parse.quote(query)
    print(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                    'temperature': parsed['main']['temp'],
                    'city': parsed['name'],
                    'country': parsed['sys']['country']
                    }
    return render_template("weather.html",weather=weather)




@app.route("/<publication>")
def get_news1(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)

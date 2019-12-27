import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

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

@app.route("/<publication>")
def get_news1(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
    app.run(port=5000, debug=True)

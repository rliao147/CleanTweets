from flask import Flask, render_template, request
import clean

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("main.html")

@app.route("/unclean", methods = ['POST'])
def unclean():
    if request.method == "POST":
        username = request.form.get("un")
        start = request.form.get("sd")
        if start == "0":
            start = int(start)
        end = request.form.get("ed")
        if end == "0":
            end = int(end)
        tweets = clean.cleanedTweets(clean.flag_tweets(username, start, end))
        return render_template("unclean.html", tweets=tweets)
    
if __name__=="__main__":
    app.run(debug=True) #Never run as debug=True in a production environment

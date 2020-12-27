from flask import Flask, render_template, request
import COVID19Py
import requests

covid19 = COVID19Py.COVID19()
latest = covid19.getLatest()


res_loc = requests.get('https://ipinfo.io/')
user_loc = res_loc.json()



locations = covid19.getLocations()


app = Flask(__name__)

def getUserStat(user_country, locations):
    for i in locations:
        if i.get('country_code')==user_country:
            l = [dict(i.get('latest')), i.get('country')]
            return l
def MySearch(query, locations):
    for i in locations:
        if i.get("country")==query:
            return i
       

@app.route("/")
def index():
    confirmed = latest.get("confirmed")
    deaths = latest.get("deaths")
    recovered = latest.get("recovered")
    # print(confirmed)
    user_country = user_loc['country']
    user_stat=getUserStat(user_country, locations)
    user_latest=user_stat[0]
    user_country=user_stat[1]
    user_coor = str(user_loc['loc'])
    user_coor = user_coor.split(',')
    # print(user_loc)
    # print(user_city)
    # print(user_latest)
    # print(locations)

    params = {"confirmed":confirmed, "recovered":recovered, "deaths":deaths, "locations":locations, "user_latest":user_latest, "user_country":user_country, "user_coor":user_coor}
    return render_template('index.html', params=params)
@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        s_country = request.form
        s_country=dict(s_country)
        s_country=s_country.get("country")
        result=MySearch(s_country, locations)
        return render_template('search.html', result=result)
@app.route('/map')
def mapPage():
    # print(user_loc)
    user_coor = str(user_loc['loc'])
    user_coor = user_coor.split(',')
    params={"user_coor":user_coor}
    return render_template('map.html', params=params)

    

app.run(debug=True)

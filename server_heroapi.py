import dota, dota2
import flask
from flask import request, render_template
import requests, json

#print(dota.getHeroData("invoker",2))

app = flask.Flask(__name__)
app.config["DEBUG"] =  True

@app.route('/dota', methods=['GET'])
def dota():
    return render_template('dota.html')


@app.route('/api/v1/dotahero', methods=['GET'])
def respond():
    # here we want to get the value of user (i.e. ?hero=some-value&range=other-value)
    hero = request.args.get('hero').replace('"','')
    timerange = int(request.args.get('range'))
    data = dota2.getHeroData(hero,timerange)
    return data

app.run('0.0.0.0',port=5000)

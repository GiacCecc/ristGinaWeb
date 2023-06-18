# 10.06.2023, Berlin
# Giacomo Ceccarelli
# Second attempt to design web page for ristGinaIoT
# v. 0.01

import datetime as dt
from ristGinaMongo import get_data_timerange

from flask import Flask, render_template #, redirect, url_for, request, jsonify, make_response
from pymongo import MongoClient

import json
import plotly
import plotly.express as px


#tz_rome = dt.timezone(dt.timedelta(hours=2, minutes=0), 'Europe/Rome')
app = Flask(__name__)

@app.route('/')
def index():
    URI = 'mongodb+srv://admin:admin@cluster0.kqg6lq5.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(URI)
    db = client['CF01']
    collection = db['logs']

    # --------------------------------------------------------------------

    last_document = collection.find_one(sort=[('_id', -1)])

    if last_document:
        logTime = last_document['logTime'] #.astimezone(tz_rome) # + dt.timedelta(hours=2)
        temp = last_document['temp']
    else:
        logTime = 'not found'
        temp = 'not found'
    
    # --------------------------------------------------------------------

    end_date = dt.datetime.utcnow() #pd.to_datetime("2023-05-18 10:00:00")
    start_date = end_date - dt.timedelta(hours=48)
    dfLogs = get_data_timerange(client, 'logs', start_date, end_date)

    x = dfLogs.index #.time
    y = dfLogs['temp']
    fig = px.scatter(x=x, y=y,
                     #labels=dict(x=N, y="Temperatura (°C)")
                     )
    
    fig.update_layout(
        #margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='#FFFDFA',
        plot_bgcolor='rgba(255,255,255,0)',
        )
    
    fig.update_traces(marker_size=4, marker_color='#544D93')
    
    fig.update_xaxes(title=None,
                     #range=[start_date, end_date],
                     showgrid=True,
                     gridwidth=.5,
                     gridcolor='rgba(0,0,0,.2)'
                     )
    
    fig.update_yaxes(ticklabelposition="inside top",
                     title="Temperatura (°C)",
                     range=[-5, 15],
                     showgrid=True,
                     gridwidth=1,
                     #griddash='dash',
                     gridcolor='rgba(0,0,0,.5)'
                     )
   
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(count=12, label="12h", step="hour", stepmode="backward"),
                    dict(count=1, label="1D", step="day", stepmode="todate"),
                    #dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    return render_template('index.html', logTime=logTime, temp=temp, graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(debug=True)

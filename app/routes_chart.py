from flask import render_template, flash, redirect, url_for
from flask import request
from werkzeug.urls import url_parse
from app import app
from app import db

from flask_login import current_user, login_user
from flask_login import login_required
from flask_login import logout_user

from app.models import User
#from app.models import Post

from datetime import datetime

# Charts dependancies
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json

# Create random data with numpy
import numpy as np
#For bubble chart demo
import math
import pandas as pd

@app.route('/plotlyscatter', methods=['GET'])
@login_required
def plotlyscatter():

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N) + 5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N) - 5

    #plt.gcf().clear()
    #lineimg = BytesIO()

    # Create traces
    trace0 = go.Scatter(
        x=random_x,
        y=random_y0,
        mode='markers',
        name='markers'
    )
    trace1 = go.Scatter(
        x=random_x,
        y=random_y1,
        mode='lines+markers',
        name='lines+markers'
    )
    trace2 = go.Scatter(
        x=random_x,
        y=random_y2,
        mode='lines',
        name='lines'
    )

    data = [trace0, trace1, trace2, ]
    #convert to JSON format
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    #py.iplot(data, filename='scatter-mode')
    #plt.savefig(lineimg, format='png')

    #lineimg.seek(0)
    #plot_url = base64.b64encode(lineimg.getvalue()).decode('ascii')
    return render_template("plotlychart.html", graphJSON=graphJSON)

@app.route('/plotlybar', methods=['GET'])
@login_required
def plotlybar():
    trace0 = go.Bar(
        x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
        name='Primary Product',
        marker=dict(
            color='rgb(49,130,189)'
        )
    )
    trace1 = go.Bar(
        x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
        name='Secondary Product',
        marker=dict(
            color='rgb(204,204,204)',
        )
    )

    data = [trace0, trace1]
    layout = go.Layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
    )

    # convert to JSON format
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("plotlychart.html", graphJSON=graphJSON)

@app.route('/plotlybubble', methods=['GET'])
@login_required
def plotlybubble():
    data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")
    df_2007 = data[data['year'] == 2007]
    df_2007 = df_2007.sort_values(['continent', 'country'])
    slope = 2.666051223553066e-05
    hover_text = []
    bubble_size = []

    for index, row in df_2007.iterrows():
        hover_text.append(('Country: {country}<br>' +
                           'Life Expectancy: {lifeExp}<br>' +
                           'GDP per capita: {gdp}<br>' +
                           'Population: {pop}<br>' +
                           'Year: {year}').format(country=row['country'],
                                                  lifeExp=row['lifeExp'],
                                                  gdp=row['gdpPercap'],
                                                  pop=row['pop'],
                                                  year=row['year']))
        bubble_size.append(math.sqrt(row['pop'] * slope))

    df_2007['text'] = hover_text
    df_2007['size'] = bubble_size
    sizeref = 2. * max(df_2007['size']) / (100 ** 2)

    trace0 = go.Scatter(
        x=df_2007['gdpPercap'][df_2007['continent'] == 'Africa'],
        y=df_2007['lifeExp'][df_2007['continent'] == 'Africa'],
        mode='markers',
        name='Africa',
        text=df_2007['text'][df_2007['continent'] == 'Africa'],
        marker=dict(
            symbol='circle',
            sizemode='area',
            sizeref=sizeref,
            size=df_2007['size'][df_2007['continent'] == 'Africa'],
            line=dict(
                width=2
            ),
        )
    )
    trace1 = go.Scatter(
        x=df_2007['gdpPercap'][df_2007['continent'] == 'Americas'],
        y=df_2007['lifeExp'][df_2007['continent'] == 'Americas'],
        mode='markers',
        name='Americas',
        text=df_2007['text'][df_2007['continent'] == 'Americas'],
        marker=dict(
            sizemode='area',
            sizeref=sizeref,
            size=df_2007['size'][df_2007['continent'] == 'Americas'],
            line=dict(
                width=2
            ),
        )
    )
    trace2 = go.Scatter(
        x=df_2007['gdpPercap'][df_2007['continent'] == 'Asia'],
        y=df_2007['lifeExp'][df_2007['continent'] == 'Asia'],
        mode='markers',
        name='Asia',
        text=df_2007['text'][df_2007['continent'] == 'Asia'],
        marker=dict(
            sizemode='area',
            sizeref=sizeref,
            size=df_2007['size'][df_2007['continent'] == 'Asia'],
            line=dict(
                width=2
            ),
        )
    )
    trace3 = go.Scatter(
        x=df_2007['gdpPercap'][df_2007['continent'] == 'Europe'],
        y=df_2007['lifeExp'][df_2007['continent'] == 'Europe'],
        mode='markers',
        name='Europe',
        text=df_2007['text'][df_2007['continent'] == 'Europe'],
        marker=dict(
            sizemode='area',
            sizeref=sizeref,
            size=df_2007['size'][df_2007['continent'] == 'Europe'],
            line=dict(
                width=2
            ),
        )
    )
    trace4 = go.Scatter(
        x=df_2007['gdpPercap'][df_2007['continent'] == 'Oceania'],
        y=df_2007['lifeExp'][df_2007['continent'] == 'Oceania'],
        mode='markers',
        name='Oceania',
        text=df_2007['text'][df_2007['continent'] == 'Oceania'],
        marker=dict(
            sizemode='area',
            sizeref=sizeref,
            size=df_2007['size'][df_2007['continent'] == 'Oceania'],
            line=dict(
                width=2
            ),
        )
    )

    data = [trace0, trace1, trace2, trace3, trace4]
    layout = go.Layout(
        title='Life Expectancy v. Per Capita GDP, 2007',
        xaxis=dict(
            title='GDP per capita (2000 dollars)',
            gridcolor='rgb(255, 255, 255)',
            range=[2.003297660701705, 5.191505530708712],
            type='log',
            zerolinewidth=1,
            ticklen=5,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Life Expectancy (years)',
            gridcolor='rgb(255, 255, 255)',
            range=[36.12621671352166, 91.72921793264332],
            zerolinewidth=1,
            ticklen=5,
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )
    # convert to JSON format
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("plotlychart.html", graphJSON=graphJSON)
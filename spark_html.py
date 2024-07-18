import dash
import re
from dash import Dash, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go
import pandas as pd
import glob
from plotly.subplots import make_subplots
import os

colors = {
    'background': 'white',
    'text': '#7FDBFF',
}

app = Dash(__name__)

class Spark:

    def __init__(self, application=None):

        files = glob.glob("./spark_streaming_test/bruv_spark_submit/reports/*.csv")
        li = []
        columns = ["id", "longitude", "latitude", "person", "peaceScore", "words", "timestamp", "gender"]
        for file in files:
            try:
                csv = pd.read_csv(file, names=columns)
                csv.head()
                li.append(csv)
            except pandas.io.common.EmptyDataError:
                print(f"{file} is empty")

        df = pd.concat(li, axis=0, ignore_index=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y_%m_%d_%H_%M_%S")
        df = df.dropna()
        #Question 1
        droneAvg = df[["id", "peaceScore"]]
        droneAvg = droneAvg.groupby("id", as_index=False)['peaceScore'].mean()
        print(droneAvg.head())
        fig1 = px.bar(droneAvg, x="id", y="peaceScore", labels={ "id" : "Drone Id", "peaceScore" : "Average PeaceScore"})

        #Question 2
        droneAvgTime = df[["timestamp", "peaceScore"]]
        droneAvgTime = droneAvgTime.groupby("timestamp", as_index=False)['peaceScore'].mean()

        fig2 = px.line(droneAvgTime, x="timestamp", y="peaceScore")

        #Question 3
        badWords = ["fuck", "motherfucker", "bitch", "stupid", "idiot", "shit", "dumbass", "damn", "shag", "wanker",
                    "twat", "cunt", "asshole"]
        onlyBadWords = df.loc[df['words'].isin(badWords)]
        badWordsGroupBy = onlyBadWords["words"].value_counts().to_frame()

        fig3 = px.histogram(badWordsGroupBy, x=badWordsGroupBy.index, y=badWordsGroupBy.words, labels={"index" : "Bad Words"}).update_layout(yaxis_title="Occurrences")

        #Question 4
        groupeByGender = df[["gender", "peaceScore"]]
        groupeByGender = groupeByGender.groupby("gender", as_index=False)['peaceScore'].mean()
        fig4 = px.histogram(groupeByGender, y="peaceScore", x="gender", labels={"gender" : "Gender"}).update_layout(yaxis_title="Average PeaceScores")

        self.main_layout = html.Div(children=[
            html.H1(
                children='Analytics',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),

            html.H2(children=['Average peaceScores on each drone',
                              dcc.Graph(
                                  id='example-graph-1',
                                  figure=fig1
                              )], style={
                'textAlign': 'center',
                'color': colors['text']
            }),

            html.H2(children=['Average peaceScores for each timestamp',
                              dcc.Graph(
                                  id='example-graph-2',
                                  figure=fig2
                              )], style={
                'textAlign': 'center',
                'color': colors['text']
            }),

            html.H2(children=['Occurrence of bad words',
                              dcc.Graph(
                                  id='example-graph-3',
                                  figure=fig3
                              )], style={
                'textAlign': 'center',
                'color': colors['text']
            }),

            html.H2(children=['Average peaceScores of each gender',
                              dcc.Graph(
                                  id='example-graph-4',
                                  figure=fig4
                              )], style={
                'textAlign': 'center',
                'color': colors['text']
            }),
        ], style={
            'backgroundColor': colors['background'],
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
        self.app.layout = self.main_layout


if __name__ == '__main__':
    res = Spark()
    res.app.run_server(debug=True)

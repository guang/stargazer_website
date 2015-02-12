"""         @author:            Guang Yang
            @mktime:            2/2/2015
            @description:       front-end API and views
"""

from flask import Flask, render_template, jsonify
from cassandra.cluster import Cluster
# from cassandra.query import BatchStatement
from utilities import *                     # NOQA
from map_url import *                       # NOQA


def _connect_to_cassandra(keyspace):
    cluster = Cluster(['54.67.42.97'])
    session = cluster.connect(keyspace)
    return session

app = Flask(__name__)
session = _connect_to_cassandra('matches_simple')


@app.route("/")
@app.route("/index")
def landing():
    top_10 = get_top_10_dict()
    recent_10 = get_recent_10_tuple()

    return render_template("index.html", top_10=top_10, recent_10=recent_10)


@app.route("/api/<map_name>/<query_type>/<race>/")
def duration_by_time(map_name, query_type, race):
    if query_type == "duration":
        if race == "A":
            info_by_map = session.execute(
                "SELECT * FROM yolo_duration_all_day WHERE map_name="
                "'{}'".format(map_name)
            )
            results = []

            for row in info_by_map:
                # [ended_at, duration_minutes]
                # duration_minutes is converted into a format that plays nice
                # with highcharts
                results.append([mktime_to_ms(row[1]), row[2]])
            results.sort()

    random_color = random_hex_color()
    # TODO do stuff for different cases
    # TODO add request.args.get("")
    return jsonify(color=random_color, name=map_name, data=results)


def get_top_10_dict():
    """ Get top 10 from cassandra, sort them, then put them into a dictionary
    for easy access in the html view.

    Example:

    """
    top_10_raw = session.execute("SELECT * FROM yolo_top_10")

    top_10_sorted = []
    for row in top_10_raw:
        try:
            map_url = ladder_maps[row[0]]
        except KeyError:
            map_url = ("https://s3-us-west-1.amazonaws.com/guang-stargazer/"
                       "ladder_maps/cat.jpg")
        top_10_sorted.append((row[0], row[1], map_url))
        top_10_sorted.sort(key=lambda tup: tup[1], reverse=True)

    top_10_dict = {}
    for position, row in enumerate(top_10_sorted):
        top_10_dict["num" + str(position)] = {"map_name": row[0],
                                              "match_count": row[1],
                                              "map_url": row[2]}
    return top_10_dict


def get_recent_10_tuple():
    """ Get all maps from recent maps table in cassandra, decode the timestamp,
    sort them by time, pull the most recent 10 maps,
    put them into a tuple to be passed into the html view.

    """

    recent_raw = session.execute("SELECT * FROM yolo_recent_10")

    recent_time_decoded = []
    for row in recent_raw:
        recent_time_decoded.append((row[0], convert_time(row[1])))

    recent_time_decoded.sort(key=lambda tup: tup[1], reverse=True)

    recent_maps = [row[0] for row in recent_time_decoded]
    return recent_maps[:20]


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

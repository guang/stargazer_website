"""         @author:            Guang Yang
            @mktime:            2/2/2015
            @description:       front-end API and views
"""

from flask import Flask, render_template, jsonify  # , request
from cassandra.cluster import Cluster
# from cassandra.query import BatchStatement
from utilities import *                    # NOQA


def _connect_to_cassandra(keyspace):
    cluster = Cluster(['54.67.42.97'])
    session = cluster.connect(keyspace)
    return session

app = Flask(__name__)
session = _connect_to_cassandra('matches_simple')


@app.route("/")
@app.route("/index")
def landing():
    return render_template("index.html")


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

    # TODO do stuff for different cases
    # TODO add request.args.get("")
    return jsonify(name=map_name, data=results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

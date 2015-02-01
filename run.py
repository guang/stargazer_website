"""         @author:            Guang Yang
            @mktime:            2/22/2015
            @description:       yolosite
"""

from flask import Flask, render_template, jsonify
from cassandra.cluster import Cluster
# from cassandra.query import BatchStatement


def _connect_to_cassandra(keyspace):
    cluster = Cluster(['54.67.42.97'])
    session = cluster.connect(keyspace)
    return session

app = Flask(__name__)
session = _connect_to_cassandra('matches_simple')


@app.route("/")
@app.route("/index")
def landing():
    return "Hello Cassandra"


@app.route("/api/duration")
def get_match_id():
    map_name = 'Deadwing LE'
    # TODO make map_name be queryable to be used like this
    # map_name = request.args.get('map_name')
    map_info_all = session.execute("SELECT * FROM yolo_map_duration_over_time")
    # TODO make queries based on only one map
    # " WHERE map_name = {}".format(map_name))

    duration_seconds_all = []

    for row in map_info_all:
        # [ended_at, duration_seconds]
        duration_seconds_all.append([row[1], row[3]])
    duration_seconds_all.sort()

    return jsonify(name=map_name, data=duration_seconds_all)


@app.route("/show_map")
def show_map():

    # map_info_all=session.execute("SELECT * FROM yolo_map_duration_over_time")
    # # TODO make queries based on only one map
    # # " WHERE map_name = {}".format(map_name))

    # match_id_list = []
    # ended_at_list = []
    # duration_seconds_list = []

    # for row in map_info_all:
    #     match_id_list.append(row[0])
    #     ended_at_list.append(row[1])
    #     duration_seconds_list.append(row[3])

    return render_template("map_duration.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

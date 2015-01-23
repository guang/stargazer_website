"""         @author:            Guang Yang
            @mktime:            2/22/2015
            @description:       yolosite
"""

from flask import Flask
from flask import request
from cassandra.cluster import Cluster
# from cassandra.query import BatchStatement


def _connect_to_cassandra(keyspace):
    cluster = Cluster(['54.67.42.97'])
    session = cluster.connect(keyspace)
    return session

app = Flask(__name__)
session = _connect_to_cassandra('all_about_that_database')


@app.route("/")
@app.route("/index")
def landing():
    return "Hello Cassandra"


@app.route("/api")
def get_match_id():
    match_id = request.args.get('match_id')
    row = session.execute("SELECT map_name "
                          "FROM guangs_database "
                          "WHERE id={0}".format(match_id))
    # for row in rows:
    #     print row.duration
    return row[0]


if __name__ == "__main__":
    app.run(host='0.0.0.0')

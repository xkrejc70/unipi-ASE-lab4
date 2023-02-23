from flask import Flask, render_template, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import time

stats_db = "stats_db"
user = "stats"
password = "stats"

app = Flask(__name__, instance_relative_config=True)


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{password}@{stats_db}/{stats_db}"

db = SQLAlchemy(app)

class Stats(db.Model):
    service = db.Column(db.String(100), primary_key = True)
    op = db.Column(db.String(100), primary_key = True)
    visits = db.Column(db.Integer)

    def __init__(self, service, op, visits = 0):
        self.service = service
        self.op = op
        self.visits = visits

with app.app_context():
    # retry, it is very slow to init the mysql db
    for i in range(100):
        try:
            db.create_all()
            print("created tables")
            break
        except:
            time.sleep(5)

def get_stats_service_op(service, op):
    with app.app_context():
        stat = db.session.query(Stats).filter_by(service=service, op=op).first()
        if stat is None:
            return None
        return stat.visits

# return dict with all service stats per op
def get_stats_service(service):
    with app.app_context():
        stats = db.session.query(Stats).filter_by(service=service).all()
        if stats is None:
            return {}

        visits = 0
        for stat in stats:
            visits += stat.visits
        return {stat.op: {"percentage": stat.visits/visits, "visits": stat.visits} for stat in stats}

def get_stats():
    with app.app_context():
        stats = db.session.query(Stats).all()
        if stats is None:
            return {}
        # aggregate stats per service
        stats_dict = {}
        visits = 0
        for stat in stats:
            if stat.service not in stats_dict:
                stats_dict[stat.service] = {}
            stats_dict[stat.service][stat.op] = stat.visits
            visits += stat.visits
        # calculate percentages
        for service in stats_dict:
            for op in stats_dict[service]:
                stats_dict[service][op] = {"percentage": stats_dict[service][op]/visits, "visits": stats_dict[service][op]}
        return stats_dict

@app.route('/stats/<service>/<op>', methods=['GET', 'POST'])
def service_op(service, op):
    if request.method == 'GET':
        stat = get_stats_service_op(service, op)
        if stat is None:
            return make_response('Invalid input (no such service or operation)\n', 400)
        return make_response(jsonify(visits=stat), 200)
    else:
        with app.app_context():
            stat = db.session.query(Stats).filter_by(service=service, op=op).first()
            if stat is None:
                stat = Stats(service, op)
                db.session.add(stat)
            stat.visits += 1
            db.session.commit()
        return make_response('', 200)

    

@app.route('/stats/<service>')
def service(service):
    stats = get_stats_service(service)
    if stats is None:
        return make_response('Invalid input (no such service)\n', 400)
    return make_response(jsonify(stats=stats), 200)

@app.route('/stats')
def stats():
    stats = get_stats()
    return make_response(jsonify(stats=stats), 200)

def create_app():
    return app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
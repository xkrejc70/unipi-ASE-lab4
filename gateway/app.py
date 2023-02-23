import requests

from flask import Flask, render_template, request, make_response
from requests.exceptions import ConnectionError, HTTPError
from gateway.urls import *


ALLOWED_MATH_OPS = ['add', 'sub', 'mul', 'div', 'mod']
ALLOWED_STR_OPS = ['lower', 'upper', 'concat', 'editdistance']

app = Flask(__name__, instance_relative_config=True)

@app.route('/')
def index():
    return make_response('ok', 200)

@app.route('/math/<op>')
def math(op):
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if op not in ALLOWED_MATH_OPS:
        return make_response('Invalid operation\n', 404)
    try:
        x = requests.get(MATH_URL + f'/{op}?a={a}&b={b}')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Math service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)


@app.route('/str/<op>')
def string(op):
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if op not in ALLOWED_STR_OPS:
        return make_response('Invalid operation\n', 404)
    try:
        if op == 'lower' or op == 'upper':
            x = requests.get(STRING_URL + f'/{op}?a={a}')
        else:
            x = requests.get(STRING_URL + f'/{op}?a={a}&b={b}')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('String service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

@app.route('/stats')
def stats():
    try:
        x = requests.get(STATS_URL + '/stats')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Stats service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

@app.route('/stats/<service>')
def stats_service(service):
    try:
        x = requests.get(STATS_URL + f'/stats/{service}')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Stats service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

@app.route('/stats/<service>/<op>')
def stats_service_op(service, op):
    try:
        x = requests.get(STATS_URL + f'/stats/{service}/{op}')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Stats service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

def create_app():
    return app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
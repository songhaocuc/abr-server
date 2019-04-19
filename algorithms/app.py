from algorithms.bottle import route, run, request, response
from algorithms.AbrManager import AbrManager
import json


abr_manager = AbrManager()


@route('/hello')
def hello():
    return "Hello world!"


def jsonp_format(callback, data):
    return callback + '(' + json.dumps(data) + ')'


@route('/abr_init/<abr_id>')
def init_abr(abr_id):
    # response.set_header('Access-Control-Allow-Origin', '*')
    callback_str = request.query.callback
    response_entity = abr_manager.init_abr(abr_id, request.query.data)
    return jsonp_format(callback_str, response_entity)


@route('/abr_request')
def exec_abr():
    state_message = request.query.state_message
    instance_id = request.query.instance_id
    callback_str = request.query.callback
    response_entity = abr_manager.exec_abr(instance_id, state_message)
    return jsonp_format(callback_str, response_entity)


@route('/abr_clear')
def clear_abr():
    instance_id = request.query.instance_id
    callback_str = request.query.callback
    response_entity = abr_manager.clear_abr(instance_id)
    return jsonp_format(callback_str, response_entity)


run(host='localhost', port=3001, debug=True)

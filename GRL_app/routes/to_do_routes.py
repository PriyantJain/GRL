import flask
import datetime

def add_routes(app, player):
    @app.route('/to_do', methods=['GET'])
    def get_to_do():    return flask.jsonify(player.get_to_do_list())

    @app.route('/to_do/completed', methods=['GET'])
    def get_to_do_completed():    
        to_do_done = player.get_to_do_done()
        to_do_done.sort(key = lambda x : x[5], reverse = True)
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")

        lim = 0
        while lim < len(to_do_done) and to_do_done[lim][5] == _today : lim += 1
        lim = max(5, lim)
        return flask.jsonify(to_do_done[:lim])

    @app.route('/to_do', methods = ['POST'])
    def create_to_do() :
        task_name = flask.request.json.get('task_name')
        task_parent = flask.request.json.get('task_parent')
        player.TD_add(task_name, task_parent)
        response = {'status': 'success'}
        return flask.jsonify(response), 201
    
    @app.route('/to_do/<int:task_id>/name', methods=['PUT'])
    def edit_to_do_name(task_id) :
        task_name = flask.request.json.get('task_name')
        player.TD_update_name(task_id, task_name)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/to_do/<int:task_id>/track', methods=['PUT'])
    def edit_to_do_track(task_id) :
        task_track = flask.request.json.get('task_track')
        player.TD_update_track(task_id, task_track)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/to_do/<int:task_id>/complete', methods=['PUT'])
    def complete_to_do(task_id) :
        player.TD_completed(task_id)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/to_do/<int:task_id>/undo', methods=['PUT'])
    def undo_to_do(task_id) :
        player.TD_undo(task_id)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/to_do/<int:task_id>', methods=['DELETE'])
    def delete_to_do(task_id) :
        player.TD_del(task_id)
        response = {'status': 'success'}
        return flask.jsonify(response)


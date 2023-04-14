import flask
import datetime

def add_routes(app, player):
    @app.route('/GRL/to_do', methods=['GET'])
    def get_to_do():    return flask.jsonify(player.get_to_do_list())

    @app.route('/GRL/to_do/completed', methods=['GET'])
    def get_to_do_completed():    
        to_do_done = player.get_to_do_done()
        to_do_done.sort(key = lambda x : x[2], reverse = True)
        _today = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")

        lim = 0
        while lim < len(to_do_done) and to_do_done[lim][2] == _today : lim += 1
        lim = max(5, lim)
        return flask.jsonify(to_do_done[:lim])

    @app.route('/GRL/to_do', methods = ['POST'])
    def create_to_do() :
        task_name = flask.request.json.get('task_name')

        player.TD_add(task_name)
        
        response = {'status': 'success'}
        return flask.jsonify(response), 201
    
    @app.route('/GRL/to_do/<int:task_id>', methods=['PUT'])
    def edit_to_do(task_id) :
        task_name = flask.request.json.get('task_name')
        
        player.TD_update(task_id, task_name)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/GRL/to_do/<int:task_id>/complete', methods=['PUT'])
    def complete_to_do(task_id) :
        player.TD_completed(task_id)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/GRL/to_do/<int:task_id>/undo', methods=['PUT'])
    def undo_to_do(task_id) :
        player.TD_undo(task_id)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/GRL/to_do/<int:task_id>', methods=['DELETE'])
    def delete_to_do(task_id) :
        player.TD_del(task_id)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

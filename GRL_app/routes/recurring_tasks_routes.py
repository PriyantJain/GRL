import flask

def add_routes(app, player):
    @app.route('/RT', methods=['GET'])
    def get_recurring_tasks():    return flask.jsonify(player.get_RT_list())

    @app.route('/RT/completed', methods=['GET'])
    def get_RT_completed():    return flask.jsonify(player.get_RT_done())

    @app.route('/RT', methods = ['POST'])
    def create_RT() :
        task_name = flask.request.json.get('task_name')
        task_points = flask.request.json.get('task_points')
        task_parent = flask.request.json.get('task_parent')
        
        player.RT_add(task_name, task_points, task_parent)
        
        response = {'status': 'success'}
        return flask.jsonify(response), 201
    
    @app.route('/RT/<int:task_id>/details', methods=['PUT'])
    def edit_RT_details(task_id) :
        task_name = flask.request.json.get('task_name')
        task_points = flask.request.json.get('task_points')
        player.RT_update_details(task_id, task_name, task_points)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/RT/<int:task_id>/track', methods=['PUT'])
    def edit_RT_track(task_id) :
        task_track = flask.request.json.get('task_track')
        player.RT_update_track(task_id, task_track)
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/RT/<int:task_id>/complete', methods=['PUT'])
    def complete_RT(task_id) :
        player.RT_completed(task_id)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/RT/<int:task_id>/undo', methods=['PUT'])
    def undo_RT(task_id) :
        player.RT_undo(task_id)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/RT/<int:task_id>', methods=['DELETE'])
    def delete_RT(task_id) :
        player.RT_del(task_id)
        
        response = {'status': 'success'}
        return flask.jsonify(response)

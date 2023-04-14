import flask

def add_routes(app, player):
    @app.route('/GRL/register_ET', methods = ['POST'])
    def register_ET() :
        task_name = flask.request.json.get('task_name')
        task_points = flask.request.json.get('task_points')
        
        player.ET(task_name, task_points)

        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/GRL/register_Standard_Task', methods = ['POST'])
    def register_Standard_Task() :
        task_name = flask.request.json.get('task_name')
        task_value = flask.request.json.get('task_value')
        
        player.StandardTasksSubmit(task_name, task_value)

        response = {'status': 'success'}
        return flask.jsonify(response)
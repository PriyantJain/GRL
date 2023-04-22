import flask

def add_routes(app, player):
    @app.route('/GRL/register_Daily_Task', methods = ['POST', 'PUT'])
    def register_Daily_Task() :
        task_no = flask.request.json.get('task_no')
        task_name = flask.request.json.get('task_name')
        
        player.DtCreateSubmit(task_no, task_name)

        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/GRL/daily_task/<int:task_no>', methods = ['PUT'])
    def toggle_daily_task(task_no) :
        if task_no == 1 : player.dt1_done = 1 - player.dt1_done
        elif task_no == 2 : player.dt2_done = 1 - player.dt2_done
        else : player.dt3_done = 1 - player.dt3_done

        response = {'status': 'success'}
        return flask.jsonify(response)
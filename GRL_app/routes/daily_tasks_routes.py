import flask

def add_routes(app, player):
    @app.route('/daily_task', methods = ['POST'])
    def register_Daily_Task() :
        task_no = flask.request.json.get('task_no')
        task_name = flask.request.json.get('task_name')
        
        player.DtCreateSubmit(task_no, task_name)

        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/daily_task/<int:task_no>', methods = ['PUT'])
    def toggle_daily_task(task_no) :
        if task_no == 1 : player.dt1_done = 1 - player.dt1_done
        elif task_no == 2 : player.dt2_done = 1 - player.dt2_done
        else : player.dt3_done = 1 - player.dt3_done

        response = {'status': 'success'}
        return flask.jsonify(response)

    @app.route('/daily_task/<int:task_no>', methods = ['GET'])
    def daily_task(task_no) :
        ''' GET API call function for daily tasks with given task_no
            Returns details of daily task : (name, completion status)'''
        if task_no == 1 : return flask.jsonify((player.dt1, player.dt1_done))
        elif task_no == 2 : return flask.jsonify((player.dt2, player.dt2_done))
        elif task_no == 3 : return flask.jsonify((player.dt3, player.dt3_done))

        return flask.jsonify('BAD PARAMETER'), 400
import {get_query} from './common_funtions.js';

// Post call 'register_ET' API to register extra task with given name, points
export function register_ET(taskName, taskPoints) {
    fetch('/register_ET', get_query('POST', {
        task_name: taskName,
        task_points: taskPoints
    }))
    .then(response => {
        if (!response.ok) throw new Error('POST request for register_ET failed');
        window.location.reload();
    })
    .catch(error => console.error(error));
}


// Post call 'register_Standard_Task' API to register standard task with given name, value
export function register_standard_tasks(taskName, taskValue) {
    fetch('/register_Standard_Task', get_query('POST', {
        task_name: taskName,
        task_value: taskValue
    }))
    .then(response => {
        if (!response.ok) throw new Error('POST request for register_Standard_Task failed');
        window.location.reload();
    })
    .catch(error => console.error(error));
}

document.getElementById('register_ET').addEventListener('click', function() {
    const taskName = document.getElementById('ET_task_name').value;
    const taskPoints = document.getElementById('ET_points_change').value;
    register_ET(taskName, taskPoints);
});

document.getElementById('StandardTasksSubmit').addEventListener('click', function() {
    const taskName = document.getElementById('StandardTasks').value;
    const taskValue = document.getElementById('StandardTasksValue').value;
    register_standard_tasks(taskName, taskValue);
});
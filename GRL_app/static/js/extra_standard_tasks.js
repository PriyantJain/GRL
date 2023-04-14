import {get_query} from './common_funtions.js';

export function register_ET(taskName, taskPoints) {
    fetch('/GRL/register_ET', get_query('POST', {
        task_name: taskName,
        task_points: taskPoints
    }))
    .then(response => {
        if (!response.ok) throw new Error('POST request for register_ET failed');
        
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

export function register_standard_tasks(taskName, taskValue) {
    fetch('/GRL/register_Standard_Task', get_query('POST', {
        task_name: taskName,
        task_value: taskValue
    }))
    .then(response => {
        if (!response.ok) throw new Error('POST request for register_Standard_Task failed');

        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

document.getElementById('register_ET').addEventListener('click', function() {
    const taskName = document.getElementById('ExtraTask').value;
    const taskPoints = document.getElementById('ExtraTaskPoints').value;
    register_ET(taskName, taskPoints);
});

document.getElementById('StandardTasksSubmit').addEventListener('click', function() {
    const taskName = document.getElementById('StandardTasks').value;
    const taskValue = document.getElementById('StandardTasksValue').value;
    register_standard_tasks(taskName, taskValue);
});
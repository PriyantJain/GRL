import { get_query} from './common_funtions.js';

// Post call to 'daily_task' to register new daily task with given No, Name
export function register_daily_task(taskNo, taskName) {
    fetch('/daily_task', get_query('POST', {
        task_no: taskNo,
        task_name: taskName
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('POST request for register_daily_task failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// Put call to 'daily_task' to toggle status of daily task with given No
export function toggle_daily_task(taskNo) {
    fetch(`/daily_task/${taskNo}`, get_query('PUT'))
    .then(response => {
        if (!response.ok) {
            throw new Error('POST request for register_daily_task failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

document.getElementById('register_DT').addEventListener('click', function() {
    if (confirm('Really want to add/overwrite Daily Task?')) {
        const taskNo = document.getElementById('DT_task_no').value;
        const taskName = document.getElementById('DT_task_name').value;
        register_daily_task(taskNo, taskName);
    }
});

document.getElementById('DT_B1').addEventListener('click', function() {toggle_daily_task(1)});
document.getElementById('DT_B2').addEventListener('click', function() {toggle_daily_task(2)});
document.getElementById('DT_B3').addEventListener('click', function() {toggle_daily_task(3)});
import {get_query} from './common_funtions.js';

// POST call to 'RT' api to create recurring task with given name, points
export function create_RT(taskName, taskPoints){
    fetch('/RT', get_query('POST', {
        task_name: taskName,
        task_points: taskPoints
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('POST request for create_RT failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// PUT call to 'RT/<taskNo>' api to edit recurring task with given no
export function edit_RT(taskNo, taskName, taskPoints){
    fetch(`/RT/${taskNo}`, get_query('PUT', {
        task_no: taskNo,
        task_name: taskName,
        task_points: taskPoints
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for edit_RT failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// PUT call to 'RT/<taskNo>/complete' api to mark recurring task with given no as complete
export function complete_RT(taskNo){
    fetch(`/RT/${taskNo}/complete`, get_query('PUT'))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for complete_RT failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// PUT call to 'RT/<taskNo>/undo' api to mark recurring task with given no as not complete
export function undo_RT(taskNo){
    fetch(`/RT/${taskNo}/undo`, get_query('PUT'))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for undo_RT failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// DELETE call to 'RT/<taskNo>' api to delete recurring task with given no
export function delete_RT(taskNo){
    fetch(`/RT/${taskNo}`, get_query('DELETE'))
    .then(response => {
        if (!response.ok) {
            throw new Error('DELETE request for delete_RT failed');
        }
        window.location.reload();
    })
    .catch(error => console.error(error));
}

// function to handle edit button for recurring tasks
export function RT_edit_button_handler(_id) {
    if (document.getElementsByName('RT_task_' + _id)[0].contentEditable == 'true') {
        let taskName = document.getElementsByName('RT_task_' + _id)[0].textContent;
        let taskPoints = document.getElementsByName('RT_points_' + _id)[0].textContent;
        let taskNo = _id;
        edit_RT(taskNo, taskName, taskPoints);
    }
    else {
        document.getElementsByName('RT_task_' + _id)[0].contentEditable = true;
        document.getElementsByName('RT_points_' + _id)[0].contentEditable = true;
    }
}

// function to add onclick function to register_RT button
document.getElementById('register_RT').addEventListener('click', function() {
    const taskName = document.getElementById('RT_task_name').value;
    const taskPoints = document.getElementById('RT_task_points').value;
    create_RT(taskName, taskPoints);
});

// add click event listener to each button for editing to do
const edit_buttons_RT = document.querySelectorAll('#RT_edit_btn');
edit_buttons_RT.forEach(button => {
    button.addEventListener('click', function() {
        const buttonNumber = parseInt(button.value);
        RT_edit_button_handler(buttonNumber);
    });
});

// add click event listener to each button for completing to do
const completed_buttons_RT = document.querySelectorAll('#RT_completed_btn');
completed_buttons_RT.forEach(button => {
    button.addEventListener('click', function() {
        const taskNo = parseInt(button.value);
        complete_RT(taskNo);
    });
});

// add click event listener to each button for undo to do
const undo_buttons_RT = document.querySelectorAll('#RT_undo_btn');
undo_buttons_RT.forEach(button => {
    button.addEventListener('click', function() {
        const taskNo = parseInt(button.value);
        undo_RT(taskNo);
    });
});

// add click event listener to each button for deleting to do
const delete_buttons_RT = document.querySelectorAll('#RT_delete_btn');
delete_buttons_RT.forEach(button => {
    button.addEventListener('click', function() {
        if (confirm('Really want to delete this recurring task?')){
            const taskNo = parseInt(button.value);
            delete_RT(taskNo);
        }
    });
});


import {get_query} from './common_funtions.js';

export function create_to_do(taskName, taskParent){
    fetch('/GRL/to_do', get_query('POST', {
        task_name: taskName,
        task_parent : taskParent
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('POST request for create_to_do failed');
        }
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

export function edit_to_do_name(taskNo, taskName){
    fetch(`/GRL/to_do/${taskNo}/name`, get_query('PUT', {
        task_no: taskNo,
        task_name: taskName,
        // task_track: taskTrack
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for edit_to_do failed');
        }
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

export function edit_to_do_track(taskNo, taskTrack){
    fetch(`/GRL/to_do/${taskNo}/track`, get_query('PUT', {
        task_no: taskNo,
        // task_name: taskName,
        task_track: taskTrack
    }))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for edit_to_do failed');
        }
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

export function complete_to_do(taskNo){
    fetch(`/GRL/to_do/${taskNo}/complete`, get_query('PUT'))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for complete_to_do failed');
        }
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

export function undo_to_do(taskNo){
    fetch(`/GRL/to_do/${taskNo}/undo`, get_query('PUT'))
    .then(response => {
        if (!response.ok) {
            throw new Error('PUT request for undo_to_do failed');
        }
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

export function delete_to_do(taskNo){
    fetch(`/GRL/to_do/${taskNo}`, get_query('DELETE'))
    .then(response => {
        if (!response.ok) {
            throw new Error('DELETE request for delete_to_do failed');
        }
        if (window.location.href.endsWith('/GRL')) window.location.reload();
        else window.location.href = window.location.href + 'GRL';
    })
    .catch(error => console.error(error));
}

// function for handling edit button in To Do
export function TD_edit_button_handler(_id) {
    if (document.getElementsByName('TD_' + _id)[0].contentEditable == 'true') {
        let taskName = document.getElementsByName('TD_' + _id)[0].textContent;
        let taskNo = _id;
        // let taskTrack = parseInt(document.getElementsByName('TD_track_' + _id)[0].getAttribute('value'));
        edit_to_do_name(taskNo, taskName);
    }
    else {
        document.getElementsByName('TD_' + _id)[0].contentEditable = true;
    }
}


document.getElementById('register_TD').addEventListener('click', function() {
    const taskParent = document.getElementById('TD_parent').value;
    const taskName = document.getElementById('TD_task_name').value;
    create_to_do(taskName, taskParent);
});

// add click event listener to each button for editing to do
const edit_buttons_TD = document.querySelectorAll('#TD_edit_btn');

edit_buttons_TD.forEach(button => {
    button.addEventListener('click', function() {
        const buttonNumber = parseInt(button.value);
        TD_edit_button_handler(buttonNumber);
    });
});

// add click event listener to each button for completing to do
const completed_buttons_TD = document.querySelectorAll('#TD_completed_btn');

completed_buttons_TD.forEach(button => {
    button.addEventListener('click', function() {
        const taskNo = parseInt(button.value);
        complete_to_do(taskNo);
    });
});

// add click event listener to each button for undo to do
const undo_buttons_TD = document.querySelectorAll('#TD_undo_btn');

undo_buttons_TD.forEach(button => {
    button.addEventListener('click', function() {
        const taskNo = parseInt(button.value);
        undo_to_do(taskNo);
    });
});

// add click event listener to each button for deleting to do
const delete_buttons_TD = document.querySelectorAll('#TD_delete_btn');

delete_buttons_TD.forEach(button => {
    button.addEventListener('click', function() {
        if (confirm('Really want to delete To Do?')){
            const taskNo = parseInt(button.value);
            delete_to_do(taskNo);
        } 
    });   
});

// helper for filling parent cell in modal pop up in TO DO  
const modal_new_TD = document.getElementById('modal_new_TD')
modal_new_TD.addEventListener('show.bs.modal', event => {
    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const parent = button.getAttribute('data-bs-parent')
    // Update the modal's content.
    const modalBodyInputParent = modal_new_TD.querySelector('#TD_parent')

    modalBodyInputParent.value = parent
})

// add click event listener to fasttrack buttons in to do
const fasttrack_buttons = document.querySelectorAll('#fasttrack');
fasttrack_buttons.forEach(button => {
    button.addEventListener('click', function() {
        const button_name = button.getAttribute("name");
        const _id = parseInt(button_name.split('_')[2]);
        // const taskName = document.getElementsByName('TD_' + _id)[0].textContent;
        const taskTrack = parseInt(button.getAttribute('value'));

        edit_to_do_track(_id, 1 - taskTrack);
    });   
});

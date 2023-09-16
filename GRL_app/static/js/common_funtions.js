export function get_query(_method, body = {}) {
    return {
        method: _method,
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }
}

export function show_error_popup(msg) {
    document.getElementById("API_err_modal_msg").textContent = msg + '\nPlease reload page.';
    let errModal = new bootstrap.Modal(document.getElementById("API_err_modal"))
    errModal.show();
}
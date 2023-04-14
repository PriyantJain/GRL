export function get_query(_method, body = {}) {
    return {
        method: _method,
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }
}
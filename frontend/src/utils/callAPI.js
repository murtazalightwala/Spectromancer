

let host = "http://127.0.0.1:8000"


export default function callAPI(url, method, headers, payload, callback) {
    return (
        fetch(host + url, {method: method, headers: headers, body: payload} )
    )
}



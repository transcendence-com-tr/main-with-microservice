let apiURL = "http://localhost:8000/api";
let token = localStorage.getItem("token") ?? "";

async function request(method, action, data=null)
{
    console.log(data)
    console.log(JSON.stringify(data))
    let response = await fetch(apiURL + "/" +  action, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}

async function post(action, data = null)
{
    return request("POST", action, data);
}

async function get(action, data = null)
{
    return request("GET", action, data);
}

async function put(action, data = null)
{
    return request("PUT", action, data);
}

async function del(action, data = null)
{
    return request("DELETE", action, data);
}


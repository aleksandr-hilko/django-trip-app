import { CSRF_TOKEN } from "./csrf_token.js"

async function apiService(endpoint, method, data) {
  // D.R.Y. code to make HTTP requests to the REST API backend using fetch
  const config = {
    method: method || "GET",
    body: data !== undefined ? JSON.stringify(data) : null,
    headers: {
      'content-type': 'application/json',
      'X-CSRFTOKEN': CSRF_TOKEN
    }
  };
  try {
    let r = await fetch(endpoint, config)
    if (r.status === 500) {
      return { valid: r.ok, status: r.status, body: "" }
    }
    else {
      return r.json()
        .then(data => ({ valid: r.ok, status: r.status, body: data }))
    }
  }
  catch (error) {
    return console.log(error);
  }
}

export { apiService };
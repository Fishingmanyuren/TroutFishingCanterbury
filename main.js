const paragraph = document.getElementById("paragraph");

console.log(document.getElementById("paragraph"));

const API_BASE = 'http://localhost:3000/api';

async function apiRequest(method, path, body = null, requiresAuth = false) {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (requiresAuth){
      const token = getToken();
      if (token){
        headers['Authorization'] = `Bearer ${token}`;
      }
    }
    
    const options = {
      method,
      headers,
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`$(API_BASE)${path}`, options);

    if (response.status === 204) {
      return null;
    }

    const data = await response.json();

    if(response.ok) {
      throw new Error(data.error || 'Request failed');
    }

    return data;
}

const Api = {
  getArticles: () => apiRequest('GET', '/articles'),
}
<<<<<<< HEAD
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
=======
const paragraph = document.getElementById("paragraph");
const API_BASE = 'http://localhost:3000/api';
const loginModal = document.getElementById('loginModal');
const loginEmail = document.getElementById('loginEmail')
const loginPassword = document.getElementById('loginPassword')

document.getElementById("login").addEventListener('click', async(e) =>{
  loginModal.classList.add('show');
})

document.getElementById("closeBtn").addEventListener('click', async(e) =>{
  loginModal.classList.remove('show');
})


document.getElementById("submitAuth").addEventListener('click', async (e) =>{
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();
  const requestBody = {
    "email": email,
    "password": password,
  };
  try{
    const response = await fetch('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });
    
    const data = await response.json();
    const token = data.access_token;
    console.log(token);
    if (response.ok){
      alert('Login Successful!');
      loginEmail.value = "";
      loginPassword.value = "";
      loginModal.classList.remove('show');
      localStorage.setItem(token);
      console.log(token);
    }else{
      alert('Login failed.');
    }
  }catch (error){
    console.error('Request failed: ', error);
  }
});
>>>>>>> 534f6879061213b32e447fc4021a170b07c64c42

const paragraph = document.getElementById("paragraph");
const API_BASE = 'http://localhost:3000/api';
const loginModal = document.getElementById('loginModal');
const registerModal = document.getElementById('registerModal');
const loginEmail = document.getElementById('loginEmail');
const loginPassword = document.getElementById('loginPassword');
const registerEmail = document.getElementById('registerEmail');
const registerPassword = document.getElementById('registerPassword');

document.getElementById("login").addEventListener('click', async(e) =>{
  loginModal.classList.add('show');
})

document.getElementById("closeLogin").addEventListener('click', (e) =>{
  loginModal.classList.remove('show');
})

document.getElementById("register").addEventListener('click', async(e) =>{
  registerModal.classList.add('show');
})

document.getElementById("closeRegister").addEventListener('click', (e) =>{
  registerModal.classList.remove('show');
})

window.addEventListener("DOMContentLoaded", async() =>{
    const access_token = sessionStorage.getItem("access_token");
    if (access_token != null){
      document.getElementById('login').innerText = "Logged In"
    }
});

document.getElementById("submitAuth").addEventListener('click', async (e) =>{
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  if(email == ""){
    alert("Email or password cannot be blank!")
  }else if(password == ""){
    alert("Email or password cannot be blank!")
  }else{

  const requestBody = {
    "email": email,
    "password": password,
  };
  
  try{
    const response = await fetch('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json',
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
      sessionStorage.setItem('access_token', token);
      document.getElementById('login').innerText = "Logged In"
    }else{
      alert('Login failed. Please check your email and password and try again.');
    }
  }catch (error){
    console.error('Request failed: ', error);
  }
}});

document.getElementById("submitRegister").addEventListener('click', async (e) =>{
  const email = document.getElementById("registerEmail").value.trim();
  const password = document.getElementById("registerPassword").value.trim();

  if(email == ""){
    alert("Email or password cannot be blank!")
  }else if(password == ""){
    alert("Email or password cannot be blank!")
  }else if(password.length <6){
    alert("Password should not be shorter than 6 characters!")
  }else{

  const requestBody = {
    "email": email,
    "password": password,
  };
  try{
    const response = await fetch('http://localhost:3000/api/auth/register', {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });
    
    if (response.ok){
      alert('Request sent! Check your email to confirm your email address.');
      registerEmail.value = "";
      registerPassword.value = "";
      registerModal.classList.remove('show');
    }else{
      alert('Registration Failed. Please try again.');
    }
  }catch (error){
    console.error('Request failed: ', error);
  }
}});
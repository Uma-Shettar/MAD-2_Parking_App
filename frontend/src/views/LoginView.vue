<template>
    <div><h1 class = "text-center" style="color: #07567d;">Login</h1></div>
    <div class="container-fluid row justify-content-center">
        <form @submit.prevent="Login" class="col-md-4">

            <div class="mb-3">
                <label for="exampleFormControlInput1" class="form-label">Email address</label>
                <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com" name="email" v-model="email">
            </div>

            <div class="mb-3">
                <label for="inputPassword5" class="form-label">Password</label>
                <input type="password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock" name="password" v-model="password" @input="Help"/>
                <div id="passwordHelpBlock" class="form-text" > {{  passwordlength }} </div>
                <div id="passwordHelpBlock" class="form-text" > {{ passwordat }} </div>
            </div>

            <div>
                <button type="submit" class="btn btn-primary">Login</button>
                <a href="/register">Create new user?</a>
            </div>
            
        </form>
    </div>
</template>


<script setup>

import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref('');
const password = ref('');

const passwordlength = ref('');
const passwordat = ref('');

const Help = () => {
    let validity = true;
    if (password.value.length < 8) {
        passwordlength.value = 'Password must be at least 8 characters long';
        validity = false;
    }
    else {
        passwordlength.value = '';
    }
    
    if (!password.value.includes('@')) {
        passwordat.value = 'Password must contain an "@" symbol';
        validity = false;
    } else {
        passwordat.value = '';
    }
    return validity;
}

async function Login() {
    if (!(Help())) {
        alert('Invalid password');
        return;
    }

    if (email.value === '' || password.value === '') {
        alert('Please fill in all fields');
        return;
    }

    
    const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });

    console.log(response);
    
    if(!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
        return;
    }
    else {
        const data = await response.json();
        console.log(data);
        localStorage.setItem('token', data.user.auth_token);
        alert(data.message);
        if (data.user.roles.includes('admin')) {
            router.push('/admin-dashboard');
        } 
        else {
            router.push('/user-dashboard');
        }

    }
    
}
</script>
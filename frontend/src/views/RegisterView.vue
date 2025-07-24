<template>
    <div><h1 class = "text-center" style="color: #07567d;">Register</h1></div>
<div class="container-fluid row justify-content-center">
    <form class = "col-5" @submit.prevent="Register">

        <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Email address</label>
            <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com" name="email" v-model="email">
        </div>

        <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Name</label>
            <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1" name = "username" v-model="username">
        </div>

        <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Password</label>
            <input type="password" class="form-control" placeholder="Password" aria-label="Password" aria-describedby="basic-addon1" name = "password" v-model="password" @input="Help"/>
            <div id="passwordHelpBlock" class="form-text">{{ passwordlength }}</div>
            <div id="passwordHelpBlock" class="form-text">{{ passwordat }}</div>
        </div>

        <div class="mb-3">
            <label for="exampleFormControlInput1" class="form-label">Confirm Password</label>
            <input type="password" class="form-control" placeholder="Confirm Password" aria-label="Confirm Password" aria-describedby="basic-addon1" name = "confirm_password" v-model="confirm_password" @input="CheckConfirmPassword"/>
            <div id="passwordHelpBlock" class="form-text">{{ ConfirmPassword }}</div>
        </div>

        <div>
            <button type="submit" class="btn btn-primary">Register</button>
            <a href="/login">Already have an account?</a>
        </div>
        
    </form>
</div>
</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref('');
const username = ref('');
const password = ref('');
const confirm_password = ref('');

const passwordlength = ref('');
const passwordat = ref('');
const ConfirmPassword = ref('');

const Help = () => {
    let validity = true;
    if (password.value.length < 8) {
        passwordlength.value = 'Password must be at least 8 characters long';
        validity = false;
    } else {
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

const CheckConfirmPassword = () => {
    if (password.value !== confirm_password.value) {
        ConfirmPassword.value = 'Passwords do not match';
        return false;
    } else {
        ConfirmPassword.value = '';
        return true;
    }
}

async function Register() {
    if (!(Help()) || ConfirmPassword.value !== '') {
        alert('Invalid input');
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value,
            name: username.value,
            password: password.value
        })
    });
    if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
        return;
    }
    router.push('/login');
}
</script>
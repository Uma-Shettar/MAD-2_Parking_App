<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useRouter } from 'vue-router';
import { AuthStore } from './stores/authentication';

const router = useRouter();

async function logout() {
    localStorage.removeItem('token');
    const response = await fetch('http://127.0.0.1:5000/api/logout', {
        method: 'POST',
        mode : 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':AuthStore().get_authtoken()
        }
    })
    alert('You have been logged out');
    router.push('/login');
}

</script>

<template>
<nav class="navbar navbar-expand-lg " style="background-color: rgb(8, 155, 247); min-height: 72px;">
  <div class="container-fluid">
    <img src="../static/logo.png" alt="Logo" width="40" height="40" style="border-radius: 81px; margin-right: 10px;" class="d-inline-block align-text-top">
    <li class="nav-item" v-if="AuthStore().get_roles() == 'admin'">
      <RouterLink class="navbar-brand" to="/admin-dashboard">Parking App</RouterLink>
    </li>
    <li class="nav-item" v-else>
    <RouterLink class="navbar-brand" to="/user-dashboard" >Parking App</RouterLink>
    </li>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarScroll">
      <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
        <li class="nav-item" v-if="!AuthStore().get_authtoken()">
          <RouterLink class="nav-link active" aria-current="page" to="/login" style="font-size: 18px;">Login</RouterLink>
        </li>
        <li class="nav-item" v-if="!AuthStore().get_authtoken()">
          <RouterLink class="nav-link active" aria-current="page" to="/register"style="font-size: 18px;">Register</RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_roles() == 'admin'">
          <RouterLink class="nav-link active" aria-current="page" to="/users" style="font-size: 18px;">Users</RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_roles() == 'admin'">
          <RouterLink class="nav-link active" aria-current="page" to="/parkingrecords" style="font-size: 18px;"> Parking Records</RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_authtoken()">
          <a class="nav-link active" aria-current="page" @click="logout" style="font-size: 18px;">Logout</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
<RouterView/>
</template>


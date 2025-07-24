<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useRouter } from 'vue-router';

const router = useRouter();

async function logout() {
    localStorage.removeItem('token');
    alert('You have been logged out');
    router.push('/login');
}

</script>

<template>
<nav class="navbar navbar-expand-lg " style="background-color: rgb(8, 155, 247); min-height: 72px;">
  <div class="container-fluid">
    <img src="../static/logo.png" alt="Logo" width="40" height="40" style="border-radius: 81px; margin-right: 10px;" class="d-inline-block align-text-top">
    <RouterLink class="navbar-brand" to="/">Parking App</RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarScroll">
      <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
        <li class="nav-item">
          <RouterLink class="nav-link active" aria-current="page" to="/login" style="font-size: 18px;">Login</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link active" aria-current="page" to="/register"style="font-size: 18px;">Register</RouterLink>
        </li>
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#"style="font-size: 18px;">Users</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#"style="font-size: 18px;"> Parking Records</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" @click="logout" style="font-size: 18px;">Logout</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
<RouterView/>
</template>


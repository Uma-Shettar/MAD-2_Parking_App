<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useRouter } from 'vue-router';
import { AuthStore } from './stores/authentication';
import { ref } from 'vue';

const router = useRouter();

const search = ref('');
const search_type = ref('');

const Search = () => {
  console.log('Search term:', search.value);      
  console.log('Search type:', search_type.value); 
  router.push(`/adminsearch/${search.value}/${search_type.value}`);
};

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
    <img src="@/assets/logo.png" alt="Logo" width="40" height="40" style="border-radius: 81px; margin-right: 10px;" class="d-inline-block align-text-top">
    <li class="nav-item" v-if="AuthStore().get_roles() == 'admin' && AuthStore().get_authtoken()">
      <RouterLink class="navbar-brand" to="/admin-dashboard">Parking App</RouterLink>
    </li>
    <li class="nav-item" v-else-if="AuthStore().get_roles() == 'user' && AuthStore().get_authtoken()">
      <RouterLink class="navbar-brand" to="/user-dashboard" >Parking App</RouterLink>
    </li>
    <li class="nav-item" v-else-if="!AuthStore().get_authtoken()">
      <RouterLink class="navbar-brand" to="/" >Parking App</RouterLink>
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
        <li class="nav-item" v-if="AuthStore().get_roles() == 'admin' && AuthStore().get_authtoken()">
          <RouterLink class="nav-link active" aria-current="page" to="/users" style="font-size: 18px;">Users</RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_roles() == 'admin' && AuthStore().get_authtoken()">
          <RouterLink class="nav-link active" aria-current="page" to="/parkingrecords" style="font-size: 18px;"> Parking Records</RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_roles() == 'admin' && AuthStore().get_authtoken()">
          <RouterLink class="nav-link active" aria-current="page" to="/adminchart" style="font-size: 18px;"> Summary </RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_roles() == 'user' && AuthStore().get_authtoken()">
          <RouterLink class="nav-link active" aria-current="page" to="/userchart" style="font-size: 18px;"> Summary </RouterLink>
        </li>
        <li class="nav-item" v-if="AuthStore().get_authtoken()">
          <a class="nav-link active" aria-current="page" @click="logout" style="font-size: 18px;">Logout</a>
        </li>
      </ul>
      <form v-if="AuthStore().get_roles() == 'admin' && AuthStore().get_authtoken()" class="d-flex" role="search" @submit.prevent="Search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search" v-model="search">
              <select class="form-select me-2" aria-label="Default select example" name="search_type" v-model="search_type">
                <option selected>Select</option>
                <option value="location">location</option>
                <option value="pincode">pincode</option>
                <option value="available">available</option>
                <option value="occupied">occupied</option>
                <option value="username">username</option>
                <option value="email">email</option>
              </select>
            <input class="btn btn-outline-success" type="submit" value="Search">
          </form>
    </div>
  </div>
</nav>
<RouterView/>
</template>


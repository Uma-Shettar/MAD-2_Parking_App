import {ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const AuthStore = defineStore('authentication', () => {
  const token = ref(localStorage.getItem('token') || null);
  const user = ref(null);

  const isAuthenticated = computed(() => {
    return token.value !== null;
  });

  function setCred(newToken, userData) {
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(userData));
    token.value = newToken;
    user.value = userData;
  }

  function clearToken() {
    token.value = null;
    localStorage.removeItem('token');
  }

  function get_name() {
    if (user.value) {
      return user.value.name;
    } else {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        user.value = JSON.parse(storedUser);
        return user.value.name;
      }
      console.error('Error passing user data');
      return (null);
    }
  }

    function get_email() {
    if (user.value) {
      return user.value.email;
    } else {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        user.value = JSON.parse(storedUser);
        return user.value.email;
      }
        console.error('Error passing user data');
      return null;
    }
  }

  function get_authtoken() {
    if (token.value) {
      return token.value;
    } else {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        token.value = storedToken;
        return token.value;
      }
        console.error('Error passing token data');
      return null;
    }
  }
  function get_roles() {
    if (user.value && user.value.roles) {
      return user.value.roles;
    } else {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        user.value = JSON.parse(storedUser);
        return user.value.roles;
      }
      console.error('Error passing roles data');
      return null;
    }
  }


  return { token, user, isAuthenticated, setCred, clearToken, get_name, get_email, get_authtoken, get_roles};
}   );
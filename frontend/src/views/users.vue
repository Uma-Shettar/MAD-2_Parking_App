<template>
    <div>
    <div class="card border-primary m-5">
        <div class="card-body">
            <h3 class="text-center" style="color:  #07567d;">Users </h3>
            <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
            <table class="table table-hover" style="text-align: center;">
                <thead >
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Frequency</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="user in users" :key="user.id" >
                    <td>{{ user.id }}</td>
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.frequency }}</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
</template>



<script setup>
import { ref, onMounted} from 'vue';
import { useRouter } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const users = ref([]);

const fetchUsers = async () => {

    if(!authStore.get_authtoken()){
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    try {
        const response = await fetch('http://127.0.0.1:5000/api/users', {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        users.value = data;
    } catch (error) {
        console.error('Error fetching users:', error);
    }
};
onMounted(() => {
    fetchUsers();
});

</script>
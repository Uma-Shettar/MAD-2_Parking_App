<template>
    <h3 class="text-center" style="color: #07567d;">Search Results</h3>

    <div>
    <div class="card border-primary m-5">
        <div class="card-body">
            <h3 class="text-center" style="color: #07567d;">Parking Lots </h3>
            <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
            <table class="table table-hover">
                <thead>
                    <tr v-if="search_type == 'location' || search_type == 'pincode'">
                        <th scope="col">ID</th>
                        <th scope="col"> Address </th>
                        <th scope="col"> Availability </th>
                    </tr>
                    <tr v-if="search_type == 'available' || search_type == 'occupied'">
                        <th scope="col">ID</th>
                        <th scope="col"> Lot Name </th>
                        <th scope="col"> Price </th>
                    </tr>
                    <tr v-if="search_type == 'username' || search_type == 'email'">
                        <th scope="col">ID</th>
                        <th scope="col">Name</th>
                        <th scope="col">Email</th>
                        <th scope="col">Frequency</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="search_type == 'location' || search_type == 'pincode'" v-for="r in results" :key="r.id">
                        <td>{{ r.id }}</td>
                        <td>{{ r.address }}</td>
                        <td>{{ r.availability }}</td>
                    </tr>
                    <tr v-if="search_type == 'available' || search_type == 'occupied'" v-for="r in results" :key="r.id">
                        <td>{{ r.id }}</td>
                        <td>{{ r.lot_name }}</td>
                        <td>{{ r.price }}</td>
                    </tr>
                    <tr v-if="search_type == 'username' || search_type == 'email'" v-for="r in results" :key="r.id">
                        <td>{{ r.id }}</td>
                        <td>{{ r.name }}</td>
                        <td>{{ r.email }}</td>
                        <td>{{ r.frequency }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    </div>

</template>


<script setup>
import { useRoute, useRouter } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const route = useRoute();

const router = useRouter();
const search = ref('');
const search_type = ref('');

const results = ref([]);

const fetchResults = async (searchp, search_typep) => { 
    if (!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    search.value = route.params.search;
    search_type.value = route.params.search_type;
    const response = await fetch(`http://127.0.0.1:5000/api/adminsearch/${search.value}/${search_type.value}`, {
        method: 'GET',
        mode : 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':AuthStore().get_authtoken()
        }
    });
    if (!response.ok) {
        alert('Failed to fetch results');
        console.error('Failed to fetch results');
        router.push('/admin-dashboard');
    }
    const data = await response.json();
    results.value = data;
};

onMounted(() => {
    fetchResults();
});
watch(() => route.params.search, () => {
    fetchResults();
});
watch(() => route.params.search_type, () => {
    fetchResults();
});

</script>
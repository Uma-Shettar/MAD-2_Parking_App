<template>
    <div><h1 class = "text-center" style="color: #07567d;">View Spot</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent>
            <div class="mb-3">
                <label for="spot_id" class="form-label">Spot Id</label>
                <input type="text" class="form-control" id="spot_id" name="spot_id" v-model="spot.id" readonly>
            </div>
            <div class="mb-3">
                <label for="status" class="form-label">Status</label>
                <input type="text"  class="form-control" id="status" name="status" v-model="spot.status" readonly>
            </div>
            <div class="mb-3">
                <button v-if="spot.status == 'O'" class="btn btn-outline-success m-1" type="button" @click="Viewdetails(spot.id)"role="View">View Details</button>
                <button v-else class="btn btn-outline-danger m-1" type="button" @click="DeleteSpot(spot.id)" role="Delete">Delete</button>
                <a class="btn btn-outline-primary m-1" @click="router.push('/admin-dashboard')" role="Edit">Cancel</a>
            </div>
        </form>
    </div>
</template>


<script setup>

import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const route = useRoute();

const spot = ref({
    id: '',
    status: ''
});
const spot_id = ref('');

const fetchSpotDetails = async () => {
    if(!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }

    if(!route.params.spot_id) {
        console.error('No spot ID provided');
        router.push('/admin-dashboard');
        return;
    }

    spot_id.value = route.params.spot_id;


    try {
        const response = await fetch(`http://127.0.0.1:5000/api/spots/${spot_id.value}`, {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            },
            credentials: 'include'
        });

        if(!response.ok) {
            alert('Failed to fetch spot details');
            console.error('Failed to fetch spot details');
            return;
        }

        const data = await response.json();
        spot.value.id = data.id;
        spot.value.status = data.status;
    } catch (error) {
        console.error('Error fetching spot details:', error);
    }
};
const DeleteSpot = async () => {
    (!authStore.get_authtoken()) ? alert('You are not logged in') : null;

    if (!route.params.spot_id) {
        console.error('No spot ID provided');
        router.push('/admin-dashboard');
        return;
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/spots/${spot_id.value}`, {
            
            method: 'DELETE',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        if (response.ok) {
            console.log('Spot deleted successfully');
            router.push('/admin-dashboard');
        } else {
            console.error('Error deleting spot');
        }
    } catch (error) {
        console.error('Error deleting spot:', error);
    }
};
onMounted(() => {
    console.log('Viewspot route params:', route.params);
    spot_id.value = route.params.spot_id;
    console.log(spot_id.value);
    fetchSpotDetails();
    console.log(spot_id.value);
});

const Viewdetails = (id) => {
    router.push(`/spotsdetails/${id}`);
};




</script>
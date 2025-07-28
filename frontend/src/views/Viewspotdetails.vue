<template>
    <div><h1 class = "text-center" style="color: #07567d;">View Spot Details</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent>
            <div class="mb-3">
                <label for="spot_id" class="form-label">Spot Id</label>
                <input type="text" class="form-control" id="spot_id" name="spot_id" v-model="spot_id" readonly>
            </div>
            <div class="mb-3">
            <label for="customer_id" class="form-label">Customer Id</label>
                <input type="text" class="form-control" id="customer_id" name="customer_id" v-model="user_id" readonly>
            </div>
            <div class="mb-3">
                <label for="vehicle_number" class="form-label">Vehicle Number</label>
                <input type="text" class="form-control" id="vehicle_number" name="vehicle_number" v-model="vehicle_number" readonly>
            </div>
            <div class="mb-3">
                <label for="reservation_timestamp" class="form-label">Date and Time of Reservation</label>
                <input type="text" class="form-control" id="reservation_timestamp" name="reservation_timestamp" v-model ="formated_parking_timestamp" readonly>
            </div>
            <div class="mb-3">
                <label for="estimated_parking_cost" class="form-label">Estimated Parking Cost</label>
                <input type="text" class="form-control" id="estimated_parking_cost" name="estimated_parking_cost" v-model="estimated_parking_cost" readonly>
            </div>
            <div class="mb-3">
                <a class="btn btn-outline-primary m-1" @click="router.push('/admin-dashboard')" role="View">Cancel</a>
            </div>
        </form>
    </div>
</template>



<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const route = useRoute();

const spot_id = ref('');
const user_id = ref('');
const vehicle_number = ref('');
const parking_timestamp = ref('');
const cost_per_hour = ref('');

const formated_parking_timestamp = computed(() => {
    return parking_timestamp.value ? new Date(parking_timestamp.value).toLocaleString('en-GB', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
    }).replace(',', '') : 'Loading...';
});

const estimated_parking_cost = computed(() => {
    const parkingtime = parking_timestamp.value;
    const price_per_hour = cost_per_hour.value;

    if (parkingtime && price_per_hour > 0) {
        try {
            const start = new Date(parkingtime);
            console.log(start);
            const end = new Date();
            console.log(end);
            const diff = end - start;
            const hours = Math.ceil(diff / (1000 * 60 * 60));
            return (hours * price_per_hour).toFixed(2);
        } catch (error) {
            console.error('Error calculating estimated parking cost:', error);
        }
    }

    return 'N/A';
    
});

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
        const response = await fetch(`http://127.0.0.1:5000/api/spotdetails/${spot_id.value}`, {
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
        }
        const data = await response.json();
        user_id.value = data.user_id;
        vehicle_number.value = data.vehicle_number;
        parking_timestamp.value = data.parking_timestamp;
        cost_per_hour.value = data.cost_per_hour;
    } catch (error) {
        console.error('Error fetching spot details:', error);
    }
};
onMounted(() => {
    fetchSpotDetails();
});

</script>
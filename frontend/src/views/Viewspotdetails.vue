<template>
    <div><h1 class = "text-center" style="color: #07567d;">View Spot Details</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent>
            <div class="mb-3">
                <label for="spot_id" class="form-label">Spot Id</label>
                <input type="text" class="form-control" id="spot_id" name="spot_id" v-model="spot.id" readonly>
            </div>
            <div class="mb-3">
            <label for="customer_id" class="form-label">Customer Id</label>
                <input type="text" class="form-control" id="customer_id" name="customer_id" v-model="spot.user_id" readonly>
            </div>
            <div class="mb-3">
                <label for="vehicle_number" class="form-label">Vehicle Number</label>
                <input type="text" class="form-control" id="vehicle_number" name="vehicle_number" v-model="spot.vehicle_number" readonly>
            </div>
            <div class="mb-3">
                <label for="reservation_timestamp" class="form-label">Date and Time of Reservation</label>
                <input type="text" class="form-control" id="reservation_timestamp" name="reservation_timestamp" v-model="fparking_timestamp" readonly>
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
const spot = ref({
    user_id: '',
    vehicle_number: '',
    parking_timestamp: '',
    leaving_timestamp: '',
    cost_per_hour: ''
});

const fparking_timestamp = computed(() => {
    if (spot.value.parking_timestamp)
        return new Date(spot.value.parking_timestamp).toLocaleString();
    return '';
});

const estimated_parking_cost = computed(() => {
    const parkingtime = spot.value.parking_timestamp;
    const price_per_hour = spot.value.cost_per_hour;

    if (parkingtime && price_per_hour > 0) {
        try {
            const start = new Date(parkingtime);
            const end = new Date();
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
        spot.value.id = data.id;
        spot.value.user_id = data.user_id;
        spot.value.vehicle_number = data.vehicle_number;
        spot.value.parking_timestamp = data.parking_timestamp;
        spot.value.leaving_timestamp = data.leaving_timestamp;
        spot.value.cost_per_hour = data.cost_per_hour;
    } catch (error) {
        console.error('Error fetching spot details:', error);
    }
};
onMounted(() => {
    fetchSpotDetails();
});

</script>
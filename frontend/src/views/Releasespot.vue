<template>
    <div><h1 class = "text-center" style="color: #07567d;">Release Spot</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent="ReleaseSpot">
            <div class="mb-3">
                <label for="Spot ID" class="form-label">Spot ID</label>
                <input type="text" class="form-control" id="spotId" name="spot_id" v-model="spot_id" readonly>
            </div>
            <div class="mb-3">
                <label for="Vehicle Number" class="form-label">Vehicle Number</label>
                <input type="text" class="form-control" id="vehicleNumber" name="vehicle_number" v-model="vehicle_number" readonly>
            </div>
            <div class="mb-3">
                <label for="Parking Timestamp" class="form-label">Parking Timestamp</label>
                <input type="text" class="form-control" id="parkingTimestamp" name="parking_timestamp" v-model="formated_parking_timestamp" readonly>
            </div>
            <div class="mb-3">
                <label for="Release Timestamp" class="form-label">Release Timestamp</label>
                <input type="text" class="form-control" id="releaseTimestamp" name="release_timestamp" v-model="formated_release_timestamp" readonly>
            </div>
            <div class="mb-3">
                <label for="Total Cost" class="form-label">Total Cost</label>
                <input type="text" class="form-control" id="totalCost" name="total_cost" v-model="total_cost" readonly>
            </div>
            <div>
                <button type="submit" class="btn btn-primary" >Release</button>
                <a class="btn btn-outline-primary m-1" @click="router.push('/user-dashboard')" role="View">Cancel</a>
            </div>
        </form>
    </div>
</template>


<script setup>
import { ref, onMounted, computed} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const route = useRoute();

const spot_id = ref('');
const reservation_id = ref('');
const vehicle_number = ref('');
const parking_timestamp = ref('');
const release_timestamp = ref(new Date());
const total_cost = ref('');

const formated_parking_timestamp = computed(() => {
    return parking_timestamp.value ? new Date(parking_timestamp.value).toLocaleString('en-GB', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
    }).replace(',', '') : 'Loading...';
});

const formated_release_timestamp = computed(() => {
    return release_timestamp.value ? new Date(release_timestamp.value).toLocaleString('en-GB', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
    }).replace(',', '') : 'Loading...';
});

const fetchspotdetails = async () => {
    if(!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }

    try {
        reservation_id.value = route.params.reservation_id;
        console.log(reservation_id.value)
        const response = await fetch(`http://127.0.0.1:5000/api/release/${reservation_id.value}`, {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        spot_id.value = data.spot_id;
        vehicle_number.value = data.vehicle_number;
        parking_timestamp.value = data.parking_timestamp;
        total_cost.value = data.total_cost;
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
    fetchspotdetails();
});

const ReleaseSpot = async () => {
    try {
        if(!authStore.get_authtoken()) {
            alert('You are not logged in');
            router.push('/login');
            return;
        }
        const response = await fetch(`http://127.0.0.1:5000/api/release/${reservation_id.value}`, {
            method: 'POST',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        console.log(data);
        router.push('/user-dashboard');
    } catch (error) {
        console.error(error);
    }
};

</script>
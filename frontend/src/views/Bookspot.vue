<template>
    <div><h1 class = "text-center" style="color: #07567d;">Book Spot</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent="Bookspot">
            <div class="mb-3">
                <label for="Spot ID" class="form-label">Spot ID</label>
                <input type="text" class="form-control" id="spotId" name="spot_id" v-model="spot_id" readonly>
            </div>
            <div class="mb-3">
                <label for="Lot ID" class="form-label">Lot ID</label>
                <input type="text" class="form-control" id="lotId" name="lotId" v-model="lot_id" readonly>
            </div>
            <div class="mb-3">
                <label for="User ID" class="form-label">User ID</label>
                <input type="text" class="form-control" id="userId" name="user_id" v-model="user_id" readonly>
            </div>
            <div class="mb-3">
                <label for="Vehicle Number" class="form-label">Vehicle Number</label>
                <input type="text" class="form-control" id="vehicleNumber" name="vehicle_number" v-model="vehicle_number">
            </div>
            <div>
                <button type="submit" class="btn btn-primary"> Reserve</button>
                <a class="btn btn-outline-primary m-1" @click="router.push('/user-dashboard')" role="View">Cancel</a>
            </div>
        </form>
    </div>
</template>


<script setup>
import { ref , onMounted} from 'vue';
import { useRouter } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const spot_id = ref('');
const user_id = ref('');
const lot_id = ref('');
const vehicle_number = ref('');

lot_id.value = router.currentRoute.value.params.lot_id;

const fetchdata = async () => {
    if (!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/book/${lot_id.value}`, {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        spot_id.value = data.spot_id;
        user_id.value = data.user_id;
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
    fetchdata();
});

const Bookspot = async () => {
    if (!(authStore.get_authtoken())) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/bookspot/${lot_id.value}`, {
            method: 'POST',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            },
            body: JSON.stringify({
                vehicle_number: vehicle_number.value
            })
        });
        const data = await response.json();
        console.log(data);
        router.push('/user-dashboard');
    } catch (error) {
        console.error(error);
    }
};


</script>
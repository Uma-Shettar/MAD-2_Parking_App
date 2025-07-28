<template>
    <div><h1 class = "text-center" style="color: #07567d;">Edit Lot</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent="edit_Lot">
            <div class="mb-3">
                <label for="locationName" class="form-label">Prime Location Name</label>
                <input type="text" class="form-control" id="locationName" name="locationName" v-model="prime_location_name" >
            </div>
            <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" class="form-control" id="address" name="address" v-model="address">
            </div>
            <div class="mb-3">
                <label for="pincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="pincode" name="pincode" v-model="pin_code">
            </div>
            <div class="mb-3">
                <label for="price" class="form-label">Price per Hour</label>
                <input type="number" class="form-control" id="price" name="price" v-model="price_per_hour">
            </div>
            <div class="mb-3">
                <label for="maximumSpots" class="form-label">Maximum Spots</label>
                <input type="number" class="form-control" id="maximumSpots" name="maximumSpots" v-model="total_spots">
            </div>
            <div>
                <button type="submit" class="btn btn-primary">Update Lot</button>
                <a class="btn btn-outline-primary m-1" @click="router.push('/admin-dashboard')" role="View">Cancel</a>
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

const prime_location_name = ref('');
const address = ref('');
const pin_code = ref('');
const price_per_hour = ref('');
const total_spots = ref('');

const lotId = ref('');

const fetchLotDetails = async () => {
    try {
        console.log(`EditlotView (fetchLotDetails): Attempting to fetch lot data for ID: ${lotId.value}`)
        const response = await fetch(`http://127.0.0.1:5000/api/lots/${lotId.value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            },
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to fetch lot details');
        }

        const data = await response.json();
        prime_location_name.value = data.prime_location_name;
        address.value = data.address;
        pin_code.value = data.pin_code;
        price_per_hour.value = data.price_per_hour;
        total_spots.value = data.total_spots;
    } catch (error) {
        console.error('Error fetching lot details:', error);
    }
};
const edit_Lot = async () => {
    if (authStore.get_authtoken() === null) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }

    if (authStore.get_roles().includes('admin') === false) {
        alert('You do not have permission to edit a lot');
        router.push('/user-dashboard');
        return;
    }

    if (!prime_location_name.value || !address.value || !pin_code.value || !price_per_hour.value || !total_spots.value){
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/api/lots/${lotId.value}`, {
            method: 'PUT',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            },
            body: JSON.stringify({
                prime_location_name: prime_location_name.value,
                address: address.value,
                pin_code: pin_code.value,
                price_per_hour: price_per_hour.value,
                total_spots: total_spots.value
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update lot');
        }

        console.log('Lot updated successfully');
        router.push('/admin-dashboard');
    } catch (error) {
        console.error('Error updating lot:', error);
    }
};

onMounted(() => {
    lotId.value = route.params.lot_id;
    if (lotId.value) {
        fetchLotDetails();
    }
    else {
        console.error('No lot ID provided');
        router.push('/admin-dashboard');
    }
});



</script>
<template>
    <div><h1 class = "text-center" style="color: #07567d;">Add Lot</h1></div>
    <div class="container-fluid row justify-content-center">
        <form class="col-5" @submit.prevent="addLot">
            <div class="mb-3">
                <label for="locationName" class="form-label">Prime Location Name</label>
                <input type="text" class="form-control" id="locationName" name="locationName" v-model="primelocationName" >
            </div>
            <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" class="form-control" id="address" name="address" v-model="address">
            </div>
            <div class="mb-3">
                <label for="pincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="pincode" name="pincode" v-model="pincode">
            </div>
            <div class="mb-3">
                <label for="price" class="form-label">Price per Hour</label>
                <input type="number" class="form-control" id="price" name="price" v-model="price_per_hour">
            </div>
            <div class="mb-3">
                <label for="maximumSpots" class="form-label">Maximum Spots</label>
                <input type="number" class="form-control" id="maximumSpots" name="maximumSpots" v-model="maximum_spots">
            </div>
            <div>
                <button type="submit" class="btn btn-primary">Add Lot</button>
                <button type="reset" @click="router.push('/admin-dashboard')" class="btn btn-secondary">Cancel</button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const primelocationName = ref('');
const address = ref('');
const pincode = ref('');
const price_per_hour = ref('');
const maximum_spots = ref('');

const addLot = async () => {

    if (authStore.get_authtoken() === null) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }

    if (authStore.get_roles().includes('admin') === false) {
        alert('You do not have permission to add a lot');
        router.push('/user-dashboard');
        return;
    }

    if (!primelocationName.value || !address.value || !pincode.value || !price_per_hour.value || !maximum_spots.value) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/lots', {
            method: 'POST',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            },
            body: JSON.stringify({
                prime_location_name: primelocationName.value,
                address: address.value,
                pin_code: pincode.value,
                price_per_hour: price_per_hour.value,
                total_spots: maximum_spots.value
            })
        });
        if (response.ok) {
            alert('Lot added successfully');
            router.push('/admin-dashboard');
            primelocationName.value = '';
            address.value = '';
            pincode.value = '';
            price_per_hour.value = '';
            maximum_spots.value = '';
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.message}`);
            console.log(errorData);
            console.error('Error adding lot');
        }
    } catch (error) {
        console.error('Error adding lot:', error);
    }
};

</script>
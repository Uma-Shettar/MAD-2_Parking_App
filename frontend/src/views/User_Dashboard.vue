<template>
<h3 class="text-center" style="color: rgb(114, 162, 250);">Welcome to the User Dashboard</h3>
    
    <div>
        <div class="card border-primary m-5">
            <div class="card-body">
                <h3 class="text-center" style="color: #07567d;">Parking History </h3>
                <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Location</th>
                            <th scope="col">Vehicle Number</th>
                            <th scope="col">Parking Date</th>
                            <th scope="col">Parking Time</th>
                            <th scope="col">Leaving Date</th>
                            <th scope="col">Leave Time</th>
                            <th scope="col">Duration(Hours)</th>
                            <th scope="col"> Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="reservation in reservations" :key="reservation.id">
                            <td>{{ reservation.id }}</td>
                            <td>{{ reservation.lot_name }}</td>
                            <td>{{ reservation.vehicle_number }}</td>
                            <td>{{ formatDate(reservation.parking_timestamp) }} </td>
                            <td>{{ formatTime(reservation.parking_timestamp) }}</td>
                            <td>{{ reservation.leaving_timestamp ? formatDate(reservation.leaving_timestamp) : '---' }} </td>
                            <td>{{ reservation.leaving_timestamp ? formatTime(reservation.leaving_timestamp) : '---' }}</td>
                            <td>{{ reservation.leaving_timestamp ?CalculatedDuration(reservation.parking_timestamp, reservation.leaving_timestamp): '---' }}</td>
                            <td>
                                <a class="btn btn-outline-primary" v-if="reservation.leaving_timestamp == None" @click="Release(reservation.id)" role="button" > Release </a>
                                <a class="btn btn-outline-primary" v-else role="button" @click="Viewdetails(reservation.id)" > View Details </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
<h3 class="text-center" style="color: #07567d;">Search Parking Spot</h3>
<form class = "d-flex" role="search" @submit.prevent="SearchLot">
    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search" v-model="search">
    <select class="form-select me-2" aria-label="Default select example" name="search_type" v-model="search_type">
        <option selected>Select</option>
        <option value="location">Location</option>
        <option value="pincode">Pincode</option>
    </select>
    <input class="btn btn-outline-success" type="submit" value="Search">
</form>

<div>
    <div class="card border-primary m-5">
        <div class="card-body">
            <h3 class="text-center" style="color: #07567d;">Parking Lots </h3>
            <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col"> Address </th>
                        <th scope="col"> Availability </th>
                        <th scope="col"> Action </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="lot in results" :key="lot.id">
                        <td>{{ lot.id }}</td>
                        <td>{{ lot.address }}</td>
                        <td>{{ lot.spots_count }}</td>
                        <td>
                            <a class="btn btn-outline-primary" @click="Book(lot.id)" role="button"> Book </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const reservations = ref([]);
const results = ref([]);
const search = ref('');
const search_type = ref('');

const formatDate = (timestamp) => {
    if (!timestamp) {
        return 'N/A';
    }
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
};

const formatTime = (timestamp) => {
    if (!timestamp) {
        return 'N/A';
    }
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
};

const CalculatedDuration = (parking_timestamp, leaving_timestamp) => {
    if (!parking_timestamp || !leaving_timestamp) {
        return 'N/A';
    }
    const parkingDate = new Date(parking_timestamp);
    const leavingDate = new Date(leaving_timestamp);
    const duration = Math.floor((leavingDate - parkingDate) / (1000 * 60 * 60));
    return duration;
};

const fetchReservations = async () => {

    if(!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/reservations', {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        reservations.value = data;
    } catch (error) {
        console.error('Error fetching reservations:', error);
    }
};

const SearchLot = async () => {

    if (!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    
    try {
        if (search.value === '' || search_type.value === '') {
            const response = await fetch('http://127.0.0.1:5000/api/lots', {
                method: 'GET',
                mode : 'cors',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token':authStore.get_authtoken()
                }
                
            });
            const data = await response.json();
            results.value = data;
            return;
        }
        const response = await fetch(`http://127.0.0.1:5000/api/search/${search.value}/${search_type.value}`, {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        results.value = data;
    } catch (error) {
        console.error('Error fetching reservations:', error);
    }
};

onMounted(() => {
    fetchReservations();
    SearchLot();
});

const Release = async (id) => {
    router.push(`/release/${id}`);
    console.log(`Release lot with ID: ${id}`);
};

const Book = async (id) => {
    router.push(`/book/${id}`);
    console.log(`Book lot with ID: ${id}`);
};

const Viewdetails = (id) => {
    alert(
    `         COST BREAKDOWN
    
    cost per hour : ${reservations.value[id].cost_per_hour}
    Parking Date : ${formatDate(reservations.value[id].parking_timestamp)}
    Parking Time : ${formatTime(reservations.value[id].parking_timestamp)}
    Leaving Date : ${formatDate(reservations.value[id].leaving_timestamp)}
    Leaving Time : ${formatTime(reservations.value[id].leaving_timestamp)}
    Duration : ${CalculatedDuration(reservations.value[id].parking_timestamp, reservations.value[id].leaving_timestamp)} hours
    Total Cost : ${CalculatedDuration(reservations.value[id].parking_timestamp, reservations.value[id].leaving_timestamp) * reservations.value[id].cost_per_hour} Rupees`
    );
};

</script>
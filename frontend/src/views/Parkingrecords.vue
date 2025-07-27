<template>
    <div>
    <div class="card border-primary m-5">
        <div class="card-body">
            <h3 class="text-center" style="color:  #07567d;"> Parking Records </h3>
            <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
            <table class="table table-hover" style="text-align: center;">
                <thead >
                <tr>
                    <th scope="col">User ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Parking Lot</th>
                    <th scope ="col">Parking Date</th>
                    <th scope="col">Spot</th>
                    <th scope="col">Duration (Hours)</th>
                    <th scope="col">Cost</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="r in records" :key="r.id" >
                    <td>{{ r.user_id }}</td>
                    <td>{{ r.name }}</td>
                    <td>{{ r.prime_location_name }}</td>
                    <td>{{ formatDate(r.parking_timestamp) }}</td>
                    <td>{{ r.spot_id }}</td>
                    <td>{{ r.duration ? r.duration : '---' }}</td>
                    <td>{{ r.total_cost ? r.total_cost : '---' }}</td>
                    <td>{{ r.status }}</td>
                    <td v-if="r.status === 'Completed'"><button class="btn btn-outline-primary" @click="Viewdetails(r.id)" role="button"> Cost Details </button></td>
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

const records = ref([]);

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


const fetchRecords = async () => {

    if (!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    try {
        const response = await fetch('http://localhost:5000/api/parkingrecords', {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': authStore.get_authtoken()
            }
        });
        if (response.ok) {
            const data = await response.json();
            records.value = data;
        } else {
            console.error('Failed to fetch records');
        }
    } catch (error) {
        console.error('Error fetching records:', error);
    }
};

onMounted(() => {
    fetchRecords();
});

const Viewdetails = (id) => {
    alert(
        `        COST BREAKDOWN for ${records.value[id].name}

        cost per hour : ${records.value[id].cost_per_hour}
        Parking Date : ${formatDate(records.value[id].parking_timestamp)}
        Parking Time : ${formatTime(records.value[id].parking_timestamp)}
        Leaving Date : ${formatDate(records.value[id].leaving_timestamp)}
        Leaving Time : ${formatTime(records.value[id].leaving_timestamp)}
        Duration : ${records.value[id].duration} hours
        Total Cost : ${records.value[id].total_cost} Rupees`
     );
};

</script>
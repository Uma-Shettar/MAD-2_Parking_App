<template>
    <div class="container-fluid row justify-content-center">
        <h3 class="text-center" style="color: #07567d;">Welcome to the Admin Dashboard</h3>
        <div class="container-fluid row justify-content-center">
            <div v-for="lot in lots" :key="lot.id" class="col-12 col-sm-12 col-md-6 col-lg-3">
                <div class="card border-primary m-3 mt-5">
                    <div class="card-body">
                        <h3 class="text-center" style="color: #07567d;">{{ lot.prime_location_name }}</h3>
                        <p class="text-center" style="color: #07567d;"> Occupied: {{ lot.spots.filter(spot => spot.status == 'O').length }} / {{ lot.total_spots }} </p>
                        <div class="d-flex align-items-center">
                            <a class="btn btn-outline-primary m-1" @click="editLot(lot.id)" role="Edit">Edit</a>
                            <a class="btn btn-outline-danger m-1" @click="deleteLot(lot.id)" role="Delete">Delete</a>
                        </div>
                        <hr style="border: 1px solid #000; width: 100%; margin: 20px auto;">
                        <div class="d-flex flex-wrap">
                                <div v-for ="spot in lot.spots" class="m-2 slot" :key="spot.id" :class="['spot', spot.status == 'O' ? 'occupied' : 'available']" @click="viewSpot(spot.id)" >
                                    {{ spot.status }}    
                                </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

<div class="d-flex justify-content-center">
    <a class="btn btn-outline-primary m-5" @click="addLot" role="button">Add new lot</a>
</div>




</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

const authStore = AuthStore();

const router = useRouter();

const lots = ref([]);
const fetchLots = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/lots', {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        const data = await response.json();
        lots.value = data;
    } catch (error) {
        console.error('Error fetching lots:', error);
    }
};

onMounted(() => {
    fetchLots();
});

const addLot = () => {
    router.push('/lots');
    console.log('Add new lot clicked');
};

const editLot = (id) => {
    router.push(`/lots/${id}`);
    console.log(`Edit lot with ID: ${id}`);
};

const deleteLot = async (id) => {
    if(confirm('Are you sure you want to delete this lot?'))
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/lots/${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token':authStore.get_authtoken()
                }
            });
            if (response.ok) {
                console.log('Lot deleted successfully');
                fetchLots();
            } else {
                console.error('Error deleting lot');
            }
        } catch (error) {
            console.error('Error deleting lot:', error);
        }
    else
        console.log('Deletion cancelled');

};

const viewSpot = (spotId) => {
    router.push(`/spots/${spotId}`);
    console.log(`View spot with ID: ${spotId}`);
};
</script>

<style scoped>
.available {
      background-color: #c6f7d0;
      color: #006400;
    }
.occupied {
      background-color: #f7c6c6;
      color: #8b0000;
    }

.slot {
      width: 40px;
      height: 40px;
      margin: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      border: 2px solid #007bff;
      font-weight: bold;
    }
</style>
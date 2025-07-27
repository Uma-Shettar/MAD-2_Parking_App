<template>
    <h3 class="text-center" style="color: rgb(114, 162, 250);"> Summary </h3>

    <div class="row m-5">
        <div class="col-md-6">
            <div class="card border-primary">
                <div class="card-body">
                    <h5 class="card-title text-center"> Your spending by Parking Lot</h5>
                    <BaseBarChart v-if="lotRevenueChartData.labels.length"
                                  :chart-data="lotRevenueChartData"
                                  chart-id="lot-revenue-chart"
                                  :height="250" />
                    <p v-else class="text-center">No revenue data available for parking lots.</p>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card border-primary">
                <div class="card-body">
                    <h5 class="card-title text-center">Reservations per Parking Lot</h5>
                    <BaseBarChart v-if="lotReservationsChartData.labels.length"
                                  :chart-data="lotReservationsChartData"
                                  chart-id="lot-reservations-chart"
                                  :height="250" />
                    <p v-else class="text-center">No reservation count data available for parking lots.</p>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { AuthStore } from '@/stores/authentication';

import BaseBarChart from '@/components/BaseBarChart.vue';

const authStore = AuthStore();

const router = useRouter();

const chartdata =ref({
    lot_revenue_data: [],
    lot_reservations_data : []
});

const lotRevenueChartData = computed(() => {
    return {
        labels: chartdata.value.lot_revenue_data.map(item => item.label),
        datasets: [
            {
                label: 'Revenue',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                data: chartdata.value.lot_revenue_data.map(item => item.value),
            },
        ],
    };
});

const lotReservationsChartData = computed(() => {
    return {
        labels: chartdata.value.lot_reservations_data.map(item => item.label),
        datasets: [
            {
                label: 'Reservations',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                data: chartdata.value.lot_reservations_data.map(item => item.value),
            },
        ],
    };
});

const fetchdata = ( async () => {
    if (!authStore.get_authtoken()) {
        alert('You are not logged in');
        router.push('/login');
        return;
    }
    try {
        const response = await fetch('http://127.0.0.1:5000/api/userchart', {
            method: 'GET',
            mode : 'cors',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token':authStore.get_authtoken()
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        chartdata.value.lot_revenue_data = data.lot_revenue_data || [];
        chartdata.value.lot_reservations_data = data.lot_reservations_data || [];
        console.log(chartdata.value);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});

onMounted(() => {
    fetchdata();
});

</script>
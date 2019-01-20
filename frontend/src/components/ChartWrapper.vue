<template>
    <ChartSeries :seriesData="seriesData" :isLoading="loading" :anomalies="anomalies"/> <!-- :anomalies="anomalies" -->
</template>


<script>

import ChartSeries from './ChartSeries.vue';
    
export default {
    components: { ChartSeries },
    computed: {
        seriesData() {
            return this.$store.getters.getDisplaySeries
        },
        loading() {
        	return this.$store.state.series.loading
        },
        anomalies() {
            return this.$store.state.series.anomalies
        }
    },
}


</script>
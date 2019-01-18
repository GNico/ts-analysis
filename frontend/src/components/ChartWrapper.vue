<template>
    <ChartSeries :seriesData="seriesData" :isLoading="loading"/>
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
        }
    },
}


</script>
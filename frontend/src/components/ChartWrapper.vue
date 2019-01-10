<template>
    <ChartSeries :seriesData="series" />

</template>


<script>

import ChartSeries from './ChartSeries.vue';
    
export default {
    components: { ChartSeries },
    data() {
        return {
            chartData: []
        }
    },
    computed: {
        series() {
            return this.$store.state.series.displaySeries
        },
        /*chartData() {
            return this.series.map(item => ({ data: item.data, color: item.color, type: item.chartType}) ) 
        }*/
    },
}


</script>
<template>
    <ChartSeries :seriesData="seriesData" />

</template>


<script>

import ChartSeries from './ChartSeries.vue';
    
export default {
    components: { ChartSeries },
    computed: {
        seriesData() {
            return this.$store.getters.getDisplaySeries
        },

    },
}


</script>
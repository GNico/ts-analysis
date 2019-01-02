<template>

<div class="select">
  <select v-model="chartType" @change="changeChartType">
    <option>line</option>
    <option>areaspline</option>
    <option>spline</option>
    <option>scatter</option>
    <option>column</option>
    <option>area</option>
</select>
</div>

</template>



<script>
    
export default {
    name: "SelectChartType",
    data () {
        return {
            chartType: {
                type: String,
                default: "line"
            }
        }
    },
    methods: {
        changeChartType() {
            this.$emit('selected', {selected: this.chartType})
        }
    }
}


</script>
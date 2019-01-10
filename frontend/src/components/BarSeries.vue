<template>    
<div class="is-flex">  
    <div class="field is-grouped is-grouped-multiline">
        <div class="control" v-for="(item, index) in seriesNames" :key="item.name" >
            <ButtonSeriesName  
                :item="item" 
                @deleted="removeItem"
            />
        </div>
    </div>

</div>    
</template>


<script>
    
import ButtonSeriesName from './ButtonSeriesName.vue';


export default {
    components: { ButtonSeriesName },
    computed: {
        seriesNames() {
            return this.$store.getters.getSeriesNames
        }
    },
    methods: {
        removeItem(item) {
            this.$store.commit('delete_series', {name: item})
        }
    }

}

</script>


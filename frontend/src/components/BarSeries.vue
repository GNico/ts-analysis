<template>    
<div class="is-flex">  
    <div class="field is-grouped is-grouped-multiline">
        <div class="control" v-for="(item, index) in seriesNames" :key="item.name" >
            <ButtonSeriesName  
                :item="item" 
                @deleted="removeItem"
                @click="toggleActive"
                :ref="item.name"
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
        },
    },
    methods: {
        removeItem(name) {
            this.$store.dispatch('deleteSeries', name )
        },
        toggleActive(event) {
            this.$store.commit("set_active_series", { [event.name]: event.active })
        }
    }

}

</script>


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
    data () {
        return {
            items: [
                {
                    name: "Series 1",
                },
                {
                    name: "Series 2",
                },
                {
                    name: "Series 3",
                },
                {
                    name: "Series 4",
                },
                {
                    name: "Series 5",
                },
                {
                    name: "Series 6",
                },
                {
                    name: "Series 7",
                },
            ],
        }
    },
    computed: {
        seriesNames() {
            return this.$store.getters.getSeriesNames
        }
    },
    methods: {
        removeItem(name) {
            let index = this.items.findIndex(item => item.name == name)
            this.items.splice(index, 1)
        }
    }

}

</script>


<template>    
<div class="is-flex">  
    <div class="field is-grouped is-grouped-multiline">
        <div class="control" v-for="(item, index) in items" :key="item.name" >
            <ButtonSeriesName  
                :item="item.name" 
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
    methods: {
        removeItem(name) {
            this.items = this.items.filter(item => item.name != name)
        }
    }

}

</script>


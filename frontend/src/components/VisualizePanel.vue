<template>
<div>    
    <p class="title">Panel de control (temporario)</p>

    <b-field label="Contexto">
        <SearchSelect 
            v-model="context_input" 
            :data="contexts"
            placeholder="Seleccionar contexto"
            @selected="changeContext"/>
    </b-field>

    <b-field label="Tag">
        <SearchSelect 
            v-model="tag_input" 
            :data="tags"
            placeholder="Seleccionar tag"
            @selected="changeTag"/>
    </b-field>


    <b-field label="Tipo de grafico">
        <SelectChartType @selected="changeChartType"/> 
    </b-field>


    <b-field label="Color">
        <SelectColor v-model="color"/> 
    </b-field>

</div>
</template>



<script>

import SelectColor from './SelectColor.vue';
import SelectChartType from './SelectChartType.vue';
import SearchSelect from './SearchSelect.vue';

export default {
    name: "VisualizePanel",
    components: { SelectColor, SelectChartType, SearchSelect },
    props: {
        contexts: {
            type: Array,
            default: []
        },
        tags: {
            type: Array,
            default: []
        }
    },
    data () {
        return {
            context_input: '',
            tag_input: '',
            color: '#6fcd98'
        }
    },
    methods: {
        changeContext(option) {
            this.$emit('context-selected', {selected: option})
        },
        changeTag(option) {
            this.$emit('tag-selected', {selected: option})
        },
        changeChartType(event) {
            this.$emit('type-selected', event)
        },
    },
    watch: {
        color(newValue) {
            this.$emit('color-selected', this.color)
        },
    }


}

</script>
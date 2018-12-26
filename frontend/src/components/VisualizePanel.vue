<template>
<div>    
    <p class="title">Panel de control (temporario)</p>

    <b-field label="Contexto">
        <b-autocomplete
            v-model="context_input"
            placeholder="Seleccionar contexto"
            open-on-focus
            keep-first
            :data="filteredContextArray"
            @select="option => changeContext(option)">
            <template slot="empty">No hay resultados</template>
        </b-autocomplete>    
    </b-field>

    <b-field label="Tag">
        <b-autocomplete
            v-model="tag_input"
            placeholder="Seleccionar tag"
            open-on-focus
            keep-first
            :data="filteredTagArray"
            @select="option => changeTag(option)">
            <template slot="empty">No hay resultados</template>
        </b-autocomplete>    
    </b-field>

    <b-field label="Tipo de grafico">
        <SelectChartType @selected="changeChartType"/> 
    </b-field>


    <b-field label="Color">
        <SelectColor @selected="changeColor"/> 
    </b-field>

</div>
</template>



<script>

import SelectColor from './SelectColor.vue';
import SelectChartType from './SelectChartType.vue';
import GradientSlider from './GradientSlider.vue';

export default {
    name: "VisualizePanel",
    components: { SelectColor, SelectChartType, GradientSlider },
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
        }
    },
    computed: {
        filteredContextArray() {
            return  this.contexts.filter(
                (item) => {return item.toLowerCase().match(this.context_input.toLowerCase())} )
        },
        filteredTagArray() {
            return  this.tags.filter(
                (item) => {return item.toLowerCase().match(this.tag_input.toLowerCase())} )
        },        
    },
    methods: {
        changeContext(option) {
            this.$emit('context-selected', {selected: option})
        },
        changeTag(option) {
            this.$emit('tag-selected', {selected: option})
        },
        changeColor(event) {
            this.$emit('color-selected', event)
        },
        changeChartType(event) {
            this.$emit('type-selected', event)
        }
    }


}

</script>
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
        <select v-model="chartType">
            <option>Line</option>
            <option>AreaSpline</option>
            <option>Spline</option>
            <option>Scatter</option>
            <option>Column</option>
            <option>Area</option>
        </select>    
    </b-field>


    <b-field label="Color">
        <ColorSelect @selected="changeColor"> </ColorSelect>
    </b-field>

</div>
</template>



<script>

import ColorSelect from './ColorSelect.vue';
import GradientSlider from './GradientSlider.vue';

export default {
    name: "VisualizePanel",
    components: { ColorSelect, GradientSlider },
    data () {
        return {
            context_input: '',
            tag_input: '',
            chartType: 'Line',
        }
    },
    computed: {
        contexts() {
            return this.$store.state.series.contexts
        },
        tags() {
            return this.$store.state.series.tags
        },
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
           this.$store.commit('set_client_context', option)
        },
        changeTag(option) {
            this.$store.commit('set_client_tags', option)
        },
        changeColor(event) {
            console.log('cambio color llego evento a panel')
            this.$emit('color-changed', event)
        }
    }


}

</script>
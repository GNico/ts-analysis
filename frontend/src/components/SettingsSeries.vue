<template>
<div>

    <p class="title">Panel de control (temporario)</p>

    <b-field label="Cliente">
        <SearchSelect 
            v-model="client_input" 
            :data="clients"
            placeholder="Seleccionar cliente"
            @selected="changeClient"/>
    </b-field>


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
    name: "SettingsSeries",
    components: { SelectColor, SelectChartType, SearchSelect },
    props: {
        clients: {
            type: Array,
            default: function () {
                return []
            }
        },
        contexts: {
            type: Array,
            default: function () {
                return []
            }
        },
        tags: {
            type: Array,
            default: function () {
                return []
            }
        }
    },
    data () {
        return {
            client_input: '',
            context_input: '',
            tag_input: '',
            color: '#6fcd98'
        }
    },
    methods: {
        changeClient(option) {
            this.$emit('client-selected', {selected: option})
        },
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
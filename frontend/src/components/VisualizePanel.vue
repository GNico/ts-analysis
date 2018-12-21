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
            :data="filteredTagArray"
            @select="option => changeTag(option)">
            <template slot="empty">No hay resultados</template>
        </b-autocomplete>    
    </b-field>
</div>
</template>



<script>

export default {
    name: "VisualizePanel",
    data () {
        return {
            context_input: '',
            tag_input: '',
            selected_context: '',
            selected_tags: '',

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
            this.selected_context = option
            this.$store.commit('set_client_context', option)

        },
        changeTag(option) {
            this.selected_tags = option
            this.$store.commit('set_client_tags', option)
        }
    }


}

</script>
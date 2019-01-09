<template>
    <b-autocomplete
        v-model="inputValue"
        :placeholder="placeholder"
        open-on-focus
        keep-first
        :data="reducedDataList"
        @select="option => $emit('selected', option)"
        @blur="onBlur">
        <template slot="empty">No hay resultados</template>
    </b-autocomplete>  
</template>


<script>

export default {
    name: "SearchSelect",
    model: {
        prop: 'value',
        event: 'selected'
    },
    props: {
        value: {
            required: true,
        },
        data: {
            required: false
        },
        maxOptionsDisplayed: {
            type: Number,
            default: 50
        },
        placeholder: {
            default: "Seleccionar"
        },
        clearOnBlur: {
            type: Boolean,
            default: true
        }
    },
    data () {
        return {
            inputValue: this.value || ''
        }
    },
    computed: {
        filteredDataList() {
            return  this.data.filter(
                (item) => {return item.toLowerCase().match(this.inputValue.toLowerCase())} )
        },
        reducedDataList() {
            return this.filteredDataList.slice(0, this.maxOptionsDisplayed)
        },
    },
    methods: {
        onBlur() {
            if (this.clearOnBlur && this.filteredDataList.length === 0) {
                this.inputValue = ''
            } 
        }
    }
}

</script>
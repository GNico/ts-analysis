<template>
    <b-autocomplete
        v-model="inputValue"
        :placeholder="placeholder"
        open-on-focus
        :data="reducedDataList"
        @select="emitSelected"
        ref=autocomplete 
        @keydown.native.enter="$event.target.blur(); closeOptions()"
        @blur="onBlur"
        >  <!-- @blur="onBlur" -->
        <template slot="empty">No hay resultados</template>
    </b-autocomplete>  
</template>


<script>

export default {
    name: "SearchSelect",
    props: {
        saved: {
            required: false,
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
    data() {
        return {
            inputValue:  ''
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
        },
        setSelected(selected) {
            let idx = this.data.findIndex(item => item == selected)
            if (idx != -1) {
                this.$refs.autocomplete.setSelected(this.data[idx])
            } else {
                console.log("no encontro item")
            }
        },
        closeOptions() {            
            this.$refs.autocomplete.isActive = false
        },
        emitSelected(option) {
            if (!this.saved) {
                this.$emit('selected', option)
            }
        },
        clear() {
            this.inputValue = ''
        }
    },
    watch: {
        saved(newval) {
            this.setSelected(newval)
        },
    }
}

</script>
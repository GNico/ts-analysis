<template>
    <select v-model="selected" v-on:change="tagSelected"> <option v-for="option in opciones" v-bind:value="option"> {{ option }} </option> </select>
</template>


<script>

export default {
    props: ['opciones'],
    data () {
        return {
            selected: ''

        }
    },
    methods: {
        tagSelected () {
            this.$emit('tagchanged', {selected: this.selected})
        }
    }

}

</script>

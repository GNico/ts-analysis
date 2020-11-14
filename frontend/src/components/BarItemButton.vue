<template>
<a class="button is-info is-flex" @click="toggle" :class="{ 'is-outlined': !isActive }">
    {{name}}
    <button class="delete is-small" @click="deleted"></button>
</a> 
</template>



<script>
export default {
    props: ['id', 'name', 'isActive'],
    methods: {
        toggle() {
            this.$emit('click', this.id)
        },
        deleted() {
            this.$emit("deleted", this.id)
        }
    }

}
</script>


<style scoped>
.delete {
    margin-left: 0.5rem;
    margin-right: -0.5rem;
}
</style>
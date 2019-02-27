<template>
<span class="tag button is-info is-large" @click="toggle" :class="{ 'is-outlined': !isActive }">
  {{name}}
  <button class="delete is-small" @click="deleted"></button>
</span>
</template>



<script>
export default {
    props: ['name', 'isActive'],
    methods: {
        toggle() {
            this.$emit('click', {name: this.name, active: !this.isActive})
        },
        deleted() {
            this.$emit("deleted", this.name)
        }
    }

}
</script>
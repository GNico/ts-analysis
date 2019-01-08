<template>
    
<div class="tags has-addons">
      <span class="tag button is-primary is-medium" @click="toggle" :class="{ 'is-outlined': !isActive }">
        {{item}}
      </span>
      <a class="tag is-delete is-primary is-medium" @click="deleted"></a>
</div>


</template>



<script>
    
export default {
    props: ['item'],
    data () {
        return {
            isActive: true
        }
    },
    methods: {
        toggle() {
            this.isActive = !this.isActive
            this.$emit('click', {toggled: this.isActive, item: this.item})
        },
        deleted() {
            this.$emit("deleted", this.item)
        }
    }

}

</script>
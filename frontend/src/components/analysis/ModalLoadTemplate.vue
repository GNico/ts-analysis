<template>
<ModalCard 
  :isActive="isActive" 
  title="Import template"
  minheight="50%"
  @close="close">

  <b-table 
    :data="allModels" 
    sticky-header
    narrowed
    hoverable
    :selected.sync="selected"
    @dblclick="load">
       
      <b-table-column field="name" label="Name" sortable searchable>
        <template v-slot="props">
          {{ props.row.name }}
        </template>
        <template #searchable="props">
            <b-input
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

      <b-table-column field="description" label="Description" searchable>
        <template v-slot="props">
          {{ props.row.description }}
        </template>        
        <template #searchable="props">
            <b-input
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

    </b-table>

  <template v-slot:footer-right>
    <div>
      <button :disabled="!selected" class="button is-small is-primary" @click="load">Load</button>
      <button :disabled="!selected" class="button is-small is-danger" @click="confirmDelete">Delete</button>
      <button class="button is-small" @click="close">Cancel</button>
    </div>
  </template>
</ModalCard>
</template>


<script>
import ModalCard from "../ModalCard"

export default {
  components: { ModalCard },
  props: { 
    allModels: {
      type: Array,
      default: () => []
    },
    isActive: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      selected: undefined,
    }
  },
  methods: {
    close() {
      this.selected = undefined,
      this.$emit('close')
    },
    load() {
      this.$emit('load', this.selected)
      this.close()
    },    
    remove() {
      this.$emit('delete',  this.selected.id)
    },
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Deleting template',
        message: 'Are you sure you want to <b>delete</b> this item? This action cannot be undone.',
        confirmText: 'Delete Template',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => this.remove()
      })
    },
  }
}


</script>
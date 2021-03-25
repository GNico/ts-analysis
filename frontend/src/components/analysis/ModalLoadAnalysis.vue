<template>
<ModalCard 
  :isActive="isActive" 
  :title="title"
  minheight="50%"
  @close="close">

  <b-table 
    :data="allAnalysis" 
    sticky-header
    narrowed
    hoverable
    :selected.sync="selected"
    @dblclick="load">
    <template slot-scope="props">
       
      <b-table-column field="name" label="Name" sortable searchable>
        {{ props.row.name }}
        <template #searchable="props">
            <b-input
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

      <b-table-column field="client" label="Client" sortable searchable >
        {{ props.row.client }}
        <template #searchable="props" >
            <b-input
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

      <b-table-column field="description" label="Description" searchable>
        {{ props.row.description }}
        <template #searchable="props">
            <b-input
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>
    </template>
  </b-table>

  <template v-slot:footer-right>
    <div>
      <button :disabled="!selected" class="button is-small is-primary" @click="load">{{confirmLabel}}</button>
      <button v-show="allowDelete" :disabled="!selected" class="button is-small is-danger" @click="confirmDelete">Delete</button>
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
    allAnalysis: {
      type: Array,
      default: () => []
    },
    isActive: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: 'Load Analysis'
    },
    allowDelete: {
      type: Boolean,
      default: true
    },
    confirmLabel: {
      type: String,
      default: 'Load'
    }
  },
  data() {
    return {
      selected: undefined,
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    load() {
      this.close()
      this.$emit('load', this.selected.id)
    }, 
    remove() {
      this.$emit('delete',  this.selected.id)
    },
    confirmDelete() {
      this.$buefy.dialog.confirm({
        title: 'Deleting analysis',
        message: 'Are you sure you want to <b>delete</b> this item? This action cannot be undone.',
        confirmText: 'Delete Analysis',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => this.remove()
      })
    },   
  }
}


</script>




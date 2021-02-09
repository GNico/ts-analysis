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

      <b-table-column field="delete" label="Delete">
        <button class="transparent-button" @click="confirmDelete(props.row.id)">
          <b-icon icon="trash-can-outline" type="is-warning"></b-icon>
        </button>
      </b-table-column>
    </template>
  </b-table>

  <template v-slot:footer-right>
    <div>
      <button :disabled="!selected" class="button is-small is-primary" @click="load">Load</button>
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
      this.$emit('close')
    },
    load() {
      this.close()
      this.$emit('load', this.selected)
    },    
    remove(id) {
      this.$emit('delete',  id)
    },
    confirmDelete(id) {
      this.$buefy.dialog.confirm({
        title: 'Deleting template',
        message: 'Are you sure you want to <b>delete</b> this item? This action cannot be undone.',
        confirmText: 'Delete Template',
        type: 'is-danger',
        scroll: 'keep',
        hasIcon: true,
        onConfirm: () => this.remove(id)
      })
    },
  }
}


</script>
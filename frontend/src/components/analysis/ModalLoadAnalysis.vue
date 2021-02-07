 <template>

<ModalCard 
  :isActive="isActive" 
  title="Load Analysis"
  minheight="50%"
  @close="close">

  <b-field class="has-text-right">
    <b-checkbox v-model="showFilters" class="has-text-white">
    Enable filters
  </b-checkbox>
  </b-field>

  <b-table 
    :data="allAnalysis" 
    sticky-header
    narrowed
    checkable
    selectable
    :checked-rows.sync="checked">
    <template slot-scope="props">
      <b-table-column field="client" label="Client" sortable :searchable="showFilters" >
        {{ props.row.client }}
        <template #searchable="props" >
            <b-input
              v-if="showFilters"
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

      <b-table-column field="name" label="Name" sortable :searchable="showFilters">
        {{ props.row.name }}
        <template #searchable="props">
            <b-input
              v-if="showFilters"
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

      <b-table-column field="description" label="Description" :searchable="showFilters">
        {{ props.row.description }}
        <template #searchable="props">
            <b-input
              v-if="showFilters"
              v-model="props.filters[props.column.field]"
              placeholder="Search..."
              icon="magnify"
              size="is-small" />
        </template>
      </b-table-column>

      <b-table-column field="load" label="Load">
        <button class="transparent-button" @click="load(props.row.id)">
          <b-icon icon="folder-download" type="is-primary"></b-icon>
        </button>
      </b-table-column>
    </template>
  </b-table>


  <template v-slot:footer-left>
    <button class="button is-small is-danger" :disabled="!checked.length" @click="deleteSelected">Delete selected</button>
  </template>
  <template v-slot:footer-right>
    <div>
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
    }
  },
  data() {
    return {
      checked: [],
      showFilters: false,
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    deleteSelected() {
      this.$emit('delete', this.checked)
    },
    load(event) {
      this.close()
      this.$emit('load', event)
    }
  }
}


</script>




 <template>

<ModalCard 
  :isActive="isActive" 
  title="Load Analysis"
  minheight="50%"
  @close="close">

  <b-table 
    :data="allAnalysis" 
    sticky-header
    narrowed
    checkable
    selectable
    :checked-rows.sync="checked">
    <template slot-scope="props">
      <b-table-column field="client" label="Client" sortable  >
        {{ props.row.client }}
      </b-table-column>

      <b-table-column field="name" label="Name" sortable >
        {{ props.row.name }}
      </b-table-column>

      <b-table-column field="description" label="Description">
        {{ props.row.description }}
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
    isActive: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      checked: [],
    }
  },
  computed: {
    allAnalysis() {
      return this.$store.state.analysis.all
    }
  },
  methods: {
    close() {
      this.$emit('close')
    },
    deleteSelected() {
      this.$emit('deleteSelected', this.checked)
    },
    load(event) {
      this.close()
      this.$emit('load', event)
    }
  }
}


</script>




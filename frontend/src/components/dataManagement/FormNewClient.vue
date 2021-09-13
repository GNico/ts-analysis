 <template>
  <form @submit.prevent="handleSubmit">
    <div class="modal-card" style="width: 300px; border-radius: 0.4em">
      <section class="modal-card-body">
        <b-field label="Name">
          <b-input
            :value="form.name"
            @input="e => form.name = e.toLowerCase()"
            placeholder="Client's name"
            pattern="[a-z0-9]+"
            size="is-small"
            validation-message="Required. Only alphanumeric characters"
            required>
          </b-input>
        </b-field>      

        <b-field label="Data source">
          <b-select placeholder="Select a name" v-model="form.folderName" size="is-small">
            <option
              v-for="option in dataSourceNames"
              :value="option"
              :key="option">
              {{ option}}
            </option>
          </b-select>
        </b-field>

        <b-field label="Time zone">
          <b-select v-model="form.UTCOffset" size="is-small">
            <option
              v-for="offset in UTCOffsets"
              :value="offset[1]"
              :key="offset[1]">
              {{ offset[0] }}
            </option>
          </b-select>
        </b-field>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-primary">Submit</button>
      </footer>
    </div>
  </form>
</template>


<script>
import { timezones, getValidUserUTCOffset } from "@/utils/datetimeConstants"

const initForm = {
  name: '',
  folderName: '',
  UTCOffset: getValidUserUTCOffset()
}

export default {
  name: 'FormNewClient',
  props: {
    dataSourceNames: {
      type: Array,
      default: () => []
    }
  },
	data() {
    return {
      form: { ...initForm }
    }
  },
  computed: {
    UTCOffsets() {
      return timezones.UTCOffsets
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', this.form)
    },  
    resetForm() {
      this.form = { ...initForm }
    }
  }
}

</script>

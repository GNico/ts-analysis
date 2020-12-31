 <template>
<div>
  <form @submit.prevent="handleSubmit">
    <div class="modal-card" style="width: 300px">
      <section class="modal-card-body">
        <b-field label="Name">
          <b-input
            :value="form.name"
            @input="e => form.name = e.toLowerCase()"
            placeholder="Client's name"
            pattern="[a-z0-9]+"
            validation-message="Required. Only alphanumeric characters"
            required>
          </b-input>
        </b-field>
        <b-field label="Folder name">
          <b-input
            v-model="form.folder_name"
            placeholder="Data folder"
            required>
          </b-input>
        </b-field>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-primary">Submit</button>
      </footer>
    </div>
  </form>
</div>
</template>


<script>
import api from "../api/repository"

export default {
  name: 'FormNewClient',
	data() {
    return {
      form: {
        name: '',
        folder_name: '',
      },
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', this.form)
    },  
  }
}

</script>

 <template>

<div>
  <form @submit.prevent="handleSubmit">
    <div class="modal-card" style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title">Nuevo cliente</p>
      </header>
      <section class="modal-card-body">
        <b-field label="Name">
          <b-input
            v-model="form.name"
            placeholder="Nombre del cliente"
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
        loading: false,
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', this.form)
    }
  }
}

</script>
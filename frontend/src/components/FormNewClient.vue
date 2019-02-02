 <template>

<div>
  <div v-if="loading">
    <span v-text="status">  </span>
  </div>

  <form @submit.prevent="handleSubmit">
    <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
            <p class="modal-card-title">Nuevo cliente (form temporario)</p>
        </header>
        <section class="modal-card-body">
            <b-field label="Name">
                <b-input
                    v-model="form.name"
                    placeholder="Nombre del cliente"
                    required>
                </b-input>
            </b-field>

            <b-field label="Index name">
                <b-input
                    v-model="form.index_name"
                    placeholder="Elasticsearch index"
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
  <!--           <button class="button" type="button" @click="$parent.close()">Close</button>-->          
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
          index_name: '',
          folder_name: '',
        },
        loading: false,
        status: ''
    }
  },
  methods: {
    handleSubmit() {
      let vm = this
      vm.loading = true
      vm.status = "INDEXANDO"
      api.addNewClient(vm.form)
      .then(response => {       
        console.log("termino indexar")
        vm.loading = false
        vm.status = "TERMINADO"
        vm.$store.dispatch('clients/fetchClients');
      })
      .catch(error => { 
        console.log('error creating new client')
      })
    }
  }
}

</script>
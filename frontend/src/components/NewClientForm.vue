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

export default {
  name: 'NewClientForm',
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
      axios.post('http://localhost:8000/prueba/newclient/', vm.form)
        .then(response => {       
          console.log("termino indexar (no async atm)")
          vm.loading = false
          vm.status = "TERMINADO"
          vm.$store.dispatch('fetchClients');
        })
        .catch(error => { 
          console.log('error creating new client')
        })
    }
  }
}

</script>
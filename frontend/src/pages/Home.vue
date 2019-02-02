<template>
    
<div class="tile is-ancestor">

    <div class="tile is-vertical is-6">
      <div class="tile">
        <div class="tile is-parent">
          <article class="tile is-child notification is-info">
            <b-table :data="clients" :columns="columns" striped hoverable focusable :selected.sync="selected"></b-table>
          </article>
        </div>
      </div>

      <div class="tile is-parent">
        <article class="tile is-child notification is-info">
            <div v-if="selected">
                <p class="title"> {{ selected.name }} </p>
                <table class="table">
                <thead>
                    <tr>
                        <th>Contexto</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for='item in selected.context'>
                        <td>{{item}}</td>
                    </tr>
                </tbody>
                </table>
            </div>
        </article>
      </div>
    </div>

    <div class="tile is-parent">
      <article class="tile is-child notification is-info">
        <FormNewClient/>
      </article>
    </div>
</div>  


</template>


<script>

import FormNewClient from '../components/FormNewClient'

export default {
    components: {  FormNewClient },
    data() {
        return {
            columns: [
                {
                    field: 'name',
                    label: 'Cliente'
                },
                {
                    field: 'count',
                    label: 'Num. Eventos',
                },
                {
                    field: 'start_date',
                    label: 'Primer evento',
                },
                {
                    field: 'end_date',
                    label: 'Ultimo evento',
                }               
            ],
            contextColumns: [
                {
                    field: 'context',
                    label: 'Contexto',
                }
            ],
            selected: null,
        }
    },
    computed: {
        clients() {
            return this.$store.state.clients.clients
        },
    }
}

</script>
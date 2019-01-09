<template>
<div>

    <div class="field">
        <label class="label"> Nombre </label>
        <b-field v-if="edit">
            <b-select
                placeholder="Default"
                expanded>
                <option value="flint">Flint</option>
                <option value="silver">Silver</option>
            </b-select>     
            <p class="control">
                <button class="button is-primary" @click="edit=false">
                    <span class="icon">
                        <i class="fas fa-plus"></i>
                    </span>
                </button>
            </p>
        </b-field>

        <b-field v-else>
            <b-input v-model="seriesOptions.name"></b-input>
            <p class="control">
                <button class="button is-danger" @click="edit=true">
                    <span class="icon">
                        <i class="fas fa-times"></i>
                    </span>
                </button>
            </p>
        </b-field>
    </div>
    

    <!-- <b-field grouped>
            <b-input placeholder="Search..." expanded></b-input>
            <p class="control">
                <button class="button is-primary">New</button>
            </p>
        </b-field> -->

    <!-- <div class="field">
        <label class="label"> Series name </label>
        <div class="field is-grouped">
          <div class="control is-expanded">
            <SearchSelect 
            v-model="client" 
            :data="clients"
            placeholder="Seleccionar cliente"
            @selected="changeClient"/>          
          </div>
          <div class="control">
            <a class="button is-info">
              New
            </a>
          </div>
        </div>
    </div>
 -->
    <div class="field">
        <label class="label"> Cliente </label>
        <SearchSelect 
            v-model="seriesOptions.client" 
            :data="clientsSelectOptions"
            placeholder="Seleccionar cliente"
            @selected="updateSelectOptions"
        />
    </div>

    <div class="field">
        <label class="label"> Contexto </label>
        <SearchSelect 
            v-model="seriesOptions.context" 
            :data="contexts"
            placeholder="Seleccionar contexto"
        />
    </div>

    <div class="field">
        <label class="label"> Tag </label>
        <SearchSelect 
            v-model="seriesOptions.tags" 
            :data="tags"
            placeholder="Seleccionar tag"
        />
    </div>

    <div class="field">
        <label class="label"> Tipo de grafico </label>
        <div class="select">
          <select v-model="seriesOptions.chartType">
                <option>line</option>
                <option>areaspline</option>
                <option>spline</option>
                <option>scatter</option>
                <option>column</option>
                <option>area</option>
            </select>
        </div>
    </div>

    <div class="field">
        <label class="label"> Intervalo display </label>
        <div class="select">
          <select v-model="seriesOptions.interval">
                <option value="30m">30 minutos</option>
                <option value="1H">1 hora</option>
                <option value="2H">2 horas</option>
                <option value="6H">6 horas</option>
                <option value="12H">12 horas</option>
                <option value="1d">1 dia</option>
            </select>
        </div>
    </div>

    <div class="field">
        <label class="label"> Color </label>
        <SelectColor v-model="seriesOptions.color"/> 
    </div>


    <!-- buttons  -->
    <div v-if="edit" class="box has-text-centered">
      <a class="button is-primary" @click="updateSeries">
          Actualizar
      </a>
    </div>
    <div v-else class="buttons is-centered box">
        <a class="button is-primary" @click="addSeries">
          Agregar
        </a>
        <a class="button is-danger" @click="cancel">
          Cancelar
        </a>
    </div>
    </div>


</div>
</template>



<script>

import SelectColor from './SelectColor.vue';
import SelectChartType from './SelectChartType.vue';
import SearchSelect from './SearchSelect.vue';

export default {
    components: { SelectColor, SelectChartType, SearchSelect },
    data () {
        return {
            seriesOptions: {
                name: '',
                client: '',
                contexts: '',
                tags: '',
                color: '#6fcd98',
                chartType: 'line',
                interval: '1H'
            },
            edit: false, 
        }
    },
    computed: {
        clients() {
            return this.$store.state.series.clients
        },
        clientsSelectOptions() {
            return this.clients.map(item => item.name);
        },
        contexts() {
            return this.$store.state.series.contexts
        },
        tags() {
            return this.$store.state.series.tags
        },
    },
    methods: {
        updateSelectOptions() {
            this.$store.dispatch('updateTagsContexts', this.seriesOptions.client)
        },
        addSeries() {
            this.edit = true
            this.$store.dispatch('addSeries', this.seriesOptions)
        },
        updateSeries() {
            this.$store.dispatch('updateSeries', this.seriesOptions)
        },
        cancel() {

        }
    }
}

</script>
<template>
<div>

    <div class="field">
        <label class="label"> Nombre </label>
        <b-field v-if="edit">
            <b-select placeholder="" expanded :value="seriesOptions.name" @input="setSavedOptions"> 
                <option v-for="item in seriesNames"> {{ item }}</option>
            </b-select>     
            <p class="control">
                <button class="button is-primary" @click="newMode">
                    <span class="icon">
                        <i class="fas fa-plus"></i>
                    </span>
                </button>
            </p>
        </b-field>

        <div v-else>
            <b-field> 
                <b-input v-model="seriesOptions.name" expanded></b-input>
                <p class="control">
                    <button class="button is-danger" @click="editMode">
                        <span class="icon">
                            <i class="fas fa-times"></i>
                        </span>
                    </button>
                </p>
            </b-field>
            <p v-show="hasError" class="help is-danger">El nombre ya existe</p>
        </div>
    </div>
    

    <div class="field">
        <label class="label"> Cliente </label>
        <SearchSelect 
            :saved="saved.client"
            :data="clientsSelectOptions"
            placeholder="Seleccionar cliente" 
            @selected="updateSelectOptions"  
            ref=clientselect
        />
            <!-- "seriesOptions.client = $event; updateSelectOptions()" -->
    </div>

    <div class="field">
        <label class="label"> Contexto </label>
        <SearchSelect 
            :saved="saved.contexts" 
            :data="contexts"
            placeholder="Seleccionar contexto"
            @selected="seriesOptions.contexts = $event"
            ref=contextselect

        />
    </div>

    <div class="field">
        <label class="label"> Tag </label>
        <SearchSelect 
            :saved="saved.tags" 
            :data="tags"
            placeholder="Seleccionar tag"
            @selected="seriesOptions.tags = $event"
            ref=tagselect

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
        <a class="button is-danger" @click="editMode">
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
            saved: {
                client: '',
                contexts: '',
                tags: '',
            },
            edit: false, 
        }
    },
    computed: {
        seriesNames() {
            return this.$store.getters['series/getSeriesNames']
        },
        clients() {
            return this.$store.state.clients.clients
        },
        clientsSelectOptions() {
            return this.clients.map(item => item.name);
        },
        contexts() {
            return this.$store.state.clients.contexts
        },
        tags() {
            return this.$store.state.clients.tags
        },
        hasError() {
            return this.seriesNames.includes(this.seriesOptions.name)
        }
    },
    methods: {
        async setSavedOptions (value) {
            let obj = this.$store.getters.getSeriesOptions(value) 
            this.seriesOptions.name = value
            this.saved.client = obj.client 
            this.seriesOptions.color = obj.color
            this.seriesOptions.chartType = obj.chartType
            this.seriesOptions.interval = obj.interval
            await this.$store.dispatch('clients/updateTagsContexts', obj.client)
            this.saved.tags = obj.tags
            this.saved.contexts = obj.contexts

            
        },
        updateSelectOptions(value) {
            this.seriesOptions.client = value
            if (this.saved.client != value) {
                this.$store.dispatch('clients/updateTagsContexts', this.seriesOptions.client)
            }
        },
        addSeries() {
            this.edit = true
            this.$store.dispatch('series/addSeries', this.seriesOptions)
        },
        updateSeries() {
            this.$store.dispatch('series/updateSeries', this.seriesOptions)
        },
        clearFields() {
            this.seriesOptions.name = ''
            this.seriesOptions.color = '#6fcd98'      
            this.seriesOptions.chartType = 'line'
            this.seriesOptions.interval = '1H'
            this.$refs.clientselect.clear()
            this.$refs.contextselect.clear()
            this.$refs.tagselect.clear()
            this.saved.client = ''
            this.saved.contexts = ''
            this.saved.tags = ''

        },
        editMode() {
            this.edit = true
        },
        newMode() {
            this.edit = false
            this.clearFields()
        }
    },
    watch: {
        seriesNames() {
            if (!this.seriesNames.includes(this.seriesOptions.name) && edit) {
                this.clearFields()
            } 
        }
    }
}

</script>
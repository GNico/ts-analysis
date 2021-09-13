<template>
<b-navbar>
  <template slot="brand">
    <b-navbar-item tag="router-link" :to="{ path: '/' }">
      <img src="@/assets/img/keepconlogo.png" width="156" height="30">
    </b-navbar-item>
  </template>

  <template slot="start">
    <router-link to='/' exact class="navbar-item">Data Management</router-link>
    <router-link to='/Visualization'  class="navbar-item">Visualization</router-link>
    <router-link to='/Analysis'  class="navbar-item">Analysis</router-link>
    <router-link to='/Monitoring'  class="navbar-item">Monitoring</router-link>
  </template>

  <template #end>
    <b-navbar-item tag="div">
      <b-dropdown  
        scrollable
        position="is-bottom-left" 
        :max-height="300" 
        v-model="UTCOffset">
        <template #trigger>
          <a class="is-flex is-align-items-center has-text-grey">
            <span><strong>{{offsets.find(elem=> elem[1] === UTCOffset)[0]}}</strong></span>
            <b-icon icon="menu-down"></b-icon>
          </a>
        </template>
        <b-dropdown-item 
          v-for="offset in offsets" 
          :key="offset[1]"
          :value="offset[1]">{{offset[0]}}
        </b-dropdown-item>
      </b-dropdown>   

    </b-navbar-item>
  </template>
</b-navbar>
</template>


<script>
import { timezones } from '@/utils/datetimeConstants'
  
export default {
  data() {
    return {
    }
  },
  computed: {
    offsets() {
      return timezones.UTCOffsets
    },
    UTCOffset: {
      get: function () {
        return this.$store.state.UTCOffset
      },
      set: function (newValue) {
        this.$store.commit('set_utcoffset', newValue)
      }
    }    
  },
  methods: {    
  }
}

</script>
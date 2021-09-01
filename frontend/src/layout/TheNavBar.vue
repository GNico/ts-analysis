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
          <b-dropdown-item v-for="offset in offsets" :value="offset[1]">{{offset[0]}}</b-dropdown-item>
      </b-dropdown>   

    </b-navbar-item>
  </template>
</b-navbar>
</template>


<script>
import { dtNames } from '@/utils/dateFormatter'
  
export default {
  data() {
    return {
     /* offsets: [
        ["UTC−12:00", -12],
        ["UTC−11:00", -11],
        ["UTC−10:00", -10],
        ["UTC−09:30", -9.5],
        ["UTC−09:00", -9],
        ["UTC−08:00", -8],
        ["UTC−07:00", -7],
        ["UTC−06:00", -6],
        ["UTC−05:00", -5],
        ["UTC−04:30", -4.5],
        ["UTC−04:00", -4],
        ["UTC−03:00", -3],
        ["UTC−02:00", -2],
        ["UTC−01:00", -1],
        ["UTC±00:00", 0],
        ["UTC+01:00", 1],
        ["UTC+02:00", 2],
        ["UTC+03:00", 3],
        ["UTC+04:00", 4],
        ["UTC+04:30", 4.5],
        ["UTC+05:00", 5],
        ["UTC+05:30", 5.5],
        ["UTC+05:45", 5.75],
        ["UTC+06:00", 6],
        ["UTC+06:30", 6.5],
        ["UTC+07:00", 7],
        ["UTC+08:00", 8],
        ["UTC+08:45", 8.75],
        ["UTC+09:00", 9],
        ["UTC+10:00", 10],
        ["UTC+11:00", 11],
        ["UTC+11:30", 11.5],
        ["UTC+12:00", 12],
        ["UTC+13:00", 13],
        ["UTC+14:00", 14]
      ] */
    }
  },
  computed: {
    offsets() {
      return dtNames.UTCOffsets
    },
    UTCOffset: {
      // getter
      get: function () {
        return this.$store.state.UTCOffset
      },
      // setter
      set: function (newValue) {
        this.$store.commit('set_utcoffset', newValue)
      }
    }    
  },


}

</script>
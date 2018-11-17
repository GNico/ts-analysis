<template>
  <div id="app">
    <!--Header with menu-->
    <base-layout></base-layout>

    <section class='section'>
        <router-view> </router-view>
    </section>
  </div>
</template>

<script>

import BaseLayout from './components/BaseLayout.vue';

export default {
  name: 'app',
  components: { BaseLayout  },
  data () {
    return {
      msg: 'Una app random App'
    }
  },
  created() {
    //initialize store data structure by submitting action.
    this.$store.dispatch('fetchClients');
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

<template>

<div id="app">
  <TheNavBar/>
  <section class='section top-section'>
      <router-view> </router-view>
  </section>
</div>
</template>


<script>
import TheNavBar from './layout/TheNavBar.vue';

export default {
  name: 'app',
  components: { TheNavBar  },
  created() {
    //initialize store data structure by submitting actions
    this.$store.dispatch('fetchClients');
  }
}
</script>

<style lang="scss">

$navbar-height: 4rem;

html, body {
  height: 100%;
  overflow: hidden;
}

.section {
  min-height: calc(100vh - ( #{$navbar-height} );
}


/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

*/
</style>

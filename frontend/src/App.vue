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
    this.$store.dispatch('clients/fetchClients');
  }
}
</script>



<style lang="scss">

$navbar-height: 4rem;

html, body {
  height: 100%;
  overflow: hidden;
}

.top-section {
  min-height: calc(100vh - ( #{$navbar-height} );
}

/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

*/
</style>

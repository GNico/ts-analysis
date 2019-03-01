<template>

<div id="app">
  <TheNavBar/>


<!--   <section class='section top-section'>
 -->      <router-view> </router-view>
<!--   </section>
 --></div>
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

::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}
 
::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3); 
    -webkit-border-radius: 10px;
    border-radius: 10px;
}
 
::-webkit-scrollbar-thumb {
    -webkit-border-radius: 10px;
    border-radius: 10px;
    background: rgba(50,60,61,0.8); 
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.5); 
}
::-webkit-scrollbar-thumb:window-inactive {
  background: rgba(50,60,61,0.4); 
}




/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

*/
</style>

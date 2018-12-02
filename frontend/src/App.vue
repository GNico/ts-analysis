<template>
  <div id="app">
    <BaseLayout></BaseLayout>

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
  created() {
    //initialize store data structure by submitting actions
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

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
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

</style>

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
</b-navbar>
</template>


<script>
  
export default {
}

</script>
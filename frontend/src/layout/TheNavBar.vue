<template>
<b-navbar>
  <template slot="brand">
    <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <img src="@/assets/img/keepconlogo.png" width="156" height="30">
    </b-navbar-item>
  </template>

  <template slot="start">
      <router-link to='/' exact class="navbar-item">Data Management</router-link>
      <router-link to='/Visualization' exact class="navbar-item">Visualization</router-link>
      <router-link to='/Analysis' exact class="navbar-item">Analysis</router-link>
      <router-link to='/Monitoring' exact class="navbar-item">Monitoring</router-link>
      <router-link to='/Test' exact class="navbar-item">Test</router-link>
  </template>

</b-navbar>
</template>


<script>
  
export default {
}

</script>
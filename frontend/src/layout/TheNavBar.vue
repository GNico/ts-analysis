<template>
<b-navbar>
  <template slot="brand">
    <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <img src="@/assets/img/keepconlogo.png" width="156" height="30">
    </b-navbar-item>
  </template>

  <template slot="start">
      <router-link to='/' exact class="navbar-item">Manage</router-link>
      <router-link to='/Visualize' exact class="navbar-item">Visualize</router-link>
      <router-link to='/Analize' exact class="navbar-item">Analize</router-link>
      <router-link to='/Alerts' exact class="navbar-item">Alerts</router-link>
      <router-link to='/Test' exact class="navbar-item">Test</router-link>
  </template>

</b-navbar>
</template>


<script>
  
export default {
}

</script>
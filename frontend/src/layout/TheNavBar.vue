<template>

<nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="https://keepcon.com/" >
        <img src="https://keepcon.com/assets/logowhite.svg" width="156" height="30">
      </a>
    </div>

    <div class="navbar-menu">
      <div class="navbar-start">
          <router-link to='/' exact class="navbar-item">Manage</router-link>

          <router-link to='/Visualize' exact class="navbar-item">Visualize</router-link>

          <router-link to='/Anomalies' exact class="navbar-item">Anomalies</router-link>

          <router-link to='/Alerts' exact class="navbar-item">Alerts</router-link>
      </div>
    </div>
</nav>  
 
</template>


<script>
  
export default {
}

</script>
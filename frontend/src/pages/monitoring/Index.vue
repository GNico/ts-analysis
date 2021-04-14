<template>
<div>
  <b-navbar :mobile-burger="false" class="lighter">       
    <template #brand>
      <router-link to="/Monitoring/Incidents"  class="navbar-item">Incidents</router-link>
      <router-link to="/Monitoring/Monitors" class="navbar-item">Monitors</router-link>
    </template>
  </b-navbar>

  <router-view></router-view>
</div>
</template>


<script>

</script>

<style scoped>
.lighter {
  filter: brightness(1.15);
}
</style>
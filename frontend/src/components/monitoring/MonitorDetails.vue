<template>
<div class="p-5">  

  <div class="title">Name: {{ $route.params.id }}</div>
  
  <b-tabs type="is-medium"  :animated="false"  destroy-on-hide>
    <b-tab-item label="Analysis list" icon="file-eye" value="Analysis">


      <div class="is-flex is-justify-content-space-between">
        <b-input placeholder="Search"> </b-input>
        <a class="button is-primary">
          <b-icon icon="playlist-plus"></b-icon>
          <span class="has-text-weight-semibold">Add analysis</span>
        </a>
      </div>


      <div class="card my-5">
        <header class="card-header">
            <div class="card-header-title is-justify-content-space-between">
              <span>An Analysis name</span>
              <div class="is-flex is-align-items-center">
                <div class="header-item"> Last run 23/4/2021, 10:01 am </div>
                <div class="header-item clickable" @click="deleteItem">                
                  <span class="icon"> 
                    <i class="mdi mdi-trash-can"></i>
                  </span>
                  Delete 
                </div>
                <b-switch v-model="active" left-label size="is-small" type="is-success" passive-type="is-danger" :rounded="false">{{active ? 'ONLINE' : 'DISABLED'}}</b-switch>
              </div>
            </div>        
        </header>
        <div class="card-content">
          <div class="content">
            Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras mattis consectetur purus sit amet fermentum.
          </div>
        </div>
      </div>     



    </b-tab-item>
    <b-tab-item label="Notification channels" icon="bell" value="Notifications">
      <span class="is-size-5"> Nothing here yet </span>
    </b-tab-item>
    
  </b-tabs>

  


</div>
</template>

<script>

export default {
  data() {
    return {
      active: true,
    }
  },
  methods: {
    deleteItem() {
      console.log("deleting")
    }
  },
  watch: {
    $route(to, from) {
      console.log("route change")
      console.log(to)
      console.log(from)
    }
  },
  created() {
    console.log("created")
  },
  mounted() {
    console.log("mounted")
  }
}

</script>


<style scoped>

.header-item {
  border-right: 1px solid;
  padding-right: 0.75rem;
  margin-right: 0.75rem;
}

.clickable {
  cursor: pointer;
  user-select: none;
}

</style>
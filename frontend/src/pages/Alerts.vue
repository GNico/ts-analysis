<template>

<div class="section  is-fullheight">
  
  <div class="columns">
    <div class="column is-6 is-offset-2 side-menu">
      <Pipeline/>
    </div>

  </div>

</div> 

</template>


<script>
import Pipeline from '../components/Pipeline';

export default {
    components: { Pipeline },
    data() {
      return {
        rowToOpen: '',
        openRows: [],
        selected: null,
        myArray: this.initial(),
        isOpen: 0,
        collapses: [
          {
              id: 1,
              title: 'Title 1',
              text: 'Text 1'
          },
          {
              id: 2,
              title: 'Title 2',
              text: 'Text 2'
          },
          {
              id: 3,
              title: 'Title 3',
              text: 'Text 3'
          },
        
        {
              id: 4,
              title: 'Title 4',
              text: 'Text 4'
          },
          {
              id: 5,
              title: 'Title 5',
              text: 'Text 5'
          },
          {
              id: 6,
              title: 'Title 6',
              text: 'Text 6'
          }
        ]
      }       
    },
    computed: {      
    
    },
    methods: {
      initial() {
        let arr = []
        for (var i = 0; i < 10; i++) {
          let item = {
            id: i.toString(),
            name: "item " + i
          }
          arr.push(item)
        }
        return arr
      },
    },
}

</script>



<style scoped>
.pipeline-item {
  display: flex;
  align-items: center;
  margin: 0 -0.25rem;
}

.pipeline-item .card {
  flex: 1;
  margin-bottom: 0.5rem;
}

.pipeline-item * {
  margin: 0 0.25rem;
}
</style>
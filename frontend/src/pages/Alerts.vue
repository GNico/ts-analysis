<template>

<div class="section  is-fullheight">
  
  <div class="columns">
    <div class="column is-6 side-menu">

 <!--   <draggable tag="div">

      <div class="pipeline-item" v-for="(collapse, index) of collapses">
        <b-collapse
          class="card"
          animation="slide"
          :key="collapse.id"
          :open="isOpen == collapse.id"
          @open="isOpen = collapse.id">
          <div slot="trigger" slot-scope="props" class="card-header">
            <p class="card-header-title">{{ collapse.title }}</p>
            <a class="card-header-icon">
              <b-icon :icon="props.open ? 'menu-down' : 'menu-up'"/>
            </a>
          </div>
          <div class="card-content">
            <div class="content">{{ collapse.text }}</div>
          </div>
        </b-collapse>


        <a class="button"> {{index + 1}} </a>
        <a class="button"> Delete </a>
      </div>


    </draggable>



      
    </div>

    <div class="column">
      <draggable 
        v-model="myArray" 
        group="people" 
        @start="drag=true" 
        @end="drag=false">
        <div v-for="element in myArray" :key="element.id" class="box">{{element.name}}</div>
      </draggable>

-->

    </div>
  </div>

</div> 

</template>


<script>
//import draggable from 'vuedraggable'

export default {
   // components: { draggable },
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
      openDetail() {
        this.openRows = [ this.rowToOpen ]

        this.$nextTick(function () {
          var element = document.getElementById(this.rowToOpen);
          element = element.parentNode.parentNode.parentNode.previousElementSibling

          var scrollamount = element.offsetTop


         // element.scrollIntoView({block: "start"});

          var table = document.getElementById("btable");
          var tableWrapper = null;
          for (var i = 0; i < table.childNodes.length; i++) {
              if (table.childNodes[i].className && table.childNodes[i].className.includes("table-wrapper")) {
                tableWrapper = table.childNodes[i];
                break;
              }
          }     
            
          if (tableWrapper) {
            tableWrapper.scroll(0, scrollamount - 40)
         //   if (! (tableWrapper.scrollHeight - tableWrapper.scrollTop  === tableWrapper.clientHeight))
         //     tableWrapper.scroll(0, tableWrapper.scrollTop - 40)
          }  
        })
      },
      closeDetail() {
        this.openRows = []
        //this.$refs.table.closeDetailRow({id: this.rowToOpen})
      }
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
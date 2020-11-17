<template>

<div class="section  is-fullheight">
  
  <b-input v-model="rowToOpen"> </b-input>
  <a class="button" @click="openDetail"> Open </a>
  <a class="button" @click="closeDetail"> Close </a> 


  <div class="columns">
    <div class="column is-4 side-menu">
      <b-table
        id="btable"
        :data="thedata"
        ref="table"
        detailed
        :selected.sync="selected"
        :opened-detailed="openRows"
        :height="700"
        sticky-header
        detail-key="id" >

        <template slot-scope="props">
          <b-table-column field="id" label="ID" width="40" numeric >
              {{ props.row.id }}
          </b-table-column>

          <b-table-column field="name" label="First Name" >
              <template>
                  {{ props.row.name}}
              </template>                
          </b-table-column>
        </template>


        <template slot="detail" slot-scope="props">
            <div :id="props.row.id">                    
              <p>
                  <strong>{{ props.row.name }}</strong>
                  <small>31m</small>
                  <br>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                  Proin ornare magna eros, eu pellentesque tortor vestibulum ut.
                  Maecenas non massa sem. Etiam finibus odio quis feugiat facilisis.
              </p>
            </div>
        </template>
      </b-table>
    </div>

    <div class="column">
      Something else
    </div>
  </div>

</div> 

</template>


<script>


export default {
    components: { },
    data() {
      return {
        rowToOpen: '',
        openRows: [],
        selected: null
      }       
    },
    computed: {
      thedata() {
        let arr = []
        for (var i = 0; i < 50; i++) {
          let item = {
            id: i.toString(),
            name: "item " + i
          }
          arr.push(item)
        }
        return arr
      }
    },
    methods: {
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



<style>

.section {
  padding: 1rem;
}


.is-fullheight {
  height: calc(100vh - 9rem);
  min-height: calc(100vh - 9rem);
}
  
.side-menu {
  overflow-y: auto;
}

.main-content {
  display: flex;
  flex-direction: column;
  overflow-y: overlay;
  overflow-x: hidden;
}
</style>
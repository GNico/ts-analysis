import api from "../api/repository";

export const tagsAndContexts = {
  data() {
    return {
      allTags: [],
      allContexts: []
    }
  },  
  computed: {
    contextsTree() {
      return { name: 'All contexts', id: "root", children: this.allContexts }
    },
    tagsTree() {
      return { name: 'All tags', id: "root", children: this.allTags }
    },
    displayContexts() {
      return { name: this.contextsTree.name, id: this.contextsTree.id, children: [] }
    },
    displayTags() {
      return { name: this.tagsTree.name, id: this.tagsTree.id, children: [] }
    },
  },
  methods: {
    updateContexts(name) {
      if (name) {
        return  api.getContexts(name)
              .then(response => {
                this.allContexts = response.data
              })
              .catch(error => { 
                  console.log('error loading contexts data');
              });
      } else {
        this.allContexts = []
      }
    },  
    updateTags(name) {
      if (name) {
        return  api.getTags(name)
              .then(response => {
                this.allTags = response.data
              })
              .catch(error => { 
                  console.log('error loading tags data');
              });  
      } else {
        this.allTags = []
      }
    }
  } 
}
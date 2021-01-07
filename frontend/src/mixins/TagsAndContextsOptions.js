import api from "../api/repository";

export const tagsAndContexts = {
  data() {
    return {
      allTags: [],
      allContexts: []
    }
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
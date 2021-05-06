<template>
<div class="columns">
  <div class="column is-12-mobile is-8-tablet is-6-desktop is-5-widescreen is-4-fullhd">
    <b-field >
      <b-input 
        ref="emailInput"
        expanded      
        v-model="email"
        placeholder="Email" 
        type="email" 
        icon="email"
        icon-right="close-circle"
        icon-right-clickable
        @icon-right-click="clearEmail"/>
      <p class="control">
        <b-button class="button is-primary" @click="addEmail">Add</b-button>
      </p>
    </b-field>


    <b-table
      v-if="emails.length"
      class="headerless-table"
      :data="emails">
      <b-table-column field="type" label="Type" v-slot="props">      
        {{props.row.email}}    
      </b-table-column>
      <b-table-column field="delete" label="D" v-slot="props" numeric>
        <button class="transparent-button" @click="deleteEmail(props.row.id)">
          <b-icon icon="trash-can" type="is-grey"></b-icon>
        </button>
      </b-table-column>
    </b-table>
  </div>
</div>
</template>


<script>
export default {
  props: {
    emails: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      email: ''
    }
  },
  methods: {
    clearEmail() {
      this.email = ''
    },
    deleteEmail(id) {
      this.$emit('delete', id)
    },
    addEmail() {
      if (this.email && this.$refs.emailInput.checkHtml5Validity()) {
        this.$emit('add', this.email)
      }
    }
  }
}
</script>

<style>
.headerless-table .table thead { 
  display: none; 
}
</style>
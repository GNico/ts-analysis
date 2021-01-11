<template>

  <b-collapse
    class="card"
    animation="slide"
    :open="false">
    <template #trigger="props">
        <div
            class="card-header"
            role="button"
        >
            <p class="card-header-title">
                {{ title }}
            </p>
            <a class="card-header-icon">
                <b-icon
                    :icon="props.open ? 'menu-down' : 'menu-up'">
                </b-icon>
            </a>
        </div>
    </template>
    <div class="card-content">
        <div class="content">
            {{ node }}
        </div>
    </div>
  </b-collapse>
</template>


<script>

export default {
  props: {
    path: {
      type: String,
      default: 'Unknown'
    },
    node: {
      type: Object,
      default: 'sarasa'
    }
  },
  data() {
    return {
      isOpen: false,
      text: 'Lorem ipsum'
    }
  },
  computed: {
    title() {
      return this.path + ' - ' + this.node.title
    }
  }
}

</script>

<style>
.card {
  max-width: 500px;
}
</style>
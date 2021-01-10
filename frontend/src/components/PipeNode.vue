<template>

  <b-collapse
    class="card"
    animation="slide"
    :open="isOpen == index"
    @open="isOpen = index">
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
            {{ text }}
        </div>
    </div>
  </b-collapse>
</template>


<script>

export default {
  props: {
    title: {
      type: String,
      default: 'Unknown'
    }
  },
  data() {
    return {
      isOpen: true,
      text: 'Lorem ipsum'
    }
  }
}

</script>

<style>
.card {
  max-width: 500px;
}
</style>
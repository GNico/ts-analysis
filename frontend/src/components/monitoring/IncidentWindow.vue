<template>
<VueDraggableResizable :w="1000" :h="500" :z="999" 
  :handles="['br']"
  @dragging="onDrag" 
  @resizing="onResize" 
  :drag-handle="'.drag'"
  :parent="false" >
  <div class="card drag" :style="{height: '100%'}">
    <header class="card-header">
      <p class="card-header-title">
        {{incident.id}}
      </p>
      <a class="button m-2 is-small"> X </a>
    </header>
    <div class="card-content">
      <div class="content">
        Lorem ipsum leo risus, porta ac consectetur ac, vestibulum at eros. Donec id elit non mi porta gravida 
        at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. 
        Cras mattis consectetur purus sit amet fermentum.
      </div>
    </div>
  </div>
</VueDraggableResizable>
</template>


<script>
import VueDraggableResizable from 'vue-draggable-resizable'

export default {
  components: { VueDraggableResizable },
  props: {
    incident: {
      type: Object,
      default: () => {return {}}    
    }
  },
  data() {
    return {
      width: 0,
      height: 0,
      x: 0,
      y: 0
    }
  },
  methods: {
    onResize: function (x, y, width, height) {
      this.x = x
      this.y = y
      this.width = width
      this.height = height
    },
    onDrag: function (x, y) {
      this.x = x
      this.y = y
    }
  },
  created() {
  }
}

</script>
<template>
<div>
<VueDraggableResizable :w="1000" :h="500" :z="999" 
  :handles="['br']"
  @dragging="onDrag" 
  @resizing="onResize" 
  :drag-handle="'.drag'"
  :parent="false" >
  <div class="card" :style="{height: '100%'}">
    <header class="card-header drag">
      <p class="card-header-title">
        {{incident.monitor}} → {{incident.analysis_name}}
      </p>
      <a class="button m-2 is-small" @click="$emit('close')"> X </a>
    </header>
    <div class="card-content" >
      <div class="content" >
        <BaseChart 
          :seriesData="chartData" 
          :bands="chartIncident"
          :style="myStyles"/>
      </div>
    </div>
  </div>
</VueDraggableResizable>
</div>
</template>


<script>
import VueDraggableResizable from 'vue-draggable-resizable'
import BaseChart from '@/components/BaseChart'

export default {
  components: { VueDraggableResizable, BaseChart },
  props: {
    incident: {
      type: Object,
      default: () => {return {}}    
    }
  },
  data() {
    return {
      width: 1000,
      height: 500,
      x: 0,
      y: 0,      
    }
  },
  computed: {
    chartData() {
      return [ {data: this.incident.series}]
    },
    chartIncident() {
      return [{ 
        id: 'p',
        from: Date.parse(this.incident.start),
        to: Date.parse(this.incident.end),
      }]
    },
    myStyles () {
      let h = this.height - 100
      let w = this.width - 50
      return {
        height: `${h}px`,
        width: `${w}px`,
      }
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
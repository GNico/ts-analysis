<template>
  <input type="range" class="slider" min="1" max="100" v-model:value="value" v-on:change="valueChangedEvent">
</template>

<script>
 
export default {
    data () {
        return {
            value: '1'

        }
    },
    methods: {
        valueChangedEvent () {
            this.$emit('valuechanged', {value: this.value})
        }
    }

} 

</script>


<style>
.slidecontainer {
    width: 100%;
}

.slider {
    -webkit-appearance: none;
    width: 100%;
    height: 25px;
 	  background: linear-gradient(to right, #0000FF, #FFFF00, #FF0000);
    outline: none;
    opacity: 1;
    -webkit-transition: .2s;
    transition: opacity .2s;
}

.slider:hover {
    opacity: 1;
}

slider:focus {
  outline: none; 
}


.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  border: 1px solid #000000;
  height: 36px;
  width: 16px;
  border-radius: 3px;
  background: #ffffff;
  cursor: pointer;
  margin-top: 0px; 
  box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d; 
}

.slider::-moz-range-thumb {
  box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;
  border: 1px solid #000000;
  height: 36px;
  width: 16px;
  border-radius: 3px;
  background: #ffffff;
  cursor: pointer;
}

.slider::-webkit-slider-runnable-track {
  background-color: transparent;
}

.slider::-moz-range-track {
  background-color: transparent;
}

</style>
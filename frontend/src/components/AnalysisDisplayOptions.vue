<template>
<div>

  <!-- <h3 class="title is-4">Display options</h3>

  <div class="field">
    <label class="label"> Analysis</label>
      <div class="field">
        <b-checkbox >
            Show anomalies
        </b-checkbox>
      </div>
      <div class="field ">
        <b-checkbox >
            Show baseline
        </b-checkbox>
      </div>

      <b-field class=""  label="Display threshold">
              <input type="range" min="1" max="100" value="50" class="slider" id="myRange">    
      </b-field>
  </div>


  <div class="field">
      <label class="label"> Color </label>
      <SelectColor/> 
  </div>

  <div class="field">
    <label class="label"> Chart type </label>
    <div class="select">
      <select >
            <option>line</option>
            <option>areaspline</option>
            <option>spline</option>
            <option>scatter</option>
            <option>column</option>
            <option>area</option>
        </select>
    </div>
  </div>
 -->



  
</div>
</template>


<script>

import SelectColor from './SelectColor.vue';


export default {
  components: { SelectColor }
}

</script>

<style>


</style>
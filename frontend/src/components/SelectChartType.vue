<template>

<div class="select">
  <select :value="value" @change="$emit('input', $event.target.value)">
    <option>line</option>
    <option>areaspline</option>
    <option>spline</option>
    <option>scatter</option>
    <option>column</option>
    <option>area</option>
</select>
</div>

</template>



<script>
    
export default {
    props: {
        value: {
            type: String,
            default: "line"
        }
    },
}


</script>
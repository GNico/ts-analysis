<template>
<div class="level">
    <div class="level-left">
        <div class="level-item">
            <input id="colorPicker" v-if="colorInputIsSupported" type="color" value="#6fcd98" v-model="currentColor" v-on:change="colorSelected">
            <select v-else v-model="currentColor" v-on:change="colorSelected">
                <option>Red</option>
                <option>Green</option>
                <option>Blue</option>
                <option>Pink</option>
                <option>Orange</option>
                <option>Brown</option>
                <option>Black</option>
                <option>Purple</option>
            </select>
        </div>
        <div class="level-item">
            <p>{{currentColor}}</p>
        </div>
    </div>
</div>
</template>


<script>

export default {
    name: "ColorSelect",
    data () {
        return {
            currentColor: '#6fcd98',
            colorInputIsSupported: null,
        }
    },
    created () {
        let i = document.createElement('input')
        i.setAttribute('type', 'color');
        (i.type === 'color') ? this.colorInputIsSupported = true : this.colorInputIsSupported = false
    },
    methods: {
        colorSelected () {
            this.$emit('selected', {selected: this.currentColor})
        }
    }
}
    

</script>
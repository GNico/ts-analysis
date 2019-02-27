<template>
<div class="level">
    <div class="level-left">
        <div class="level-item">
            <input id="colorPicker" v-if="colorInputIsSupported" type="color" :value="value" @change="colorSelected">
            <select v-else  value="Green" @change="colorSelected">
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
            {{ value }}
        </div>
    </div>
</div>
</template>


<script>

export default {
    props: {
        value: { 
            required: true,
        }
    },
    data () {
        return {
            colorInputIsSupported: null,
        }
    },
    created () {
        let i = document.createElement('input')
        i.setAttribute('type', 'color');
        (i.type === 'color') ? this.colorInputIsSupported = true : this.colorInputIsSupported = false
    },
    methods: {
        colorSelected (event) {
            this.$emit('input', event.target.value)
        }
    }
}
    

</script>
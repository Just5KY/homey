<template>
  <div :class="'option-toggle-switch option-toggle-switch' + getClassMod">
    <input class="option-toggle-switch__checkbox"
      type="checkbox"
      :value="val"
      :checked="val"
      @input="toggle"
    >
    <div :class="'option-toggle-switch__slider option-toggle-switch__slider' + getClassMod"></div>
  </div>
</template>

<script>
export default {
    name: 'OptionToggleSwitch',
    data(){
        return {
            localVal: false
        }
    },
    props: {
        val: Boolean,
    },
    computed: {
        getClassMod(){
            return (this.localVal) ? '--enabled' : '';
        }
    },
    emits: ['update:val'],
    methods: {
        toggle(){
            this.localVal = !this.localVal
            this.$emit('update:val', this.localVal)
        }
    },
    created() {
        this.localVal = this.val;
    }
}
</script>

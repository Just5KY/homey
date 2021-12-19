
<template>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            {{ header }}
          </div>

          <div class="modal-body">
            <slot name="body">
              default body
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              default footer
              <button @click="$emit('close')" class="modal-default-button">
                Save
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
    name: 'OptionsPopup',
    props: {
        header: String,
        body: String,
        footer: String,
    }
}
</script>


<template>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <h2>Settings</h2>
          </div>
          <div class="modal-body">
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. Saepe quas qui at sapiente et, illum dolores blanditiis aliquam incidunt! Consectetur iure, ipsum odit dolorem aspernatur molestias repellendus nemo explicabo illo!
          </div>
          <div class="modal-footer">
            <button @click="$emit('close')" class="modal-button">
              Save
            </button>
            <button @click="$emit('close')" class="modal-button modal-button__cancel">
              Cancel
            </button>
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

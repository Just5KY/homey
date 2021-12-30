
<template>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <h2>Settings</h2>
          </div>
          <div class="modal-body">
            <ul>
              <li class="modal-option">
                <h3>Dashboard Title</h3>
                <div class="modal-option__button-container">
                  <input v-model="localConfig.title">
                </div>
              </li>
              <li class="modal-option">
                <h3>Minimal Mode</h3>
                <div class="modal-option__button-container">
                  On<input type="radio" :value="true" v-model="localConfig.minimal_mode">
                  Off<input type="radio" :value="false" v-model="localConfig.minimal_mode">
                </div>
              </li>
              <li class="modal-option">
                <h3>Service Status Indicators</h3>
                <div class="modal-option__button-container">
                  On<input type="radio" :value="true" v-model="localConfig.enable_service_status">
                  Off<input type="radio" :value="false" v-model="localConfig.enable_service_status">
                </div>
              </li>
              <li v-if="!localConfig.minimal_mode" class="modal-option">
                <h3>Docker Backend</h3>
                <div class="modal-option__button-container">
                  <select v-model="localConfig.docker_api_backend">
                    <option value="docker">Docker</option>
                    <option value="portainer">Portainer</option>
                  </select>
                </div>
              </li>
            </ul>
          </div>
          <div class="modal-footer">
            <button @click="close(true)" class="modal-button">
              Save
            </button>
            <button @click="close(false)" class="modal-button modal-button__cancel">
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
  data: function() {
    return {
      localConfig: Object,
    };
  },
  props: {
      header: String,
      body: String,
      footer: String,
      config: Object,
  },
  created: function() {
    this.localConfig = this.config;
  },
  methods: {
    close(shouldSave) {
      this.$emit('close');

      if (shouldSave) this.$emit('saveConfig');
      else            this.$emit('loadConfig');
    },
  },
}
</script>

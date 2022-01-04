
<template>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div v-if="!showServices" class="modal-container">

          <div class="modal-header">
            <h2>Settings</h2>
          </div>

          <div class="modal-body">
            <ul>
              <li class="modal-option">
                <h3>Title</h3>
                <div class="modal-option__button-container">
                  <input v-model="localConfig.title">
                </div>
              </li>
              <li class="modal-option">
                <h3>Minimal Mode<span :title="this.minimalModeWarning" class="material-icons-outlined">info</span></h3>
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
            <button @click="showServices = !showServices" class="modal-button modal-button__services">Services...</button>
            <button @click="close(false)" class="modal-button modal-button__cancel">Cancel</button>
            <button @click="close(true)" class="modal-button modal-button__save">Save</button>
          </div>

        </div>
        <div v-else class="modal-container">
          <div class="modal-header">
            <h2>Services</h2>
          </div>

          <div class="modal-body">
              <div class="modal-option__header">
                  <select v-model="selectedService">
                    <option value="newService">New Service</option>
                    <option v-for="s in localConfig.services" :key="s.name" :value="s.name">{{s.name}}</option>
                  </select>
              </div>
              <div class="service-editor">
                <div class="service-editor__image-container">
                  <img v-if="getSelectedService.icon" 
                    :src="'./images/icons/'+getSelectedService.icon" 
                    class="service-editor__image-container__image" />
                  <label for="uploader">
                    <span v-if="getSelectedService.icon" title="Upload New Image" id="upload_corner" class="material-icons-outlined">file_upload</span>
                    <span v-else id="upload_placeholder" title="Upload Image" class="material-icons-outlined">file_upload</span>
                  </label>
                  <input type="file" id="uploader" accept="image/png, image/jpeg" @change="fileUploaded" />
                </div>
                <div class="service-editor__options">
                  <ul>
                    <li class="modal-option">
                      <h3>Name</h3>
                      <div class="modal-option__button-container">
                        <input v-model="getSelectedService.name">
                      </div>
                    </li>
                    <li class="modal-option">
                      <h3>Subtitle</h3>
                      <div class="modal-option__button-container">
                        <input v-model="getSelectedService.subtitle">
                      </div>
                    </li>
                    <li class="modal-option">
                      <h3>URL</h3>
                      <div class="modal-option__button-container">
                        <input v-model="getSelectedService.url">
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
          </div>

          <div class="modal-footer">
            <button @click="close(false)" class="modal-button modal-button__cancel">Cancel</button>
            <button @click="close(false)" class="modal-button modal-button__save">Save</button>
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
      showServices: false,
      selectedService: "newService",
      minimalModeWarning: "Make homey more like Homer (disable all API functionality).\n\nOnce minimal mode is enabled, it can only be disabled by manually editing config.yml.",
    };
  },
  props: {
      header: String,
      body: String,
      footer: String,
      config: Object,
  },
  computed: {
    getSelectedService() {
      for(let i = 0; i < this.localConfig.services.length; i++) {
        if (this.localConfig.services[i].name == this.selectedService)  return this.localConfig.services[i];
      }
      return {'name': '', 'icon': '', 'subtitle': '', 'url': ''};
    },
  },
  created: function() {
    this.localConfig = this.config;
  },
  methods: {
    // close(true) will write newly selected settings to config.yml
    // close(false) will discard newly selected settings by reloading config.yml
    close(shouldSave) {
      this.$emit('close');

      if (shouldSave) this.$emit('saveConfig');
      else            this.$emit('loadConfig');
    },
    fileUploaded() {
      let img = this.$el.querySelector('#uploader').files[0];
      // load image into UI immediately
      // do not send AJAX upload until saveConfig is emitted
    }
  },
}
</script>

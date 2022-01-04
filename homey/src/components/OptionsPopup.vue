
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

        <!-- services panel -->

        <div v-else class="modal-container">
          <div class="modal-header">
            <h2>Services</h2>
          </div>

          <div class="modal-body">
              <div class="modal-option__header">
                  <select @change="dropdownUpdated" v-model="selectedService">
                    <option value="newService">New Service</option>
                    <option v-for="s in localConfig.services" :key="s.name" :value="s.name">{{s.name}}</option>
                  </select>
              </div>
              <div class="service-editor">
                <div class="service-editor__image-container">
                  <img v-if="getSelectedService.icon && !newImage" 
                    :src="'./images/icons/'+getSelectedService.icon" 
                    class="service-editor__image-container__image" />
                  <img v-if="newImage"
                    :src="newImage" 
                    class="service-editor__image-container__image" />
                  <label for="uploader">
                    <span v-if="getSelectedService.icon || newImage" title="Upload New Image" id="upload_corner" class="material-icons-outlined">file_upload</span>
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
            <button @click="close(true)" class="modal-button modal-button__save">{{getSaveString}}</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

// TODO: only new values from selected service should be saved
// TODO: add browse icons button/field to select previously uploaded icon

export default {
  name: 'OptionsPopup',
  data: function() {
    return {
      localConfig: Object,
      showServices: false,
      selectedService: "newService",
      newService: {'name': '', 'icon': '', 'subtitle': '', 'url': ''},
      newImage: null,
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
      return this.newService;
    },
    getSaveString() {
      return 'Save' + (this.newImage ? ' & Upload' : '');
    }
  },
  created: function() {
    this.localConfig = this.config;
  },
  methods: {
    // close(true) will write newly selected settings to config.yml
    close(shouldSave) {
      if (shouldSave){
        if(this.selectedService == 'addService') {
          if(!this.newImage) console.log("Error creating new service: Image is required.")
          else if(this.newService.name == '' || this.newService.url == '') {
            console.log("Error saving service: Name & URL are required.");
          }
          else {
            this.uploadIcon();
            this.localConfig.services.push(this.newService);
            this.$emit('saveConfig');
          }
        }
        else {
          let toUpdate = this.getSelectedService;
          if(toUpdate.name == '' || toUpdate.url == ''){
            console.log("Error saving service: Name & URL are required.");
          }
          else{
            if(this.newImage){
              this.uploadIcon();
              toUpdate.icon = this.$el.querySelector('#uploader').files[0].name;
            }
            this.$emit('saveConfig');
          }
        }
      }
      // close(false) will discard newly selected settings by reloading config.yml
      else  this.$emit('loadConfig');

      this.$emit('close');
    },
    fileUploaded() {
      let files = this.$el.querySelector('#uploader').files;
      
      // load image into UI for previewing
      let fr = new FileReader();
      fr.onload = e => { this.newImage = e.target.result; }
      fr.readAsDataURL(files[0]);
    },
    uploadIcon() {
      let files = this.$el.querySelector('#uploader').files;
      this.newService.icon = files[0].name;

      // attempt to save image to public/images/icons folder
      let fd = new FormData();
      fd.append("image", files[0])
      let header = {'Content-Type': 'multipart/form-data'}
      this.axios.post('http://0.0.0.0:9101/uploadIcon', fd, 
        {headers: header}).then((res) => {
          if(res.data['Success']){
            // Successful image upload
          }
          else  console.log('Error uploading icon: ' + res.data['Error']);
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
    dropdownUpdated: function() {
      this.newImage = null;
    },
  },
}
</script>

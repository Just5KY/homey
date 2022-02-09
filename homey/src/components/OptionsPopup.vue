
<template>
    <!-- main settings menu -->
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div v-if="!showServices && !showCards && !showBookmarks" class="modal-container">

          <div class="modal-header">
            <h2>Settings</h2>
          </div>

          <div class="modal-body">
            <ul>
              <TransitionGroup name="smooth-list">
              <li class="modal-option" :key="1">
                <h3>Title</h3>
                <div class="modal-option__button-container">
                  <input class="option-text-field" v-model="localConfig.title">
                </div>
              </li>
              <li class="modal-option" :key="2">
                <h3>Minimal Mode<span :title="this.minimalModeWarning" class="material-icon icon-info"></span></h3>
                <OptionToggleSwitch v-model:val="localConfig.minimal_mode" />
              </li>
              <li v-if="!localConfig.minimal_mode" class="modal-option" :key="3">
                <h3>3D House</h3>
                <OptionToggleSwitch v-model:val="localConfig.show_house" />
              </li>
              <li class="modal-option" :key="4">
                <h3>Compact Services</h3>
                <OptionToggleSwitch v-model:val="localConfig.compact_services" />
              </li>
              <li v-if="!localConfig.minimal_mode" class="modal-option" :key="5">
                <h3>Status Indicators</h3>
                <OptionToggleSwitch v-model:val="localConfig.enable_service_status" />
              </li>
              <li class="modal-option" :key="6">
                <h3>Bookmarks in Header</h3>
                <OptionToggleSwitch v-model:val="localConfig.bookmarks_in_header" />
              </li>
              <li class="modal-option" :key="7">
                <h3>Notifications
                  <span :title="'Website-level alerts for errors & selected events.\nNo browser permissions required.'" class="material-icon icon-info"></span>
                </h3>
                <OptionToggleSwitch v-model:val="localConfig.enable_notifications" />
              </li>
              <li v-if="localConfig.enable_notifications" class="modal-option" :key="8">
                <h3>Audio Notifications</h3>
                <OptionToggleSwitch v-model:val="localConfig.audio_notifications" />
              </li>
              <li v-if="!localConfig.minimal_mode" class="modal-option" :key="9">
                <h3>Docker Backend</h3>
                <div class="modal-option__button-container">
                  <select class="option-dropdown-menu" v-model="localConfig.docker_api_backend">
                    <option value="docker">Docker</option>
                    <option value="portainer">Portainer</option>
                  </select>
                </div>
              </li>
              </TransitionGroup>
            </ul>
          </div>

          <div class="modal-footer">
            <button @click="showServices = !showServices" class="modal-button modal-button__services">Services</button>
            <button @click="showBookmarks = !showBookmarks" class="modal-button modal-button__bookmarks">Bookmarks</button>
            <button @click="showCards = !showCards" class="modal-button modal-button__cards">Cards</button>
            <button @click="close(false)" class="modal-button modal-button__cancel">Cancel<span class="material-icon icon-arrow_right"></span></button>
            <button @click="close(true)" class="modal-button modal-button__save">Save<span class="material-icon icon-check"></span></button>
          </div>

        </div>

        <!-- service editor sub-menu -->

        <div v-if="showServices" class="modal-container">
          <div class="modal-header">
            <h2>Services</h2>
          </div>

          <div class="modal-body">
              <div class="modal-option__header">
                  <select @change="dropdownUpdated" v-model="selectedService" class="option-dropdown-menu">
                    <option value="newService">New Service</option>
                    <option v-for="(s, i) in localConfig.services" :key="i" :value="s.name">{{s.name}}</option>
                  </select>
              </div>
              <div class="service-editor">
                <div class="service-editor__image-container">
                  <img v-if="getSelectedService().icon && !newImage" 
                    :src="'./data/icons/'+getSelectedService().icon" 
                    class="service-editor__image-container__image"
                    onerror="this.onerror=null; this.src='data/icons/default.png'" />
                  <img v-if="newImage"
                    :src="newImage" 
                    class="service-editor__image-container__image"
                    onerror="this.onerror=null; this.src='data/icons/default.png'" />
                  <label for="uploader">
                    <transition name="slide-up">
                      <span v-if="(getSelectedService().icon || newImage || newService.icon != '') && !showGallery" 
                        title="Upload New Icon" 
                        class="uploader-button uploader-button__corner-right uploader-button__corner material-icon icon-upload_file">
                        </span>
                    </transition>
                    <transition v-if="selectedService == 'newService'" name="fade">
                      <span v-if="!showGallery && !getSelectedService().icon && !newImage && newService.icon ==''" 
                        class="uploader-button material-icon icon-upload_file" id="upload_placeholder" title="Upload Icon">
                        </span>
                    </transition>
                  </label>
                  <input type="file" id="uploader" ref="uploader" accept="image/png, image/jpeg" @change="fileUploaded" />
                  <transition name="fade">
                    <span v-if="!showGallery" title="Browse Uploaded Icons" @click="showGallery = !showGallery"
                        class="uploader-button uploader-button__corner-left uploader-button__corner material-icon icon-image">
                    </span>
                    <span v-else title="Cancel" @click="showGallery = !showGallery"
                        class="uploader-button uploader-button__corner-left uploader-button__corner material-icon icon-close">
                    </span>
                  </transition>
                  <transition name="slide-up">
                    <IconGallery v-if="showGallery" @selectIcon="selectNewIcon" />
                  </transition>
                </div>
                <div class="service-editor__options">
                  <ul>
                    <li class="modal-option">
                      <h3>Name</h3>
                      <div class="modal-option__button-container">
                        <input class="option-text-field" v-model="localServiceName">
                      </div>
                    </li>
                    <li class="modal-option">
                      <h3>Subtitle</h3>
                      <div class="modal-option__button-container">
                        <input class="option-text-field" v-model="getSelectedService().subtitle">
                      </div>
                    </li>
                    <li class="modal-option">
                      <h3>URL</h3>
                      <div class="modal-option__button-container">
                        <input class="option-text-field" v-model="getSelectedService().url">
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
          </div>
  
          <div class="modal-footer">
            <transition name="fade">
              <button v-if="selectedService != 'newService'" 
                @click="deleteService(getSelectedService())" 
                class="modal-button modal-button__delete">
                Delete</button>
            </transition>
            <button @click="showServices = !showServices" class="modal-button modal-button__cancel">
              Back<span class="material-icon icon-arrow_right"></span></button>
            <button @click="close(true)" class="modal-button modal-button__save">
              {{getSaveString}}<span class="material-icon icon-check"></span></button>
          </div>
        </div>
      
        <!-- show/hide cards sub-menu -->

        <div v-if="showCards" class="modal-container">
          <div class="modal-header">
            <h2>Cards</h2>
          </div>

          <div class="modal-body">
            <ul>
              <li v-for="c in localConfig.cards" :key="c.name" class="modal-option">
                <h3>{{ c.name }}</h3>
                <OptionToggleSwitch v-model:val="c.enable" />
              </li>
            </ul>
          </div>
  
          <div class="modal-footer">
            <transition name="fade">
              <button v-if="selectedService != 'newService'" 
                @click="deleteService(getSelectedService())" 
                class="modal-button modal-button__delete">
                Delete</button>
            </transition>
            <button @click="showCards = !showCards" class="modal-button modal-button__cancel">Back<span class="material-icon icon-arrow_right"></span></button>
            <button @click="close(true)" class="modal-button modal-button__save">{{getSaveString}}<span class="material-icon icon-check"></span></button>
          </div>
        </div>

        <!-- bookmark editor sub-menu -->

        <div v-if="showBookmarks" class="modal-container">
          <div class="modal-header">
            <h2>Bookmarks</h2>
          </div>

          <div class="modal-body">
            <div class="modal-option__header">
                <select @change="localBookmarkName = getSelectedBookmark().name;" 
                  v-model="selectedBookmark" class="option-dropdown-menu">
                  <option value="newBookmark">New Bookmark</option>
                  <option v-for="(b, i) in localConfig.bookmarks" :key="i" :value="b.name">{{b.name}}</option>
                </select>
            </div>
            <ul>
              <li class="modal-option">
                <h3>Name</h3>
                <div class="modal-option__button-container">
                  <input class="option-text-field" v-model="localBookmarkName">
                </div>
              </li>
              <li class="modal-option">
                <h3>URL</h3>
                <div class="modal-option__button-container">
                  <input class="option-text-field" v-model="getSelectedBookmark().url">
                </div>
              </li>
              <li class="modal-option">
                <h3>Hover Text</h3>
                <div class="modal-option__button-container">
                  <input class="option-text-field" v-model="getSelectedBookmark().hover"
                    placeholder="Optional">
                </div>
              </li>
            </ul>
          </div>
  
          <div class="modal-footer">
            <transition name="fade">
              <button v-if="selectedBookmark != 'newBookmark'" 
                @click="deleteBookmark(getSelectedBookmark() /* CREATE THIS METHOD */)" 
                class="modal-button modal-button__delete">
                Delete</button>
            </transition>
            <button @click="showBookmarks = !showBookmarks" class="modal-button modal-button__cancel">Back<span class="material-icon icon-arrow_right"></span></button>
            <button @click="close(true)" class="modal-button modal-button__save">{{getSaveString}}<span class="material-icon icon-check"></span></button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import IconGallery from './IconGallery.vue';
import OptionToggleSwitch from './OptionToggleSwitch.vue';

export default {
  name: 'OptionsPopup',
  data: function() {
    return {
      localConfig: Object,
      showServices: false,
      showCards: false,
      showBookmarks: false,
      newService: {'name': '', 'icon': '', 'subtitle': '', 'url': ''},
      selectedService: 'newService',
      newBookmark: {'name': '', 'hover': '', 'url': ''},
      selectedBookmark: 'newBookmark',
      localServiceName: String,
      localBookmarkName: String,
      newImage: null,
      showGallery: false,
      servicesDeleted: false,
      minimalModeWarning: "Disables all API functionality & 3D eyecandy to save resources.\n\nOnce minimal mode is enabled, it can only be disabled by editing config.yml.",
    };
  },
  components: {
    IconGallery,
    OptionToggleSwitch
  },
  props: {
      header: String,
      body: String,
      footer: String,
      config: Object,
  },
  computed: {
    getSaveString() {
      return 'Save' + (this.newImage ? ' & Upload' : '');
    }
  },
  created: function() {
    this.localConfig = this.config;
    this.localServiceName = '';
    this.localBookmarkName = '';
  },
  methods: {
    // close(true) will write newly selected settings to config.yml
    close(shouldSave) {
      if (shouldSave){
        // save main options
        if( (!this.showServices && !this.showBookmarks) || this.servicesDeleted ){
          this.$emit('saveConfig');
          this.$emit('close');
          return;
        }

        // save bookmarks
        if(this.showBookmarks) {
          // create new bookmark
          if(this.selectedBookmark == 'newBookmark') {
            this.newBookmark.name = this.localBookmarkName;
            if(this.newBookmark.name == '' || this.newBookmark.url == '') {
              console.error("Error creating bookmark: Name & URL are required.");
              this.$emit('close');
              return;
            }
            else {
              this.localConfig.bookmarks.push(this.newBookmark)
            }
          }
          // update existing bookmark
          else {
            let toUpdate = this.getSelectedBookmark();
            toUpdate.name = this.localBookmarkName;
            if(toUpdate.name == '' || toUpdate.url == ''){
              console.log("Error saving bookmark: Name & URL are required.");
              this.$emit('close');
              return;
            }
          }
          this.$emit('saveConfig');
          return;
        }

        // add new service
        if(this.selectedService == 'newService') {
          this.newService.name = this.localServiceName;
          if(this.newService.icon == '' && !this.newImage) console.error("Error creating new service: Image is required.")
          else if(this.newService.name == '' || this.newService.url == '') {
            console.error("Error creating service: Name & URL are required.");
          }
          // upload new image
          else {
            if(this.newImage){
              this.uploadIcon(this.$refs.uploader.files[0]);
              this.newService.icon = this.$refs.uploader.files[0].name;
            }
            this.localConfig.services.push(this.newService);
            this.$emit('saveConfig');
          }
        }
        // update existing service
        else {
          let toUpdate = this.getSelectedService();
          toUpdate.name = this.localServiceName;
          if(toUpdate.name == '' || toUpdate.url == ''){
            console.log("Error saving service: Name & URL are required.");
          }
          else{
            // upload new image if selected
            if(this.newImage){
              this.uploadIcon(this.$refs.uploader.files[0]);
              toUpdate.icon = this.$refs.uploader.files[0].name;
            }
            for(let i = 0; i < this.localConfig.services.length; i++) {
              if (this.localConfig.services[i].name == this.selectedService)  this.localConfig.services[i] = this.getSelectedService()
            }
            this.$emit('saveConfig');
          }
        }
      }

      // close(false) will discard newly selected settings by reloading config.yml
      else  this.$emit('loadConfig');
      // close modal either way
      this.$emit('close');
    },
    // get dropdown selected service
    // can't v-model on name as it can be edited
    getSelectedService() {
      for(let i = 0; i < this.localConfig.services.length; i++) {
        if (this.localConfig.services[i].name == this.selectedService)  {
          return this.localConfig.services[i];
        }
      }

      return this.newService;
    },
    getSelectedBookmark() {
      for(let i = 0; i < this.localConfig.bookmarks.length; i++) {
        if (this.localConfig.bookmarks[i].name == this.selectedBookmark)  {
          return this.localConfig.bookmarks[i];
        }
      }

      return this.newBookmark;
    },
    // remove a service from the list & flag it for deletion from config file
    // changes are discarded if user does not hit 'Save' after
    deleteService(service){
      this.localConfig.services.splice(this.localConfig.services.indexOf(service), 1);
      this.selectedService = 'newService'
      this.localServiceName = ''
      this.servicesDeleted = true;
    },
    deleteBookmark(bookmark) {
      this.localConfig.bookmarks.splice(this.localConfig.bookmarks.indexOf(bookmark), 1);
      this.selectedBookmark = 'newBookmark';
      this.localBookmarkName = '';
      this.servicesDeleted = true;
    },
    selectNewIcon(filename){
      this.newImage = null;
      if(this.getSelectedService() == 'newService'){
        this.newService.icon = filename;
      }
      else this.getSelectedService().icon = filename;
      this.showGallery = false;
    },
    // load image (into page) from file picker dialog
    fileUploaded(event) {
      let files = event.target.files;
      
      // load image into UI for previewing
      let fr = new FileReader();
      fr.onload = e => { this.newImage = e.target.result; }
      fr.readAsDataURL(files[0]);
    },
    // upload icon from filepicker
    uploadIcon(file) {
      this.newService.icon = file.name;

      // attempt to save image to public/data/icons
      let fd = new FormData();
      fd.append("image", file)
      let header = {'Content-Type': 'multipart/form-data'}
      this.axios.post('/api/uploadIcon', fd, 
        {headers: header}).then((res) => {
          if(res.data['Success']){
            // Successful image upload
          }
          else  console.error('Error uploading icon: ' + res.data['Error']);
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
    dropdownUpdated: function() {
      this.newImage = null;
      this.newService.icon = '';
      this.showGallery = false;
      this.localServiceName = this.getSelectedService().name;
    },
  },
}
</script>

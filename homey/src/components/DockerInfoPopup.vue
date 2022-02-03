
<template>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container modal-container--large">

          <div class="modal-header">
            <h2>Statistics &amp; Logs for {{ details.stats.name.substring(1) }}
              <span class="material-icon icon-info"></span>
            </h2>
          </div>

          <div class="modal-body">
            <div class="docker-info--stats">
              <ul>
                <li v-for="stat in details.stats" :key="stat">
                  <p>{{ stat }}</p>
                </li>
              </ul>
            </div>
            <h3>Log</h3>
            <div class="docker-info--log">
              <ul>
                <li v-for="line in reversedLog" :key="line">
                  <p>{{ line }}</p>
                </li>
              </ul>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="close" class="modal-button modal-button__save">OK</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

export default {
  name: 'DockerInfoPopup',
  data: function() {
    return {
    };
  },
  props: {
      details: {},
  },
  computed: {
    reversedLog() {
      let d = this.details.log.map(e => e);
      return d.reverse();
    }
  },
  created: function() {
    console.log(this.details.stats)
  },
  methods: {
    // close(true) will write newly selected settings to config.yml
    close(shouldSave) {
      this.$emit('close');
    },
  },
}
</script>

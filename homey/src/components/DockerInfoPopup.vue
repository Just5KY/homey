
<template>
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container modal-container--large">

          <div class="modal-header">
            <h2>Statistics &amp; logs for {{ details.stats.name.substring(1) }}
              <span class="material-icon icon-info"></span>
            </h2>
          </div>

          <div class="modal-body">
            <div class="docker-info--stats">
              <pre ref="jsonContainer" 
                class="docker-info--stats__json">{{ prettyPrintedStats }}</pre>
            </div>
            <div class="docker-info--log">
              <ul>
                <li v-for="line in reversedLog" :key="line">
                  <p>{{ line }}</p>
                </li>
              </ul>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="this.$emit('close')" class="modal-button modal-button__save">OK</button>
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
    prettyPrintedStats() {
      return JSON.stringify(this.details.stats, null, 2);
    },
    reversedLog() {
      let deepCopy = this.details.log.map(ele => ele);
      return deepCopy.reverse();
    }
  },
}
</script>

import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import VueAxios from 'vue-axios';
import Notifications from '@kyvg/vue3-notification';
//import '@material-design-icons/font'

// Vue entrypoint
const app = createApp(App);

app.use(VueAxios, axios)
app.use(Notifications)

app.config.globalProperties.axios=axios
app.config.globalProperties.window=window

app.mount('#app')
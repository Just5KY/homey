<template>
  <div class="weather-card-container">
    <h2>Weather</h2>
    <div v-for="w in weatherData" 
      :key="w.time" class="weatherElement" >
      {{w.time}}<span><skycon :title="w.weather_type" 
        size="16" color="#F8F8F2" 
        :condition="getSkycon(w.weather_type)"
      /> {{w.temp}}F </span>
    </div>
  </div>
</template>

<script>
import Skycon from "vue-skycons";

export default {
  name: 'WeatherCard',
  components: {
    Skycon
  },
  props: {
      title: String,
  },
  data () {
    return {
      weatherData: Array,
      currentWeatherType: String,
    }
  },
  computed: {
    /*
   <skycon condition="clear-day" />
    <skycon condition="clear-night" />
    <skycon condition="partly-cloudy-day" />
    <skycon condition="partly-cloudy-night" />
    <skycon condition="cloudy" />
    <skycon condition="rain" />
    <skycon condition="sleet" />
    <skycon condition="snow" />
    <skycon condition="wind" />
    <skycon condition="fog" />
    <skycon condition="rain" size="128" color="orangered" paused @load="console.log" />
    */
    
  },
  methods: {
    getHourlyWeather: function() {
        let today = new Date().toJSON().slice(0, 10).replaceAll('-', '');
        this.axios.get('http://0.0.0.0:9101/weatherHourly/' + today).then((res) => {
          this.weatherData = res.data.slice(0,9);
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
    getSkycon: function(weatherType){
      switch(weatherType){
        case 'Light Snow Showers':
        case 'Light Snow':
          return 'snow'

        case 'Overcast':
        case 'Partly Cloudy':
          return 'cloudy'
        
      }
        return 'clear-day'
    },
  },
  beforeMount() {
      this.getHourlyWeather();
  },
}
</script>

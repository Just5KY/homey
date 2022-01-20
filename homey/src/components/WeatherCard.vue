<template>
  <div :class="getClass" @click="isFlipped = !isFlipped" @mouseleave="isFlipped = false">
      <div class="weather-card-container__side weather-card-container__side--front">
          <skycon class="weather-card-container__background--skycon" v-if="weatherDataHourly.length > 1" 
                :title="getCurrentWeather.weather_type" size=128 color="#44475a" :condition="getSkycon(getCurrentWeather.weather_type)"/>
          <div class="weather-card-container__heading">
            <div class="weather-card-container__heading--daily-details">
              <div>{{getCurrentWeather.temp}}°F</div>
              <div>{{getCurrentWeather.weather_type}}</div>
            </div>
            <span class="weather-card-container__heading--title">Weather</span>
          </div>
          <div class="weather-card-container__details">
              <div v-for="w in weatherDataHourly" :title="w.weather_type" 
                :key="w.time" class="weather-element" >
                <p>{{w.time}}</p>
                <p>{{w.temp}}°F</p>
                  <skycon class="weather-element__skycon" 
                    size="16" color="#F8F8F2" 
                    :condition="getSkycon(w.weather_type)"
                  /> 
              </div>
          </div>
      </div>
      <div class="weather-card-container__side weather-card-container__side--back">
          <div class="weather-card-container__weekly-forecast">
            <ul>
              <li v-for="n in this.weatherDataDaily" :key="n.time" 
                class="weather-element" :title="n.day + ': ' + n.weather_type"  >
                <p>{{n.weekday}}</p> <p>{{n.temp_min}}° - {{n.temp_max}}°F</p>
                <skycon class="weather-element__skycon"
                  size="24" color="#8be9fd" 
                  :condition="getSkycon(n.weather_type)"
                /> 
              </li>
            </ul>
          </div>
      </div>
  </div>
</template>

<script>
import Skycon from "vue-skycons";
import notifications from '../notifications';

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
      weatherDataHourly: Array,
      weatherDataDaily: Array,
      isFlipped: false,
    }
  },
  computed: {
    getCurrentWeather: function() {
      if(this.weatherDataHourly.length > 2){
        return this.weatherDataHourly[0];
      }
      return {temp: 0, weather_type: 'Weather API Error'}
    },
    getClass() {
      return 'weather-card-container' + ((this.isFlipped) ? ' weather-card-container__flipped' : '' )
    }
  },
  methods: {
    getHourlyWeather: function() {
        let today = new Date().toJSON().slice(0, 10).replaceAll('-', '');
        this.axios.get('http://0.0.0.0:9101/weatherHourly/' + today).then((res) => {
            this.weatherDataHourly = res.data.slice(0,9);
      }).catch(e => {
        console.warn('Error: Could not retrieve weather information from homey API. Are coordinates configured correctly?');
        notifications.notifyWarning('Warning: Could not retrieve hourly weather information');
      });
    },
    getDailyWeather: function() {
        let today = new Date().toJSON().slice(0, 10).replaceAll('-', '');
        this.axios.get('http://0.0.0.0:9101/weatherWeekly').then((res) => {
          if(res.data.length > 2) this.weatherDataDaily = res.data;
      }).catch(e => {
        console.warn('Error: Could not retrieve weather information from homey API. Are coordinates configured correctly?');
        notifications.notifyWarning('Warning: Could not retrieve weekly weather information');
      });
    },
    getSkycon: function(weatherType){
      switch(weatherType){
        case 'Light Snow Showers':
        case 'Light Snow':
        case 'Moderate Snow':
        case 'Heavy Snow':
        case 'Snow Grains':
          return 'snow'
        case 'Overcast':
        case 'Partly Cloudy':
          return 'cloudy'
        case 'Fog':
        case 'Depositing rime fog':
          return 'fog'
        case 'Light Rain':
        case 'Heavy Rain':
        case 'Rain':
        case 'Light Drizzle':
        case 'Moderate Drizzle':
        case 'Heavy Drizzle':
        case 'Light Showers':
        case 'Moderate Showers':
        case 'Heavy Showers':
        case 'Thunderstorm':
          return 'rain'
        case 'Light Freezing Rain':
        case 'Heavy Freezing Rain':
        case 'Light Thunderstorm w/ Hail':
        case 'Heavy Thunderstorm w/ Hail':
          return 'sleet'
      }

      return 'clear-day';    
    },
  },
  beforeMount() {
      this.getHourlyWeather();
      this.getDailyWeather();
  },
}
</script>

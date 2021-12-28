<template>
  <div class="weather-card-container">
      <div class="weather-card-container__side weather-card-container__side--front">
          <skycon class="weather-card-container__background--skycon" v-if="weatherDataHourly.length > 1" 
                :title="getCurrentWeather.weather_type" size=128 color="#44475a" :condition="getSkycon(getCurrentWeather.weather_type)"/>
          <div class="weather-card-container__heading">
            <!-- <skycon class="weather-card-container__heading--skycon" v-if="weatherDataHourly.length > 1" 
                :title="getCurrentWeather.weather_type" size=48 color="#f8f8f2" :condition="getSkycon(getCurrentWeather.weather_type)"/> -->
            <div class="weather-card-container__heading--daily-details">
              <div>{{getCurrentWeather.temp}}°F</div>
              <div>{{getCurrentWeather.weather_type}}</div>
            </div>
            <span class="weather-card-container__heading--title">Weather</span>
          </div>
          <div class="weather-card-container__details">
              <div v-for="w in weatherDataHourly" 
                :key="w.time" class="weatherElement" >
                {{w.time}}<span><skycon :title="w.weather_type" 
                  size="16" color="#F8F8F2" 
                  :condition="getSkycon(w.weather_type)"
                /> {{w.temp}}°F </span>
              </div>
          </div>
      </div>
      <div class="weather-card-container__side weather-card-container__side--back">
          <div class="weather-card-container__weekly-forecast">
            <ul>
              <li v-for="n in this.weatherDataDaily" :key="n.time" class="weatherElement" >{{n.day}}: {{n.temp_min}}°F - {{n.temp_max}}°F ({{n.weather_type}})</li>
            </ul>
          </div>
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
      weatherDataHourly: Array,
      weatherDataDaily: Array,
    }
  },
  computed: {
    getCurrentWeather: function() {
      if(this.weatherDataHourly.length > 2){
        return this.weatherDataHourly[0];
      }
      return {temp: 0, weather_type: 'Weather API Error'}
    }
  },
  methods: {
    getHourlyWeather: function() {
        let today = new Date().toJSON().slice(0, 10).replaceAll('-', '');
        this.axios.get('http://0.0.0.0:9101/weatherHourly/' + today).then((res) => {
            this.weatherDataHourly = res.data.slice(0,9);
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
    getDailyWeather: function() {
        let today = new Date().toJSON().slice(0, 10).replaceAll('-', '');
        this.axios.get('http://0.0.0.0:9101/weatherWeekly').then((res) => {
          if(res.data.length > 2) this.weatherDataDaily = res.data;
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
  },
  beforeMount() {
      this.getHourlyWeather();
      this.getDailyWeather();
  },
}
</script>

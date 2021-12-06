<template>
  <div class="weather-card-container">
    <div v-for="w in weatherData" :key="w.time" class="weatherElement" >{{w.time}}<span>{{w.temp}}F {{w.weather_type}}</span></div>
  </div>
</template>

<script>
export default {
  name: 'WeatherCard',
  props: {
      title: String,
  },
  data () {
    return {
      weatherData: Array,
    }
  },
  methods: {
    getHourlyWeather: function() {
        this.axios.get('http://0.0.0.0:9101/weatherHourly/20211205').then((res) => {
          this.weatherData = res.data
      }).catch(e => {
        console.log('Could not reach homey API');
      });
    },
  },
  beforeMount() {
      this.getHourlyWeather();
  },
}
</script>

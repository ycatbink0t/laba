<template>
    <div class="container">
      <div :key="person" v-for="person in persons">
        <template v-if="person.routes.length > 0">
          <h2>
            {{person.first_name + ' ' +person.last_name}}
          </h2>
          <div class="persona">
            <div :key="route" v-for="route in person.routes" class="route">
              Time departure: {{route.time_departure}}
              <br>
              Time arrive: {{route.time_arrive}}
              <br>
              Transport type: {{route.type}}
              <br>
              Streets: {{route.streets.join(', ')}}
            </div>
          </div>
        </template>
      </div>
    </div>
</template>

<script>import axios from 'axios'
export default {
  name: 'PersonsRoutesView',
  data () {
    return {
      persons: [
        {
          first_name: 'Loading...',
          last_name: ' ',
          routes: [{
          }]
        }
      ]
    }
  },
  created () {
    axios.get('/dms/api?what=person_routes').then(response => {
      console.log(response.data)
      this.persons = response.data
    })
  }
}
</script>

<style scoped>
.route{
  display: inline-block;
  border: solid 1px #6D6D6D;
}
</style>

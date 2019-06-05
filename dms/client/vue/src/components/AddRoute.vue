<template>
    <div class="form">
      <label title="Bus, car, bike etc">Type:
        <input type="text" v-model="request.type">
      </label>
      <label>Time departure:
        <input type="time" v-model="request.time_departure">
      </label>
      <label>Time arrive:
        <input type="time" v-model="request.time_arrive">
      </label>
      <label>Select owner:
        <select v-model="selectedPerson">
          <option :key="person.id" v-for="person in persons">{{person.first_name + ' ' + person.last_name}}</option>
        </select>
      </label>
      <label title="Select street to add to route">Select street:
      <select v-model="selectedStreet">
        <option :key="street.id" v-for="street in streets">{{street.street_name}}</option>
      </select>
      </label>
      <input type="button" @click="pushStreet" value="Add street to route">
      <br>
      <p>
        Streets : {{selectedStreets.reduce((result, value) => result + ', ' + value, '').slice(2)}}
      </p>
      <br>
      <input type="button" @click="submit" value="submit"> <!--SUBMIT IS OVERRODE -->
    </div>
</template>

<script>import axios from 'axios'
export default {
  name: 'AddRoute',
  data () {
    return {
      request: {
        what: 'addroute',
        personId: -1,
        streets: [],
        time_departure: '',
        time_arrive: '',
        type: ''
      },
      selectedPerson: '',
      selectedStreet: '',
      selectedStreets: [],
      streets: [{id: -1, street_name: 'Loading...'}],
      persons: [{id: -1, first_name: 'Loa', last_name: 'ding...'}]
    }
  },
  created () {
    axios.get('/dms/api?what=streets').then(response => { this.streets = response.data })
    axios.get('/dms/api?what=persons').then(response => { this.persons = response.data })
  },
  methods: {
    submit () {
      axios.post('/dms/api/', JSON.stringify(this.request)).then(() => {
        this.$router.go(-1)
        alert('Route added')
      })
    },
    pushStreet () {
      if (!this.request.streets.find(street => street === this.selectedStreetId)) {
        this.selectedStreets.push(this.selectedStreet)
        this.request.streets.push(this.selectedStreetId)
      }
    }
  },
  computed: {
    selectedStreetId () {
      return this.streets.find(street => street.street_name === this.selectedStreet).id
    }
  },
  watch: {
    selectedPerson () {
      this.request.personId = this.persons.find(person => person.first_name + ' ' + person.last_name === this.selectedPerson).id
    }
  }
}
</script>

<style scoped>
.form{
  margin-left: auto;
  margin-right: auto;
  padding: 30px;
  background-color: #f1ebf0;
  border-spacing: 0;
  width: 25%;
  margin-top: 20%;
}
label{
  display: table-row;
  height: 28px;
}
input{
  border: solid 1px #6D6D6D;
}
</style>

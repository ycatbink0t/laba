<template>
  <div id="tables">
    <input id="search" placeholder="Search" @input="searchEdited">
    <div class="tables-links">
      <ul>
        <li :key="link.name" :name="link.name" v-for="link in links" @click="tableChanged('?what=table&name=' + link.name)">
          <a>{{link.name}}</a>
        </li>
      </ul>
    </div>
    <div class="tables">
      <div :key="table" v-for="table in tables">
        <h2>{{table.name}}</h2>
        <table>
          <tbody>
          <tr>
            <th></th>
            <th :key="header" v-for="header in table.headers">{{header}}</th>
          </tr>
          <tr :key="rowIndex" v-for="(row, rowIndex) in table.rows">
            <button  @click="deleteRow({name: table.name, id: row.id, rowIndex})">Delete</button>
            <td :key="headerIndex" v-for="(data, headerIndex) in row.cells">
              <input type="text" :value="data"
                     @change="dataEdited(
                       {newValue: data,
                        id: row.id,
                        headerIndex,
                        name: table.name})">
            </td>
          </tr>
          <template v-if="table.newRows.length > 0">
            <tr :key="rowIndex" v-for="(row, rowIndex) in table.newRows">
              <button @click="deleteNewRow({name: table.name, rowIndex})">Delete</button>
              <td :key="data" v-for="(data, headerIndex) in row">
                <input type="text" :value="data"
                       @change="newDataEdited(
                         {newValue: $event.target.value,
                         headerIndex,
                         rowIndex,
                         name: table.name})">
              </td>
              <button @click="saveNewRow({rowIndex, name: table.name})">Save</button>
            </tr>
          </template>
          <button @click="addNewRow({name: table.name})">Add new row</button>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>import axios from 'axios/index'
import {debounce} from 'lodash'
export default {
  name: 'App',
  data () {
    return {
      currentValue: '',
      links: [{name: 'loading'}],
      search: '',
      message: 'DMS v0.3',
      tables: [{
        name: 'Choose table',
        newRows: []
      /*
      headers: ['one', 'two', 'three'],
      rows: [{cells: ['first', 'second', 'meh'], id: 1},
        {cells: ['bla', 'ble', 'blue'], id: 223}]
    }
    */}]}
  },
  methods: {
    dataEdited: function (message) {
      let currentTable = this.tables.find((a) => { return a.name === message.name })
      let data = {
        what: 'update',
        name: message.name,
        id: message.id,
        header: currentTable.headers[message.headerIndex],
        value: message.newValue}
      axios.post('/dms/api/', JSON.stringify(data))
        .then((response) => {
          if (response.status === 220) {
            return 0
          } else {
            currentTable.rows.find(a => { return a.id === message.id }).cells[message.headerIndex] = message.newValue
          }
        })
    },
    tableChanged: function (link) {
      axios.get('/dms/api' + link).then((response) => {
        let table = response.data
        if (!table.hasOwnProperty('rows')) table.rows = []
        table.newRows = []
        this.tables = [table]
      })
    },
    addNewRow: function (message) {
      let currentTable = this.tables.find((a) => { return a.name === message.name })
      let emptyRow = []
      for (let i = 0; i < currentTable.headers.length; i++) {
        emptyRow.push('Fill this cell')
      }
      currentTable.newRows.push(emptyRow)
    },
    newDataEdited: function (message) {
      let currentTable = this.tables.find((a) => { return a.name === message.name })
      currentTable.newRows[message.rowIndex][message.headerIndex] = message.newValue
    },
    saveNewRow: function (message) {
      let currentTable = this.tables.find((a) => { return a.name === message.name })
      let data = {
        what: 'insert',
        name: message.name,
        headers: currentTable.headers,
        values: currentTable.newRows[message.rowIndex]
      }
      axios.post('/dms/api/', JSON.stringify(data)).then((response) => {
        if (response.status === 221) {
          alert(response.data)
          return 0
        }
        let id = response.data
        let cells = currentTable.newRows.splice(message.rowIndex, 1)[0]
        currentTable.rows.push({id, cells})
      })
    },
    deleteRow: function (message) {
      if (!confirm()) return 0
      let currentTable = this.tables.find((a) => { return a.name === message.name })
      axios.post('/dms/api/', JSON.stringify({what: 'delete', id: message.id, name: message.name}))
        .then((response) => {
          currentTable.rows.splice(message.rowIndex, 1)
        })
    },
    deleteNewRow: function (message) {
      if (!confirm()) return 0
      let currentTable = this.tables.find((a) => { return a.name === message.name })
      currentTable.newRows.splice(message.rowIndex, 1)
    },
    searchUpdate: function (value) {
      console.log(this.search)
      axios.get('/dms/api?what=search&value=' + this.search).then((response) => {
        console.log(response.data)
        let tables = response.data
        tables.forEach(table => { table.newRows = [] })
        this.tables = tables
      })
    },
    searchEdited: function (val) {
      console.log('search watcher')
      this.search = event.target.value
      this.tables = [{name: 'Loading...', newRows: []}]
      this.debouncedGetAnswer()
    }
  },
  created: function () {
    axios.get('/dms/api?what=links').then((response) => {
      this.links = response.data
    })
    this.debouncedGetAnswer = debounce(this.searchUpdate, 1000)
  }
}
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  #tables{
    margin-top: 40px;
  }
  table{
    padding-top: 10px;
    margin-left: auto;
    margin-right: auto;
    background-color: #F1EBF0;
    border-spacing: 0;
  }
  .data{
    background-color: #F1EBF0;
    color: #6D6D6D;
  }
  td{
    border: 1px solid #AAABBC;
    border-spacing: 0;
    background: #F1EBF0 !important;
  }
  td:hover{
    padding: 0;
  }
  input{
    outline: none;
    background: #F1EBF0 !important;
    border: none;
    text-align: center;
  }
  input:hover{
    background: #AAABBC !important;
    padding: 0;
  }
  li{
    display: inline;
  }
  li:hover{
    cursor: pointer;
  }
  ul{
    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  a{
    padding: 10px;
    background-color: #AAABBC;
  }
  h2{
    padding: 10px;
    background-color: #C1C1C1;
  }
  #search{
    float:right;
  }
</style>

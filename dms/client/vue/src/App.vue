<template>
  <div id="app">
    <nav>
      <router-link to="/tables">Edit database Tables</router-link>
      <router-link to="/adduser">Add user</router-link>
      <router-link to="/addstreet">Add street</router-link>
      <router-link to="/addroute">Add route</router-link>
      <router-link to="/personroutes">Persons routes</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>

</style>

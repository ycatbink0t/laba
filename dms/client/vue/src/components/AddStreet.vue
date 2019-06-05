<template>
  <div class="form">
    <form action="/dms/addstreetform/" method="post">
      <label>Street name:
        <input type="text" name="street_name">
      </label>
      <input type="submit" value="Submit">
    </form>
  </div>
</template>

<script>export default {
  name: 'AddStreet'
}
</script>

<style scoped>
.form{
  margin-left: auto;
  margin-right: auto;
  padding: 30px;
  background-color: #f1ebf0;
  border-spacing: 0;
  width: 20%;
  margin-top: 25%;
}
label{
  display: table-row;
  height: 28px;
}
input{
  border: solid 1px #6D6D6D;
}
</style>

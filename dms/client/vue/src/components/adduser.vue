<template>
  <div class="form">
  <form action="/dms/adduserform/" method="post">
    <label>First name:
      <input type="text" name="first_name">
    </label>
    <label>Last name:
      <input type="text" name="last_name">
    </label>
    <label>Date of birth:
      <input type="date" name="date_of_birth">
    </label>
    <input type="submit" value="Submit">
  </form>
</div>
</template>

<script>export default {
  name: 'adduser'
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

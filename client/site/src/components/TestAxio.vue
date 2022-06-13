<template>
  <div class="content"></div>
</template>

<script>
import axios from "axios";

export default {
    name: 'TestAxio',
    created() {
    axios.get("https://jsonplaceholder.typicode.com/todos/1").then((result) => {
      console.log(result.data);
    })
  }
};
</script>

<style scoped lang="scss">
</style>
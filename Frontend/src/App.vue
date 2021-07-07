<template>
  <div id="app">
    <Header></Header>
    <div class="container">
      <div class="row">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
  import Header from "./components/Header/Header"
  export default {
    components:{
      Header
    }
  };
</script>

<style></style>

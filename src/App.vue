<script setup>
import Footer from './components/Footer.vue';
import Header from './components/Header.vue';
import MP3Content from './components/MP3Content.vue';
</script>

<template>
  <Header></Header>
  <MP3Content></MP3Content>
  <Footer></Footer>
</template>


<style scoped>
.content {
  padding-top: 8rem; /* espacio para el navbar fijo */

  text-align: center;
  color: #333;
  
}
</style>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import GenPlaylists from './components/GenPlaylists.vue'
import router from './router/index'

const songData = ref({})

const getSong = (s) => {
  songData.value = s
  router.push({ name: 'genplaylists'})
}
</script>

<template>
<header>
  <RouterLink to="/" id="banner">
    <img alt="logo" class="logo" src="@/assets/icon.svg" width="128" height="128" />
    <h1>matsubara</h1>
  </RouterLink>
    <nav>
      <RouterLink to="/about">About</RouterLink>
      <!-- <RouterLink to="/genplaylists">Generate Playlists</RouterLink> -->
    </nav>
</header>
<main>
  <RouterView :songData="songData" @set="(song) => getSong(song)"/>
    <!-- <RouterView /> -->
</main>
<footer>Alexander Stradnic {{ new Date().getFullYear() }}</footer>
</template>

<style scoped>
#banner {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  text-decoration: none;
  color: white;
}
header {
  text-align: center;
}
h1 {
  font-weight: 1000;
  font-family: 'Courier New', Courier, monospace;
}
nav {
  display: flex;
  justify-content: center;
  align-items: baseline;
}
nav > *{
  padding: 2em 2em;
}
main {
  display: block;
  width: 60%;
  margin: 0 auto;
  min-height: max-content;
}
footer {
  background-color: rgba(0,0,0,0.4);
  color: white;
  text-align: center;
  padding: 0.5em 0;
}
</style>
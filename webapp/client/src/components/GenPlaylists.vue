<script setup>
import axios from 'axios'
import { reactive, defineProps } from 'vue'

let random = true
let sim = true
let casebased = true
let casebased_k = 20
let length = 10

const props = defineProps({
  songData: {
    type: Object
  }
})

const state = reactive({
  lists: []
})

async function generate(){
  document.getElementById("spinner").style.display = "block";
  let res = await axios.get(`https://music.nimitzpro.tk/generate${"?seed="+props.songData.Track_uri+"&length="+length}${random ? "&random="+random : ""}${sim ? "&sim="+sim : ""}${casebased ? "&casebased="+casebased : ""}${casebased ? "&casebased_k="+casebased_k : ""}`, {timeout:300000})
  state.lists = res.data.lists
  document.getElementById("spinner").style.display = "none";
}

</script>

<template>
    Song: {{ props.songData.Track_name }}
    <br>
    Artist: {{ props.songData.Artist_name }}

    <form v-on:submit.prevent="generate" class="form">
      Enable Random:<input type="checkbox" v-model="random" checked />
      Enable Similarity:<input type="checkbox" v-model="sim" checked />
      Enable Case-based:<input type="checkbox" v-model="casebased" checked />
      Case-based K amount of input playlists: <input v-model="casebased_k" :value="casebased_k" checked />
      
      Length of playlists: <input v-model="length" :value="length" />
      <button @click="generate">Generate Playlists</button>
    </form>
    <img src="../assets/spinner.gif" id="spinner" />
    {{ state.lists }}
</template>

<style>
#spinner {
  display: none;
}
</style>
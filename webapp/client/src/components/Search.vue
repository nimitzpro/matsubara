<script setup>
import axios from 'axios'
import { reactive } from 'vue'

let title = ""
let artist = ""

const state = reactive({
  songs: []
})

function search(){
    if(artist || title) {
    axios.get(`https://music.nimitzpro.tk/search${artist ? "?artist="+artist : ""}${title && artist ? "&title="+title : title ? "?title="+title : ""}`).then((res) => {
        console.log(res.data)
        state.songs = res.data
    })
    }
}

</script>

<template>
<header>
    <h1>Search for a seed song and press enter!</h1>
    <form v-on:submit.prevent="search" class="form">
        <input v-model="title" placeholder="Song Title"/><br>
        <input v-model="artist" placeholder="Artist"/><br>
        <button @click="search()">Search</button>
    </form>
</header>
    <ul>
        <li v-for="song in state.songs" :key="song.Track_uri" @click="$emit('set', song)">
            {{ song.Track_name }} - {{ song.Artist_name }}
        </li>
    </ul>
</template>

<style>
::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: gray;
  opacity: 0.8; /* Firefox */
}
::-ms-input-placeholder { /* Microsoft Edge */
  color: gray;
  opacity: 0.8;
}

form {
    margin-top: 2em;
    width: 100%;
    display: flex;
    justify-content: space-around;
    /* align-items: center; */
}

input, button {
    font-size: 2em;
    background-color: rgba(0,0,0,0.4);
}
input{
  padding: 0.5em 1em;
  border: none;
  box-sizing: border-box;
  border-radius: 0.25em 0.25em;
  color: white;
}
button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 0 0;
  display: none;
}
</style>
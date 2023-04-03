<template>
  <main>
    {{ this.song }}
  </main>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
export default {
  setup(props) {
    const song = ref([])
  },
  data() {
    return {
    }
  },
  methods: {
    increment() {
      this.count++
    }
  },
  mounted() {
    axios.get("http://localhost:4000/sql").then((res) => {
      this.song.value = JSON.stringify(res.body)
    })
  }
}
</script>
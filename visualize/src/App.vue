<template>
  <div id="app">
    <Homunculus msg="Literary Homunculus" id="homunculus"/>
    <Slide/>
    <ul>
      <li v-for="book in books" v-bind:key="book.idx">
        {{ book.name }} 
      </li>
    </ul>
  </div>
</template>

<script>
  import Homunculus from './components/Homunculus.vue';
  import Slide from './components/Slider.vue';
  import { db } from './firebaseConfig';

  export default {
    name: 'app',
    data() {
      return {
        books: []
      }
    },
    firestore() {
      return {
        books: db.collection('books'),
      }
    },
    components: {
      Homunculus,
      Slide
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 2px;
  }
  #homunculus {
    height: 90%;
    vertical-align: top;
  }
</style>

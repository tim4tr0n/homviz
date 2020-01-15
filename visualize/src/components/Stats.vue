<template>
  <div class="slidecontainer">
    <h1>Homunculus Info</h1>
    <input type="range" min="1" max="100" value="1" class="slider" id="slide">
    <ul>
        <li v-for="book in books" v-bind:key="book.idx">
        {{ book.name }} 
        </li>
    </ul>
  </div>
</template>

<script>
  import { db } from '../firebaseConfig';
  export default{
    name: 'Stats',
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
  }
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .slidecontainer {
        width: 20vmax;
        height: 35vmax;
        background: #cccccc;
    }
</style>
<template>
  <div v-if="stats.viewByYearMode" class="slidecontainer">
    <input @input="changeSlider" min="0" v-bind:max="stats.max" id="slider" type="range"/>
  </div>
</template>

<script>

export default {
  data () {
    return {
      sliderKey: 0,
      sliderValue: null,
      queriedBooks: this.$store.getters.queriedBooks,
      selectedBook: this.$store.getters.selectedBook,
      selectedBookIndex: this.$store.getters.selectedBookIndex,
      viewByYearMode: this.$store.getters.viewByYearMode,
      slider: {
          startMin: 25,
          startMax: 75,
          min: 0,
          max: 100,
          start: 40,
          step: 1
      }
    }
  },
  computed: {
    stats() {
        return {
          queriedBooks: this.$store.getters.queriedBooks,
          selectedBook: this.$store.getters.selectedBook,
          viewByYearMode: this.$store.getters.viewByYearMode,
          max: this.$store.getters.queriedBooks.length - 1,
        }
    }
  },
  methods:{
    changeSlider(e){
      console.log("slider changed", e.target.valueAsNumber)
      const index = e.target.valueAsNumber
      const book = this.stats.queriedBooks[index]
      this.$store.dispatch('changeSelectedBookAndBodyState', { book, index } )
    },
    rerenderSlider(){
      this.sliderKey += 1
    }
  },
  mounted: function() {

    // this.createSlider()
    // this.$store.subscribe((mutation) => {
    //   if( mutation.type == "changeSelectedSubgenre" || (mutation.type == "changeSelectedLanguage")){
    //     // this.rerenderSlider()
    //     // this.createSlider()
        
    //   }
    // })    

  
    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #slider {
    bottom: -10px;
    width: 90%;
    left: 5%;
  }
  .slidecontainer {
    width: 100%;
    /* boxShadow: '0 2pt 8pt rgba(0, 0, 0, 0.5)'' */
  }

</style>
<template>
  <div class="slidecontainer">
    <hsc-window-style-metal>
        <hsc-window title="hom info" >
            <fieldset>
                <legend>View by Year</legend>
                <input type="radio" name="viewByYear" value=true @change="($event) => { selectViewByYearMode($event) }"> True
                <input type="radio" name="viewByYear" checked value=false @change="($event) => { selectViewByYearMode($event) }"> False
            </fieldset>
            <fieldset>
                <legend>Genre</legend>
                <select @input="updateGenre">
                    <option value="none" selected>Choose a genre</Option>
                    <option v-for="(value, key) in selectorData.genres"  v-bind:key="key" v-bind:value="key">{{value}}</option>
                </select>
            </fieldset>
            <fieldset>
                <legend>Subgenre</legend>
                <select @input="updateSubgenre">
                    <option value="none" selected>All</Option>
                    <option v-for="(value, key) in selectorData.subgenres"  v-bind:key="key" v-bind:value="key">{{value}}</option>
                </select>
            </fieldset>
            <fieldset>
                <legend>Language</legend>
                <select @input="updateLanguage">
                    <option value="none" selected>Choose a language</Option>
                    <option v-for="(value, key) in selectorData.languages"  v-bind:key="key" v-bind:value="key">{{value}}</option>
                </select>
            </fieldset>
            <fieldset>
                <legend>query limit</legend>
                <input type="number" :max=200 />
            </fieldset>
        </hsc-window>
    </hsc-window-style-metal>
  </div>
</template>

<script>
import Vue from 'vue'
import * as VueWindow from '@hscmap/vue-window'

Vue.use(VueWindow)

export default {
    name: 'Stats',
    data() {
        return {
            sliderValue: null,
            books: [],
            sliderPosition: this.$store.getters.sliderPosition,
            genres: this.$store.getters.genres,
            subgenres: this.$store.getters.subgenres,
            languages: this.$store.getters.languages,
            selectedGenre: this.$store.getters.selectedGenre,
            selectedSubgenre: this.$store.getters.selectedSubgenre,
            selectedLanguage: this.$store.getters.selectedLanguage,
            playingMusic: false
        }
    },
    methods: {
        selectViewByYearMode(e){
            
            console.log("selection event", e.target.value)
            this.playMusic()
            if ( e.target.value == "true" ){
                var newValue = true
            } else {
                newValue = false
            }
            this.$store.commit("changeViewByYearMode", newValue)
            if (e.target.value == "true"){
                console.log("we re gonna query that shit")
                this.$store.dispatch('queryBooks')
            }
        },
        playMusic(){
            if (!this.playingMusic){
                var audio = new Audio('https://drive.google.com/uc?export=download&id=1I-Hic4KpHB5GDvXxOhuHnyK0t4NK2U8K')
                audio.play()
                this.playingMusic = true
                audio.onended = () => {
                    audio.play()
                }
            }
        },
        updateGenre(e) {
            this.$store.commit("changeSelectedGenre", e.srcElement.value)
        },
        updateSubgenre(e) {
            this.$store.commit("changeSelectedSubgenre", e.srcElement.value)
        },
        updateLanguage(e) {
            this.$store.commit("changeSelectedLanguage", e.srcElement.value)
        }
    },
    computed: {
        // TODO : fix these awful naming conventions. will inevitably come when sliderPosition is mapped to homunculus body parts
        selectorData() {
            return {
                sliderPosition: this.$store.getters.sliderPosition,
                genres: this.$store.getters.genres,
                subgenres: this.$store.getters.subgenres,
                languages: this.$store.getters.languages,
                selectedLanguage: this.$store.getters.selectedLanguage,
                homunculusState: this.$store.getters.homunculusState
            }
        },
   
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    select {
        width: 100%
    }
</style>
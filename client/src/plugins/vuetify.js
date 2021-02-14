import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify)

export default new Vuetify({
  icons: {
    iconfont: 'mdi'
  },
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
      light: {
        primary: "#1B1D27",
        variant: "#3C3D49",
        gray: "#B7B7C6",
        secondary: "#719DE0",
        tertiary: "#4F86D9",
        background: "#F7F7F7",
        surface: "#FCFCFC",
        error: "#EC7965"
      }
    }
  }
})
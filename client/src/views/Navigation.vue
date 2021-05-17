<template>
  <div id="app">
    <v-app>
      <v-content>
        <transition mode="out-in">
          <v-container
            fluid
            fill-height
            style="
              padding: 0px;
              margin: 0px;
              background-color: var(--v-background-base);
            "
          >
            <shared-menu />
            <router-view v-on:message="popup" />
            <shared-github />
            <shared-copyright />
            <v-snackbar
              v-model="snackbar"
              :color="color"
              :timeout="3000"
              bottom
            >
              {{ message }}
              <template v-slot:action="{ attrs }">
                <v-btn dark text v-bind="attrs" @click="snackbar = false">
                  Close
                </v-btn>
              </template>
            </v-snackbar>
          </v-container>
        </transition>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import SharedMenu from '@/components/shared/menu.vue';
import SharedGithub from '@/components/shared/github.vue';
import SharedCopyright from '@/components/shared/copyright.vue';

export default {
  components: {
    SharedMenu,
    SharedGithub,
    SharedCopyright,
  },
  data() {
    return {
      snackbar: false,
      message: null,
      color: null,
    };
  },
  methods: {
    popup(message) {
      this.snackbar = true;
      this.message = message.text;
      this.color = message.color;
    },
    redirect() {
      window.location.href = process.env.VUE_APP_WEBSITE_BASE_URL;
    },
  },
};
</script>

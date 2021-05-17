<template>
  <div>
    <v-card class="card">
      <v-row
        no-gutters
        style="
          display: flex;
          height: 100%;
          justify-content: center;
          align-items: center;
        "
      >
        <a
          href="https://www.linkedin.com/company/calaster"
          target="_blank"
          style="
            display: flex;
            text-decoration: none;
            margin: 0 6px;
          "
        >
          <v-icon small color="tertiary">
            mdi-linkedin
          </v-icon>
        </a>
        <a
          href="https://www.facebook.com/calastertech"
          target="_blank"
          style="
            display: flex;
            text-decoration: none;
            margin: 0 6px;
          "
        >
          <v-icon small color="tertiary">
            mdi-facebook
          </v-icon>
        </a>
        <a
          href="https://twitter.com/CalAster911"
          target="_blank"
          style="
            display: flex;
            text-decoration: none;
            margin: 0 6px;
          "
        >
          <v-icon small color="tertiary">
            mdi-bird
          </v-icon>
        </a>
        <v-btn icon small style="margin: 0;" @click="modal = true">
          <v-icon small color="tertiary">
            mdi-google-analytics
          </v-icon>
        </v-btn>
      </v-row>
    </v-card>
    <performances :modal="modal" v-on:modal="modal = $event" />
  </div>
</template>

<style type="scss" scoped>
.card {
  height: 32px;
  min-width: 140px;
  padding: 0 12px;
  background-color: var(--v-surface-base) !important;
  border-radius: 4px !important;
  border: solid 1px #e5e9ed !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  position: absolute;
  bottom: 10px;
  left: calc(50% - 70px);
}
</style>

<script>
import Performances from '@/components/shared/performances/main.vue';

export default {
  components: {
    Performances,
  },
  data() {
    return {
      modal: false,
    };
  },
};
</script>

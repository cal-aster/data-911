<template>
  <v-dialog v-model="active" :fullscreen="$vuetify.breakpoint.xs" width="600px">
    <v-card
      v-if="active"
      :color="$vuetify.breakpoint.xs ? 'surface' : 'background'"
      height="fit-content"
      style="margin: 0; padding: 0;"
      v-bind:style="{
        borderRadius: $vuetify.breakpoint.xs ? '0' : '4px',
      }"
    >
      <v-row
        no-gutters
        style="background-color: var(--v-tertiary-base) !important;"
        v-bind:style="{
          padding: $vuetify.breakpoint.xs
            ? '12px 20px 12px 30px'
            : '12px 30px 12px 40px',
        }"
      >
        <span
          class="body surface--text"
          style="
            font-weight: bold;
            font-size: 20px;
            align-self: center;
          "
        >
          Performances
        </span>
        <v-spacer />
        <v-btn icon @click="active = false">
          <v-icon color="surface">mdi-close</v-icon>
        </v-btn>
      </v-row>
      <perfect-scrollbar
        v-bind:style="{
          padding: $vuetify.breakpoint.xs ? '0' : '20px 30px',
          maxHeight: $vuetify.breakpoint.xs
            ? 'calc(100vh - 90px)'
            : 'calc(90vh - 60px)',
        }"
      >
        <statistic
          v-if="stats"
          :title="'Over the last 24 hours'"
          :min="stats.min_t1d"
          :avg="stats.avg_t1d"
          :max="stats.top_t1d"
          v-bind:style="{
            marginBottom: $vuetify.breakpoint.xs ? '0' : '12px',
          }"
        />
        <statistic
          v-if="stats"
          :title="'Over the last 7 days'"
          :min="stats.min_t7d"
          :avg="stats.avg_t7d"
          :max="stats.top_t7d"
          v-bind:style="{
            marginBottom: $vuetify.breakpoint.xs ? '0' : '12px',
          }"
        />
        <statistic
          v-if="stats"
          :title="'Over the last 28 days'"
          :min="stats.min_t28"
          :avg="stats.avg_t28"
          :max="stats.top_t28"
        />
      </perfect-scrollbar>
    </v-card>
  </v-dialog>
</template>

<script>
import Statistic from './statistic.vue';

export default {
  components: {
    Statistic,
  },
  props: {
    modal: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      stats: null,
      active: this.modal,
    };
  },
  watch: {
    active() {
      this.$emit('modal', this.active);
      if (this.active) {
        this.$http.get('/performances').then((response) => {
          this.stats = response.data;
        });
      }
    },
    modal() {
      this.active = this.modal;
    },
  },
};
</script>

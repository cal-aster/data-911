<template>
  <v-card class="card">
    <v-card-title
      style="
        background-color: var(--v-background-base);
        padding: 10px 16px 10px 24px;
      "
    >
      <span
        class="body primary--text"
        style="font-weight: bold; font-size: 18px;"
      >
        {{
          $vuetify.breakpoint.xs
            ? 'Daily over 3 months'
            : 'Daily number of calls over 3 months'
        }}
      </span>
      <v-spacer />
      <v-menu
        ref="menu"
        v-model="menu"
        :close-on-content-click="false"
        transition="scale-transition"
        max-width="450px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-row
            no-gutters
            v-bind="attrs"
            v-on="on"
            style="
              max-width: fit-content;
              display: flex;
              padding: 6px 0;
            "
          >
            <span
              class="subtitle-3"
              style="
                display: flex;
                color: rgb(0, 0, 0, 0.33);
                font-size: 14px;
                font-weight: bold;
                margin-right: 12px;
                align-items: center;
              "
            >
              {{ date }}
            </span>
            <v-icon color="rgb(0, 0, 0, 0.33)">
              mdi-calendar
            </v-icon>
          </v-row>
        </template>
        <v-date-picker
          v-model="date"
          :min="city.min_date"
          :max="city.max_date"
          full-width
          no-title
          scrollable
        />
      </v-menu>
    </v-card-title>
    <v-card-text
      style="
        padding: 10px 10px 0 10px;
        margin: 0;
        display: flex;
        height: 100px;
        max-height: 100px;
        align-items: center;
        place-content: center;
        background-color: var(--v-surface-base);
      "
    >
      <time-serie
        v-if="data"
        :data="data"
        style="
          height: 100% !important;
          max-height: 100px !important;
          width: 100% !important;
        "
        v-bind:style="{
          margin: $vuetify.breakpoint.xs ? '0 0 -8px -8px' : '0',
        }"
      />
      <hollow-dots-spinner
        v-else
        :animation-duration="1000"
        :dot-size="8"
        :dots-num="6"
        color="#719DE0"
      />
    </v-card-text>
  </v-card>
</template>

<style type="scss" scoped>
.card {
  width: 100%;
  min-height: 160px;
  background-color: var(--v-surface-base) !important;
  border-radius: 4px !important;
  border: solid 1px #e5e9ed !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
}
</style>

<script>
import { HollowDotsSpinner } from 'epic-spinners';
import TimeSerie from '@/components/shared/timeserie.vue';

export default {
  components: {
    TimeSerie,
    HollowDotsSpinner,
  },
  props: {
    city: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      data: null,
      menu: false,
      date: null,
    };
  },
  created() {
    this.date = this.city.max_date;
  },
  watch: {
    date() {
      this.menu = false;
      this.load(this.date);
    },
  },
  methods: {
    load(date) {
      this.data = null;
      this.$http
        .get(`/temporal/daily/${this.city.id}?last=${date}`)
        .then((response) => {
          this.data = response.data;
        });
    },
  },
};
</script>

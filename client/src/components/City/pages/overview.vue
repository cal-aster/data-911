<template>
  <perfect-scrollbar
    style="
      height: calc(100vh - 190px);
      max-height: calc(100vh - 190px);
      padding: 0;
    "
  >
    <v-row
      no-gutters
      style="
        height: calc(100vh - 190px);
        max-height: calc(100vh - 190px);
        display: block;
      "
    >
      <v-row no-gutters>
        <v-col
          cols="12"
          sm="4"
          v-for="(stat, index) in stats"
          :key="index"
          v-bind:style="{
            padding: $vuetify.breakpoint.xs
              ? '0'
              : index == 1
              ? '0px 4px'
              : index == 0
              ? '0px 8px 0px 0px'
              : index == 2
              ? '0px 0px 0px 8px'
              : '0',
            marginTop: $vuetify.breakpoint.xs ? (index > 0 ? '6px' : '0') : '0'
          }"
        >
          <city-pages-card :title="stat.label" :value="stat.value" />
        </v-col>
      </v-row>
      <city-pages-hourly
        v-if="timedHourly"
        :city="city"
        style="margin: 12px 0;"
      />
      <city-pages-daily
        v-if="timedDaily"
        :city="city"
        style="margin: 12px 0;"
      />
      <city-pages-weekly
        v-if="timedWeekly"
        :city="city"
        style="margin: 12px 0;"
      />
    </v-row>
  </perfect-scrollbar>
</template>

<script>
export default {
  props: {
    city: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      series: null,
      timedHourly: false,
      timedDaily: false,
      timedWeekly: false
    };
  },
  mounted() {
    setTimeout(() => {
      this.timedWeekly = true;
    }, 50);
    setTimeout(() => {
      this.timedDaily = true;
    }, 50);
    setTimeout(() => {
      this.timedHourly = true;
    }, 50);
  },
  computed: {
    stats() {
      return [
        {
          label: "Population",
          value: this.city.population
            ? this.$vuetify.breakpoint.xs
              ? this.city.population.toLocaleString()
              : this.city.population.toLocaleString() + " inhabitants"
            : "---"
        },
        {
          label: "Earliest data",
          value: this.city.min_date
        },
        {
          label: "Latest data",
          value: this.city.max_date
        }
      ];
    }
  }
};
</script>

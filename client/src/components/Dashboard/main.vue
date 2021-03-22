<template>
  <div
    style="
      padding: 0;
      margin: 0;
      width: 100%;
      height: 100%;
      display: flex;
    "
  >
    <dashboard-header :cities="cities" />
    <dashboard-socials :cities="cities" />
    <shared-search
      placeholder="Looking for a city?"
      v-on:search="search = $event"
      style="
        position: absolute;
        top: 10px;
      "
      v-bind:style="{
        right: $vuetify.breakpoint.smAndDown ? '10px' : '30px'
      }"
    />
    <v-row
      no-gutters
      v-bind:style="{
        padding: $vuetify.breakpoint.smAndDown ? '0' : '0 14px'
      }"
    >
      <perfect-scrollbar
        style="
          margin: 80px 0px 56px 0px;
          width: 100%;
          height: calc(100vh - 142px);
          max-height: calc(100vh - 142px);
        "
      >
        <v-row no-gutters>
          <v-col
            cols="12"
            sm="6"
            md="4"
            lg="3"
            xl="2"
            v-for="city in fCities"
            :key="city.id"
            style="
              max-height: 232px;
            "
            v-bind:style="{
              padding: $vuetify.breakpoint.smAndDown
                ? '0 10px 20px 10px'
                : '0px 16px 32px 16px'
            }"
          >
            <dashboard-city :city="city" />
          </v-col>
        </v-row>
      </perfect-scrollbar>
    </v-row>
  </div>
</template>

<script>
export default {
  metaInfo: {
    title: "Data911 - Dashboard",
    htmlAttrs: {
      lang: "en"
    }
  },
  data() {
    return {
      search: "",
      cities: this.$store.state.cities
    };
  },
  computed: {
    nCalls() {
      var count = 0;
      this.cities.forEach(x => {
        count += x.num_calls;
      });
      return count;
    },
    fCities() {
      return this.cities.filter(x => {
        return x.city.toLowerCase().includes(this.search.toLowerCase());
      });
    }
  },
  methods: {
    days(start, end) {
      var d_0 = new Date(start);
      var d_1 = new Date(end);
      return (d_1.getTime() - d_0.getTime()) / (1000 * 3600 * 24);
    },
    update() {
      this.cities.forEach(x => {
        if (!this.minDate) {
          this.minDate = x.min_date;
        } else if (x.min_date < this.minDate) {
          this.minDate = x.min_date;
        }
        if (!this.maxDate) {
          this.maxDate = x.max_date;
        } else if (x.max_date > this.maxDate) {
          this.maxDate = x.max_date;
        }
      });
      this.numDays = this.days(this.minDate, this.maxDate);
    }
  }
};
</script>

<template>
  <v-card class="component">
    <v-menu
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      transition="scale-transition"
      max-width="450px"
      min-width="450px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-row v-bind="attrs" v-on="on" no-gutters>
          <span
            class="subtitle-3"
            style="
              color: rgb(0, 0, 0, 0.33);
              font-size: 14px;
              font-weight: bold;
              align-self: center;
              margin-right: 12px;
            "
          >
            {{ dates.length == 0 ? "Pick some dates" : tDates }}
          </span>
          <v-icon color="rgb(0, 0, 0, 0.33)">
            mdi-calendar
          </v-icon>
        </v-row>
      </template>
      <v-date-picker
        v-model="dates"
        :min="city.min_date"
        :max="city.max_date"
        range
        full-width
        no-title
        scrollable
      />
    </v-menu>
  </v-card>
</template>

<style type="scss" scoped>
.component {
  height: 32px;
  min-width: fit-content;
  padding: 0 8px 0 16px;
  background-color: var(--v-surface-base) !important;
  border-radius: 4px !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  position: absolute;
  display: flex;
  top: 10px;
  right: 30px;
  z-index: 5;
  align-items: center;
}
@media only screen and (max-width: 1264px) {
  .component {
    display: none;
  }
}
</style>

<script>
import _ from "lodash";

export default {
  props: {
    city: {
      type: Object,
      default: () => {}
    },
    dates: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      menu: null
    };
  },
  watch: {
    menu() {
      if (!this.menu) {
        if (this.dates.length == 0) {
          this.$emit("dates", [this.city.max_date]);
        } else {
          this.$emit("dates", this.dates);
        }
      } else {
        if (this.dates.length == 0) {
          this.dates = [this.city.max_date];
        }
      }
    }
  },
  computed: {
    fDates() {
      var sDates = _.cloneDeep(this.dates);
      sDates.sort();
      return sDates.join(" to ");
    },
    tDates() {
      var dates = _.cloneDeep(this.dates);
      dates.sort();
      return `${dates[0]} ~ ${dates[1] ? dates[1] : dates[0]}`;
    }
  }
};
</script>

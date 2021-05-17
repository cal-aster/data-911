<template>
  <div
    style="
      padding: 0;
      margin: 0;
      width: 100%;
      height: 100%;
    "
  >
    <v-overlay v-model="overlay" absolute :opacity="0.9" class="overlay">
      <atom-spinner
        v-if="loading"
        :animation-duration="1000"
        :size="60"
        color="#EC7965"
      />
      <v-card v-else elevation="0" class="card">
        <v-row no-gutters style="margin-bottom: 40px;">
          <span>
            To avoid any server overload, we limit our visualization feature to
            a period of 7 days.
            <br /><br />
            We agree, lazy developers ...
          </span>
        </v-row>
        <v-row no-gutters>
          <looping-rhombuses-spinner
            :animation-duration="2500"
            :rhombus-size="18"
            color="#EC7965"
            style="margin: 0 auto;"
          />
        </v-row>
      </v-card>
    </v-overlay>
    <v-overlay
      v-if="!city.localized"
      absolute
      :opacity="0.33"
      class="overlay"
    />
    <cluster-toggle v-if="city.localized" v-on:toggle="type = $event" />
    <dates-selection
      v-if="isCityReady && city.localized"
      :city="city"
      :dates="dates"
      v-on:dates="dates = $event"
    />
    <records-count v-if="city.localized" :data="data" :records="records" />
    <mapbox-map
      style="height: 100%;"
      :access-token="token"
      :map-style="style"
      :center="center"
      :zoom="zoom"
      @mb-created="map = $event"
    >
      <mapbox-cluster
        v-if="type == 'clusters'"
        :data="data"
        :clusterCountPaint="{
          'text-color': 'black',
        }"
        :unclusteredPointPaint="{
          'circle-color': 'yellow',
        }"
        :clustersPaint="{
          'circle-color': 'rgba(238, 162, 50, 0.5)',
          'circle-radius': 20,
        }"
      />
    </mapbox-map>
  </div>
</template>

<style>
.mapboxgl-ctrl-bottom-right {
  display: none !important;
}
.mapboxgl-ctrl-bottom-left {
  bottom: 8px !important;
  left: 50% !important;
  width: 100px !important;
}
</style>

<style type="scss" scoped>
.card {
  width: 25vw;
  padding: 0 16px;
  background-color: transparent !important;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
}
.overlay {
  position: absolute;
  width: 66.6vw;
  top: 0;
  right: 0;
  left: 33.3vw;
  z-index: 1;
}
@media only screen and (max-width: 1904px) {
  .overlay {
    width: 50vw;
    left: 50vw;
  }
}
@media only screen and (max-width: 1264px) {
  .overlay {
    display: none;
  }
}
</style>

<script>
import Vue from 'vue';
import 'mapbox-gl/dist/mapbox-gl.css';
import VueMapbox from '@studiometa/vue-mapbox-gl';
Vue.use(VueMapbox);

import cloneDeep from 'lodash/cloneDeep';
import isEmpty from 'lodash/isEmpty';
import { AtomSpinner, LoopingRhombusesSpinner } from 'epic-spinners';
import ClusterToggle from './toggle.vue';
import DatesSelection from './dates.vue';
import RecordsCount from './records.vue';

export default {
  components: {
    ClusterToggle,
    DatesSelection,
    RecordsCount,
    AtomSpinner,
    LoopingRhombusesSpinner,
  },
  props: {
    city: {
      type: Object,
      default: () => {},
    },
    center: {
      type: Array,
      default: () => [0.0, 0.0],
    },
    zoom: {
      type: Number,
      default: 1,
    },
  },
  data() {
    return {
      map: null,
      dates: [],
      type: 'heatmap',
      loading: false,
      blocking: false,
      data: null,
      records: 0,
      token: process.env.VUE_APP_MAPBOX_TOKEN,
      style: 'mapbox://styles/calaster/ckbso5bl203ds1ip7yj0yvhkc?optimize=true',
    };
  },
  watch: {
    city() {
      this.dates = [this.city.max_date];
    },
    type() {
      if (this.map.isStyleLoaded()) {
        if (this.map.getSource('calls')) {
          this.delHeatmap();
        }
        if (this.type === 'heatmap') {
          this.map.on('load', this.addHeatmap());
        }
      }
    },
    data() {
      if (this.map.isStyleLoaded() && this.type === 'heatmap') {
        if (this.map.getSource('calls')) {
          this.delHeatmap();
        }
        this.map.on('load', this.addHeatmap());
      }
    },
    dates() {
      this.fetch();
    },
  },
  computed: {
    overlay() {
      return this.loading || this.blocking;
    },
    isCityReady() {
      return !isEmpty(this.city);
    },
    isDateReady() {
      return this.dates.length > 0;
    },
  },
  methods: {
    days(start, end) {
      var d_0 = new Date(start);
      var d_1 = new Date(end);
      return (d_1.getTime() - d_0.getTime()) / (1000 * 3600 * 24);
    },
    fetch() {
      if (this.$vuetify.breakpoint.lgAndUp) {
        var sDates = cloneDeep(this.dates);
        sDates.sort();
        let nDays = this.days(sDates[0], sDates[1] ? sDates[1] : sDates[0]);
        if (nDays > 7) {
          this.blocking = true;
        } else {
          this.loading = true;
          this.blocking = false;
          let url = '/spatial/' + this.$route.params.id + '?';
          url += `start=${sDates[0]}&end=${sDates[1] ? sDates[1] : sDates[0]}`;
          this.$http
            .get(url)
            .then((response) => {
              this.loading = false;
              this.records = response.data.nRecords;
              this.data = response.data.geojson;
            })
            .catch((error) => {
              this.loading = false;
              console.log(error);
            });
        }
      }
    },
    delHeatmap() {
      this.map.removeLayer('heatmap');
      this.map.removeLayer('calls');
      this.map.removeSource('calls');
    },
    addHeatmap() {
      this.map.addSource('calls', {
        type: 'geojson',
        data: this.data,
      });
      this.map.addLayer(
        {
          id: 'heatmap',
          type: 'heatmap',
          source: 'calls',
          maxzoom: 15,
          paint: {
            'heatmap-weight': {
              property: 'dbh',
              type: 'exponential',
              stops: [
                [1, 0],
                [62, 1],
              ],
            },
            'heatmap-intensity': {
              stops: [
                [11, 1],
                [15, 3],
              ],
            },
            'heatmap-color': [
              'interpolate',
              ['linear'],
              ['heatmap-density'],
              0,
              'transparent',
              0.2,
              '#ECE7BA',
              0.4,
              '#ECE077',
              0.6,
              '#D8A151',
              0.8,
              '#987138',
            ],
            'heatmap-radius': {
              stops: [
                [11, 15],
                [15, 20],
              ],
            },
            'heatmap-opacity': {
              default: 1,
              stops: [
                [14, 1],
                [15, 0],
              ],
            },
          },
        },
        'waterway-label',
      );
      this.map.addLayer(
        {
          id: 'calls',
          type: 'circle',
          source: 'calls',
          minzoom: 14,
          paint: {
            'circle-radius': {
              property: 'dbh',
              type: 'exponential',
              stops: [
                [{ zoom: 15, value: 1 }, 5],
                [{ zoom: 15, value: 62 }, 10],
                [{ zoom: 22, value: 1 }, 20],
                [{ zoom: 22, value: 62 }, 50],
              ],
            },
            'circle-color': {
              property: 'dbh',
              type: 'exponential',
              stops: [
                [0, 'rgba(236,222,239,0)'],
                [10, 'rgb(236,222,239)'],
                [20, 'rgb(208,209,230)'],
                [30, 'rgb(166,189,219)'],
                [40, 'rgb(103,169,207)'],
                [50, 'rgb(28,144,153)'],
                [60, 'rgb(1,108,89)'],
              ],
            },
            'circle-stroke-color': 'white',
            'circle-stroke-width': 1,
            'circle-opacity': {
              stops: [
                [14, 0],
                [15, 1],
              ],
            },
          },
        },
        'waterway-label',
      );
    },
  },
};
</script>

<template>
  <v-card class="card d-none d-md-block">
    <v-row
      no-gutters
      style="
        display: flex;
        height: 100%;
        justify-content: center;
        align-items: center;
      "
    >
      <v-progress-linear
        v-if="cities.length == 0"
        indeterminate
        color="tertiary"
      />
      <span
        v-else
        class="subtitle-3 variant--text"
      >
        <b>{{ nCalls != 0 ? nCalls.toLocaleString() : "--" }}</b> calls reported
        for a total of <b>{{ cities.length }}</b> cities
      </span>
    </v-row>
  </v-card>
</template>

<style type="scss" scoped>
  .card {
    height: 48px;
    min-width: 400px;
    padding: 0 20px;
    background-color: var(--v-surface-base) !important;
    border-radius: 4px !important;
    border: solid 1px #e5e9ed !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
    position: absolute;
    top: 10px;
    left: calc(50% - 200px);
  }
</style>

<script>
  export default {
    props: {
      cities: {
        type: Array,
        default: () => []
      }
    },
    computed: {
      nCalls() {
        var cnt = 0
        this.cities.forEach(x => {
          cnt += x.num_calls
        })
        return cnt
      }
    }
  }
</script>
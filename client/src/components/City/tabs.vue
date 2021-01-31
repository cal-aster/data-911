<template>
  <v-card
    class="card"
  >
    <v-tabs
      grow
      v-model="tab"
      center-active
      height="30px"
      background-color="transparent"
      slider-color="transparent"
      active-class="active"
      style="padding: 0; margin: 0;"
    >
      <v-tab class="body tab">
        Overview
      </v-tab>
      <!-- <v-tab disabled class="body tab" style="margin: 0 20px;">
        Statistics
      </v-tab>
      <v-tab disabled class="body tab">
        Priorities
      </v-tab> -->
    </v-tabs>
  </v-card>
</template>

<style type="scss" scoped>
  .tab {
    text-transform: none;
    font-size: 14px;
    font-weight: normal;
    font-weight: bold !important;
    color: var(--v-primary-base) !important;
  }
  .active {
    height: 30px !important;
    border-radius: 4px;
    background-color: var(--v-tertiary-base) !important;
    color: var(--v-surface-base) !important;
  }
  .card {
    padding: 4px;
    height: 38px;
    background-color: var(--v-surface-base) !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  }
</style>

<script>
  export default {
    data() {
      return {
        tab: 0
      }
    },
    watch: {
      tab() {
        this.$emit('tab', this.tab)
      }
    }
  }
</script>
<template>
  <v-card class="component">
    <v-col
      cols="6"
      style="
        padding: 0;
        margin: 0;
        display: flex;
      "
    >
      <v-btn
        text
        width="100%"
        class="text-none button body"
        @click="
          $emit('toggle', 'heatmap');
          toggle = 'heatmap';
        "
        style="border-radius: 4px 0px 0px 4px !important;"
        v-bind:class="{
          'active': toggle == 'heatmap'
        }"
      >
        <span>heatmap</span>
      </v-btn>
    </v-col>
    <v-col
      cols="6"
      style="
        padding: 0;
        margin: 0;
        display: flex;
      "
    >
      <v-btn
        text
        width="100%"
        class="text-none button body"
        @click="
          $emit('toggle', 'clusters');
          toggle = 'clusters';
        "
        style="border-radius: 0px 4px 4px 0px !important;"
        v-bind:class="{
          'active': toggle == 'clusters'
        }"
      >
        <span>clusters</span>
      </v-btn>
    </v-col>
  </v-card>
</template>

<style type="scss" scoped>
  .component {
    height: 32px;
    width: 180px;
    padding: 0;
    background-color: var(--v-surface-base) !important;
    border-radius: 4px !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
    position: absolute;
    display: flex;
    top: 10px;
    left: calc(33.3% + 30px);
    z-index: 5;
  }
  .button {
    height: 32px !important;
    border: solid 1px #e5e9ed !important;
  }
  .button span {
    font-size: 14px !important;
    font-weight: bold;
    color: rgb(0, 0, 0, 0.33) !important;
  }
  .active {
    background-color: var(--v-tertiary-base) !important;
    border: solid 1px var(--v-tertiary-base) !important;
  }
  .active span {
    color: var(--v-surface-base) !important;
  }
  .button:hover {
    background-color: var(--v-tertiary-base) !important;
    border: solid 1px var(--v-surface-base) !important;
  }
  .button:hover span {
    color: var(--v-surface-base) !important;
  }
  @media only screen and (max-width: 1904px) {
    .component {
      left: calc(50% + 30px);
    }
  }
  @media only screen and (max-width: 1264px) {
    .component {
      display: none;
    }
  }
</style>

<script>
export default {
  data() {
    return {
      toggle: 'heatmap'
    }
  }
}
</script>
<template>
  <v-card class="component">
    <v-row no-gutters>
      <span
        class="body"
        style="
          color: rgb(0, 0, 0, 0.33);
          font-size: 14px;
          font-weight: bold;
        "
      >
        <b class="tertiary--text">{{ data ? data.features.length : "0" }}</b> of
        <b class="primary--text">{{ records }}</b> records are geolocalized
      </span>
    </v-row>
  </v-card>
</template>

<style type="scss" scoped>
.component {
  height: 32px;
  min-width: fit-content;
  padding: 0 16px;
  background-color: var(--v-surface-base) !important;
  border-radius: 4px !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  position: absolute;
  display: flex;
  bottom: 10px;
  left: calc(33.3% + 30px);
  z-index: 5;
  align-items: center;
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
  props: {
    data: {
      type: Object,
      default: () => {}
    },
    records: {
      type: Number,
      default: 0
    }
  }
};
</script>

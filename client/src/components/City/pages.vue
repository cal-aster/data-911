<template>
  <v-tabs-items
    v-model="tab"
    style="
      height: calc(100vh - 174px);
      max-height: calc(100vh - 174px);
      background-color: transparent;
    "
  >
    <v-tab-item>
      <city-pages-overview :city="city" style="margin-top: 12px;" />
    </v-tab-item>
  </v-tabs-items>
</template>

<script>
export default {
  props: {
    tab: {
      type: Number,
      default: 0
    },
    city: {
      type: Object,
      default: () => {}
    }
  }
};
</script>

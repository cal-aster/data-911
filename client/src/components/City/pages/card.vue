<template>
  <v-card
    class="card"
    v-bind:style="{
      display: $vuetify.breakpoint.xs ? 'flex' : 'inherit'
    }"
  >
    <v-col
      cols="6"
      sm="12"
      style="
        background-color: var(--v-background-base);
        padding: 10px 16px 10px 24px;
        align-items: center;
        display: flex;
      "
    >
      <span
        class="body primary--text"
        style="font-weight: bold; font-size: 18px;"
      >
        {{ title }}
      </span>
    </v-col>
    <v-col
      cols="6"
      sm="12"
      style="
        padding: 12px 24px;
        display: flex;
        align-items: center;
      "
      v-bind:style="{
        placeContent: $vuetify.breakpoint.xs ? 'flex-end' : 'inherit'
      }"
    >
      <span
        class="subtitle-3 primary--text"
        style="
          display: block;
          font-weight: bold;
          font-size: 18px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        "
      >
        {{ value }}
      </span>
    </v-col>
  </v-card>
</template>

<style type="scss" scoped>
.card {
  background-color: var(--v-surface-base) !important;
  border-radius: 4px !important;
  border: solid 1px #e5e9ed !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
}
</style>

<script>
export default {
  props: {
    title: {
      type: String,
      default: "---"
    },
    value: {
      type: String,
      default: null
    }
  }
};
</script>

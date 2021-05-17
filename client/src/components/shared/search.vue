<template>
  <v-card class="card" elevation="0">
    <v-text-field
      dense
      flat
      solo
      hide-details
      v-model="search"
      :placeholder="placeholder"
      single-line
      height="46px"
      class="subtitle-3"
    >
      <template slot="append">
        <v-icon small color="tertiary">
          mdi-magnify
        </v-icon>
      </template>
    </v-text-field>
  </v-card>
</template>

<style type="scss" scoped>
.card {
  max-height: 48px;
  border-radius: 4px !important;
  padding: 0px !important;
  background-color: var(--v-surface-base) !important;
  border: 1px solid #e5e9ed !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  width: 200px !important;
}
.card:hover {
  border: 1px solid var(--v-secondary-base) !important;
}
</style>

<script>
export default {
  props: {
    placeholder: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      search: '',
    };
  },
  watch: {
    search() {
      if (!this.search) {
        this.search = '';
      }
      this.$emit('search', this.search);
    },
  },
};
</script>

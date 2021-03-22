<template>
  <v-card
    color="surface"
    elevation="0"
    style="
      width: 100%;
      height: fit-content;
    "
    v-bind:style="{
      padding: $vuetify.breakpoint.xs ? '0 10px' : '10px 20px',
      borderRadius: $vuetify.breakpoint.xs ? '0' : '4px',
      border: $vuetify.breakpoint.xs ? 'none' : '1px solid #efefef',
      boxShadow: $vuetify.breakpoint.xs
        ? 'none'
        : '0 1px 4px 0 rgba(0, 0, 0, 0.14)'
    }"
  >
    <v-card-title>
      <span class="variant--text">
        {{ title }}
      </span>
    </v-card-title>
    <v-divider style="margin: 4px 0px;" />
    <v-row
      no-gutters
      style="
        width: 100%;
        padding: 16px 10px;
      "
    >
      <v-col cols="4" style="padding: 0 4px;">
        <v-row no-gutters style="justify-content: center; margin-bottom: 10px;">
          <span class="title primary--text">Min</span>
        </v-row>
        <v-row no-gutters style="justify-content: center;">
          <span class="body tertiary--text" style="font-weight: bold;">
            {{ format(min) }}
          </span>
        </v-row>
      </v-col>
      <v-col cols="4" style="padding: 0 4px;">
        <v-row no-gutters style="justify-content: center; margin-bottom: 10px;">
          <span class="title primary--text">Avg</span>
        </v-row>
        <v-row no-gutters style="justify-content: center;">
          <span class="body tertiary--text" style="font-weight: bold;">
            {{ format(avg) }}
          </span>
        </v-row>
      </v-col>
      <v-col cols="4" style="padding: 0 4px;">
        <v-row no-gutters style="justify-content: center; margin-bottom: 10px;">
          <span class="title primary--text">Max</span>
        </v-row>
        <v-row no-gutters style="justify-content: center;">
          <span class="body tertiary--text" style="font-weight: bold;">
            {{ format(max) }}
          </span>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: null
    },
    min: {
      type: Number,
      default: 0.0
    },
    avg: {
      type: Number,
      default: 0.0
    },
    max: {
      type: Number,
      default: 0.0
    }
  },
  methods: {
    format(t) {
      let tmp = t * 1000;
      if (tmp < 1000) {
        return `${tmp.toFixed(2)}ms`;
      } else {
        return `${t.toFixed(2)}s`;
      }
    }
  }
};
</script>

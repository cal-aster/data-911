<template>
  <v-card class="card">
    <v-row
      no-gutters
      style="
        display: flex;
        height: 100%;
        justify-content: center;
        align-items: center;
      "
    >
      <v-icon
        small
        v-if="$vuetify.breakpoint.lgAndUp"
        :color="city.department == 'police' ? 'var(--v-tertiary-base)' :
                city.department == 'fire' ? '#D56956' : 'var(--v-background-base)'"
        style="margin-right: 10px;"
      >
        {{
          city.department == 'police' ? 'mdi-police-badge' :
          city.department == 'fire' ? 'mdi-fire' : 'mdi-pencil'
        }}
      </v-icon>
      <span
        v-if="$vuetify.breakpoint.xlAndUp"
        style="font-weight: bold; margin-right: 26px; text-transform: capitalize;"
        class="subtitle-3"
        v-bind:class="{
          'tertiary--text': city.department == 'police',
          'error--text': city.department == 'fire'
        }"
      >
        {{ city.department }}
      </span>
      <v-icon
        v-if="$vuetify.breakpoint.smAndUp"
        small
        color="tertiary"
        style="margin-right: 10px;"
      >
        mdi-database
      </v-icon>
      <span
        v-if="$vuetify.breakpoint.smAndUp"
        style="font-weight: bold; margin-right: 26px;"
        class="subtitle-3 tertiary--text"
      >
        {{ city.num_calls ? city.num_calls.toLocaleString() : '--' }} records
      </span>
      <v-spacer />
      <span
        class="body primary--text"
        style="font-weight: bold; font-size: 20px;"
      >
        {{ city.city }}, {{ city.state }}
      </span>
    </v-row>
  </v-card>
</template>

<style type="scss" scoped>
  .card {
    height: 48px;
    min-width: fit-content;
    padding: 0px 20px;
    background-color: var(--v-surface-base) !important;
    border-radius: 4px !important;
    border: solid 1px #e5e9ed !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
    position: absolute;
    top: 10px;
    right: calc(66.6% + 30px);
  }
  @media only screen and (max-width: 1904px) {
    .card {
      right: calc(50% + 30px);
    }
  }
  @media only screen and (max-width: 1264px) {
    .card {
      right: 30px;
    }
  }
  @media only screen and (max-width: 960px) {
    .card {
      right: 10px;
    }
  }
</style>

<script>
  export default {
    props: {
      city: {
        type: Object,
        default: () => {}
      }
    }
  }
</script>
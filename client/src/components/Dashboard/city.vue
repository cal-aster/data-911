<template>
  <div>
    <v-card class="card">
      <v-card-title
        style="
          padding: 12px 16px 12px 24px;
        "
        v-bind:style="{
          backgroundColor:
            city.department == 'police'
              ? 'var(--v-secondary-base)'
              : city.department == 'fire'
              ? 'var(--v-error-base)'
              : 'var(--v-background-base)'
        }"
      >
        <v-row no-gutters style="width: 100%;">
          <span style="font-weight: bold;" class="headline-3 surface--text">
            {{ city.city }}
          </span>
          <v-spacer />
          <v-btn icon @click="modal = true">
            <v-icon size="20" color="surface">
              {{
                city.department == "police"
                  ? "mdi-police-badge"
                  : city.department == "fire"
                  ? "mdi-fire"
                  : "mdi-pencil"
              }}
            </v-icon>
          </v-btn>
        </v-row>
        <v-row no-gutters style="width: 100%;">
          <span class="subtitle-3 surface--text">
            {{ city.state_name }}
          </span>
        </v-row>
        <v-row
          style="
            margin: 0;
            padding: 6px 24px 6px 12px;
            border-radius: 4px 0px 0px 4px;
            position: absolute;
            right: 0px;
            top: 62px;
            min-width: fit-content;
          "
          v-bind:style="{
            backgroundColor:
              city.department == 'police'
                ? 'var(--v-tertiary-base)'
                : city.department == 'fire'
                ? '#D56956'
                : 'var(--v-background-base)'
          }"
        >
          <v-spacer />
          <v-icon small color="surface" style="margin-right: 10px;">
            mdi-phone
          </v-icon>
          <span style="font-weight: bold;" class="subtitle-3 surface--text">
            {{ city.num_calls ? city.num_calls.toLocaleString() : "--" }}
          </span>
        </v-row>
      </v-card-title>
      <v-card-text style="padding: 12px 24px;">
        <v-row no-gutters style="width: 100%;">
          <span class="subtitle-3" style="font-weight: bold;">
            Latest:
          </span>
        </v-row>
        <v-row no-gutters style="width: 100%;">
          <span class="subtitle-3">
            {{ city.max_date }}
          </span>
          <v-spacer />
          <a @click="$router.push('/city/' + city.id)" class="explorer">
            explore
            <v-icon
              small
              :color="
                city.department == 'police'
                  ? 'tertiary'
                  : city.department == 'fire'
                  ? '#D56956'
                  : 'background'
              "
            >
              mdi-play
            </v-icon>
          </a>
        </v-row>
      </v-card-text>
    </v-card>
    <v-dialog
      v-model="modal"
      :fullscreen="$vuetify.breakpoint.xs"
      width="780px"
    >
      <dashboard-description :city="city" v-on:close="modal = false" />
    </v-dialog>
  </div>
</template>

<style type="scss" scoped>
.card {
  background-color: var(--v-surface-base) !important;
  border-radius: 4px !important;
  border: solid 1px #e5e9ed !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
}
.card:hover {
  border: solid 1px var(--v-secondary-base) !important;
  box-shadow: 1px 2px 4px 1px rgba(0, 0, 0, 0.14) !important;
}
.explorer {
  margin-top: -2px;
  font-size: 14px;
  font-weight: bold;
  text-decoration: none;
}
.explorer:hover i {
  margin-left: 4px;
}
</style>

<script>
export default {
  props: {
    city: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      modal: false
    };
  }
};
</script>

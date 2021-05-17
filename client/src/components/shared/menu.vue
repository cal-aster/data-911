<template>
  <div>
    <div class="dial">
      <v-speed-dial
        v-if="!$vuetify.breakpoint.xs && $route.name != 'City'"
        v-model="menu"
        direction="right"
        transition="slide-x-reverse-transition"
      >
        <template v-slot:activator>
          <v-btn v-model="menu" class="navigation" active-class="active-menu">
            <v-icon v-if="menu">
              mdi-close
            </v-icon>
            <v-img
              v-else
              contain
              src="@/assets/logo.png"
              max-height="28"
              max-width="28"
            />
          </v-btn>
        </template>
        <v-btn
          v-if="!$vuetify.breakpoint.xs"
          class="shadowed text-none navigation bar"
          active-class="active"
          to="/"
        >
          Home
        </v-btn>
        <v-btn
          v-if="!$vuetify.breakpoint.xs"
          class="shadowed text-none navigation bar"
          active-class="active"
          to="/dashboard"
        >
          Dashboard
        </v-btn>
        <v-btn
          v-if="!$vuetify.breakpoint.xs"
          class="shadowed text-none navigation bar"
          active-class="active"
          to="/team"
        >
          Team
        </v-btn>
      </v-speed-dial>
      <v-btn
        v-if="$route.name == 'City'"
        class="navigation active-menu"
        @click="$router.push('/dashboard')"
      >
        <v-icon color="tertiary">
          mdi-view-dashboard
        </v-icon>
        <span
          v-if="$vuetify.breakpoint.smAndUp"
          style="font-weight: bold; margin-left: 12px;"
          class="subtitle-3 primary--text"
        >
          Dashboard
        </span>
      </v-btn>
      <v-btn
        v-if="$vuetify.breakpoint.xs && $route.name != 'City'"
        class="navigation"
        active-class="active-menu"
        @click="menu = !menu"
      >
        <v-img contain src="@/assets/logo.png" max-height="28" max-width="28" />
      </v-btn>
    </div>
    <v-navigation-drawer
      v-if="$vuetify.breakpoint.xs"
      v-model="menu"
      fixed
      bottom
      style="
        z-index: 100;
        min-height: 100vh;
      "
    >
      <v-row
        no-gutters
        style="
          position: absolute;
          top: 0;
          left: 0;
          height: 64px;
          width: 100vw;
          padding: 0 16px;
          background-color: var(--v-surface-base);
        "
      >
        <v-img
          contain
          max-width="28px"
          max-height="28px"
          src="@/assets/logo.png"
          style="align-self: center; margin-left: 12px;"
        />
        <v-spacer />
        <v-btn icon @click="menu = false" style="align-self: center;">
          <v-icon style="margin-right: 12px;" color="variant">
            mdi-close
          </v-icon>
        </v-btn>
      </v-row>
      <v-layout
        column
        justify-space-around
        style="
          width: 100vw;
          height: calc(100vh - 64px);
          position: absolute;
          display: flex;
          bottom: 0;
        "
      >
        <v-row
          no-gutters
          style="
            width: 100vw;
            align-content: center;
            justify-content: center;
          "
        >
          <a
            @click="
              $router.push('/').catch(() => {});
              menu = false;
            "
          >
            <span class="headline-3" style="font-weight: bold;">
              Home
            </span>
          </a>
        </v-row>
        <v-row
          no-gutters
          style="
            width: 100vw;
            align-content: center;
            justify-content: center;
          "
        >
          <a
            @click="
              $router.push('/dashboard').catch(() => {});
              menu = false;
            "
          >
            <span class="headline-3" style="font-weight: bold;">
              Dashboard
            </span>
          </a>
        </v-row>
        <v-row
          no-gutters
          style="
            width: 100vw;
            align-content: center;
            justify-content: center;
          "
        >
          <a
            @click="
              $router.push('/team').catch(() => {});
              menu = false;
            "
          >
            <span class="headline-3" style="font-weight: bold;">
              Team
            </span>
          </a>
        </v-row>
      </v-layout>
    </v-navigation-drawer>
  </div>
</template>

<style style="scss">
.dial {
  position: absolute;
  top: 10px;
  left: 30px;
}
.navigation {
  border-radius: 4px !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  height: 48px !important;
  border: 1px solid #e5e9ed !important;
  padding: 0px 16px !important;
  background-color: var(--v-surface-base) !important;
}
.navigation span {
  font-size: 14px;
  font-weight: bold;
  font-stretch: normal;
  font-style: normal;
  line-height: 1.25;
  letter-spacing: 0.8px;
  text-align: center;
  color: var(--v-primary-base) !important;
  text-transform: none !important;
}
.navigation:hover {
  border: solid 1px var(--v-secondary-base) !important;
  color: var(--v-surface-base) !important;
  background-color: var(--v-surface-base) !important;
  opacity: 1 !important;
}
.navigation:hover span {
  color: var(--v-primary-base) !important;
}
.navigation:active {
  border: solid 2px var(--v-secondary-base) !important;
  color: transparent !important;
}
.active {
  border: solid 1px var(--v-secondary-base) !important;
  color: var(--v-surface-base) !important;
  background-color: var(--v-surface-base) !important;
}
.active-menu {
  border: solid 1px transparent !important;
  color: var(--v-primary-base) !important;
  background-color: var(--v-surface-base) !important;
}
@media only screen and (max-width: 960px) {
  .dial {
    left: 10px;
  }
}
</style>

<script>
export default {
  data() {
    return {
      menu: false,
    };
  },
};
</script>

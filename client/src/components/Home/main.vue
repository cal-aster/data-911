<template>
  <v-container fluid fill-height>
    <v-row
      justify="center"
      no-gutters
      style="
        margin: 0 auto;
        width: 1400px;
        max-width: 1400px;
        overflow: hidden;
      "
    >
      <div
        style="
          min-width: min(28vw, 360px);
          max-width: min(28vw, 360px);
          max-height: min(24vw, 300px);
          overflow: hidden;
          text-align: right;
        "
      >
        <transition name="slide-fade" mode="out-in">
          <div v-if="state == 0">
            <span
              style="
                font-size: min(20vw, 220px);
                color: var(--v-tertiary-base);
                font-weight: normal;
                text-align: end;
              "
            >
              Cal
            </span>
          </div>
        </transition>
        <transition name="slide-fade" mode="out-in">
          <div v-if="state == 1">
            <span
              style="
                font-size: min(20vw, 220px);
                color: var(--v-tertiary-base)
                font-weight: bold;
                letter-spacing: max(-1.5vw, -21px);
              "
            >
              911
            </span>
          </div>
        </transition>
      </div>
      <span
        style="
          font-size: min(20vw, 220px);
          color: var(--v-primary-base)
          font-weight: bold;
        "
      >
        Aster
      </span>
    </v-row>
    <div style="display: contents;">
      <v-row
        v-if="$vuetify.breakpoint.xs"
        justify="center"
        no-gutters
        style="
          margin: auto;
          width: 100%;
          align-items: center;
        "
      >
        <v-btn to="/dashboard" class="explore">
          Explore
        </v-btn>
      </v-row>
      <v-row
        justify="center"
        no-gutters
        style="
          margin: 0 auto auto auto;
          width: 1400px;
          max-width: 1400px;
          align-items: center;
        "
      >
        <v-btn
          v-if="$vuetify.breakpoint.smAndUp"
          to="/dashboard"
          class="explore"
        >
          Explore
        </v-btn>
        <span
          style="
            font-weight: bold;
            display: flex;
          "
          v-bind:style="{
            fontSize: $vuetify.breakpoint.xs ? '6vw' : 'min(4vw, 28px)',
            marginTop: $vuetify.breakpoint.xs ? '20px' : '0',
            marginLeft: $vuetify.breakpoint.xs ? '0' : '16px',
            justifyContent: $vuetify.breakpoint.xs ? 'center' : 'start',
            textAlign: $vuetify.breakpoint.xs ? 'center' : 'start'
          }"
        >
          {{
            $vuetify.breakpoint.xs
              ? "How are call centers"
              : "how call centers are"
          }}
          <br v-if="$vuetify.breakpoint.xs" />
          doing near you{{ $vuetify.breakpoint.xs ? "?" : "" }}
        </span>
      </v-row>
    </div>
  </v-container>
</template>

<style style="scss" scoped>
.explore {
  border-radius: 4px !important;
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.14) !important;
  height: min(14vw, 64px) !important;
  padding: 0px 16px !important;
  background-color: var(--v-surface-base) !important;
  opacity: 1 !important;
  -webkit-transition: background-color 1s;
  text-align: right;
}
.explore >>> span {
  font-size: min(4vw, 28px);
  font-weight: bold;
  font-stretch: normal;
  font-style: normal;
  line-height: 1.25;
  letter-spacing: 0.8px;
  text-align: center;
  color: var(--v-primary-base) !important;
  text-transform: none !important;
  -webkit-transition: all 1s ease;
}
.explore:hover {
  background-color: var(--v-tertiary-base) !important;
  -webkit-transition: all 1s ease;
}
.explore:hover >>> span {
  color: var(--v-surface-base) !important;
  -webkit-transition: all 1s ease;
}
.slide-fade-enter-active {
  transition: all 2s ease;
}
.slide-fade-leave-active {
  opacity: 0;
}
.slide-fade-enter,
.slide-fade-leave-to {
  transform: translateY(60px);
  opacity: 0;
}
@media only screen and (max-width: 600px) {
  .explore >>> span {
    font-size: 7vw;
  }
}
</style>

<script>
export default {
  metaInfo: {
    title: "Data911",
    htmlAttrs: {
      lang: "en"
    }
  },
  data() {
    return {
      state: 0
    };
  },
  mounted() {
    setInterval(() => {
      this.state = (this.state + 1) % 2;
    }, 3000);
  }
};
</script>

<template>
  <v-container
    fluid
    fill-height
  >
    <v-row
      justify="center"
      no-gutters
      style="
        margin: 0 auto;
        width: 1400px;
        max-width: 1400px;
        align-items: center;
      "
    >
        <v-col
          cols="12"
          md="6"
          v-bind:style="{
            padding: $vuetify.breakpoint.smAndDown ? '0': '0 20px',
            margin: $vuetify.breakpoint.smAndDown ? '70px 0 40px 0' : '0'
          }"
        >
          <div style="width: 100%;">
            <span
              class="text--primary"
              style="
                display: block;
                font-size: min(4.5vw, 20px) !important;
                font-weight: normal;
                line-height: min(6vw, 30px) !important;
              "
            >
              At <shared-calaster />, we are a team passionate about bringing
              meaningful change to the emergency response ecosystem. By analyzing emergency
              calls in real time, we ensure that 911 operators can focus their efforts on
              providing emotional support to victims during emergencies. By relieving
              operators of the burden of taking notes and extracting key information from calls,
              we limit call time, ensuring operators can address the next emergency faster.
              <br /><br />
              <shared-calaster /> has built the first visualization platform
              gathering performance metrics for 911 call centers across the US.
            </span>
          </div>
        </v-col>
        <v-spacer />
        <v-col
          cols="12"
          md="5"
          style="height: 100%; padding: 0px;"
          v-bind:style="{
            marginBottom: $vuetify.breakpoint.smAndDown ? '70px' : '0'
          }"
        >
          <v-row no-gutters>
            <v-spacer />
            <team-contributor
              style="align-self: center;"
              firstname="Meryll"
              lastname="Dindin"
              role="Architect"
              :picture="require('@/assets/contributors/meryll-dindin.jpg')"
              :lazy="require('@/assets/contributors/meryll-dindin-lazy.jpg')"
              linkedin="https://www.linkedin.com/in/dindin-meryll/"
            />
            <v-spacer />
          </v-row>
          <v-row no-gutters>
            <v-spacer />
            <v-col cols="12" sm="5" style="padding: 0; text-align: -webkit-center;">
              <team-contributor
                style="align-self: center;"
                firstname="Neha"
                lastname="Dhingra"
                role="Backend Wizard"
                :picture="require('@/assets/contributors/neha-dhingra.jpg')"
                :lazy="require('@/assets/contributors/neha-dhingra-lazy.jpg')"
                linkedin="https://www.linkedin.com/in/neha-dhingra-068235173/"
                v-bind:style="{
                  marginTop: $vuetify.breakpoint.xs ? '0' : '80px'
                }"
              />
            </v-col>
            <v-spacer />
            <v-col cols="12" sm="5" style="text-align: -webkit-center;">
              <team-contributor
                style="align-self: center;"
                firstname="Pierre-Louis"
                lastname="Missler"
                role="Data Hero"
                :picture="require('@/assets/contributors/pierre-louis-missler.jpg')"
                :lazy="require('@/assets/contributors/pierre-louis-missler-lazy.jpg')"
                linkedin="https://www.linkedin.com/in/pierrelouismissler/"
                v-bind:style="{
                  marginTop: $vuetify.breakpoint.xs ? '12px' : '80px'
                }"
              />
            </v-col>
            <v-spacer />
          </v-row>
        </v-col>
      </v-row>
  </v-container>
</template>

<style style="scss" scoped>
</style>

<template>
  <v-container fluid fill-height>
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
          padding: $vuetify.breakpoint.smAndDown ? '0' : '0 20px',
          margin: $vuetify.breakpoint.smAndDown ? '70px 0 40px 0' : '0'
        }"
      >
        <div style="width: 100%;">
          <p class="text">
            The only way to truly empower first responders is by disrupting the
            workflow in several places simultaneously. CalAster focuses on
            mental health support, but our work has an even broader scope.
          </p>
          <p class="text">
            CalAster has built the first open-source visualization platform for
            911 call center data across the US. We are continuously increasing
            the list of available cities so check it out!
          </p>
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
          <v-col
            cols="12"
            sm="5"
            style="padding: 0; text-align: -webkit-center;"
          >
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
              :picture="
                require('@/assets/contributors/pierre-louis-missler.jpg')
              "
              :lazy="
                require('@/assets/contributors/pierre-louis-missler-lazy.jpg')
              "
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
.text {
  font-size: 24px;
  font-weight: normal;
  font-stretch: normal;
  font-style: normal;
  line-height: 1.5;
  letter-spacing: normal;
  text-align: left;
  color: var(--v-primary-base);
  word-break: break-word;
}
@media only screen and (max-width: 1904px) {
  .text {
    font-size: 22px;
  }
}
@media only screen and (max-width: 1264px) {
  .text {
    font-size: 20px;
  }
}
@media only screen and (max-width: 960px) {
  .text {
    font-size: 16px;
  }
}
</style>

<script>
export default {
  metaInfo: {
    title: "Data911 - Team",
    htmlAttrs: {
      lang: "en"
    }
  }
};
</script>

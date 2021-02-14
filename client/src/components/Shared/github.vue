<template>
  <v-card
    class="card"
  >
    <span
      style="
        font-size: 12px;
        font-weight: bold;
        color: rgb(0, 0, 0, 0.33);
        align-self: center;
        display: flex;
        text-decoration: none;
      "
    >
      <a
        href="https://github.com/cal-aster/data-911"
        target="_blank"
        style="
          text-decoration: none;
          color: rgb(0, 0, 0, 0.33);
        "
      >
        <v-icon
          small
          color="tertiary"
        >
          mdi-github
        </v-icon>
        {{ $vuetify.breakpoint.mdAndUp ? 'Github Documentation' : '' }}
      </a>
    </span>
  </v-card>
</template>

<style type="scss" scoped>
  .card {
    height: 32px;
    background-color: var(--v-surface-base) !important;
    border-radius: 4px !important;
    border: solid 1px #e5e9ed !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
    position: absolute;
    bottom: 10px;
    left: 30px;
    padding: 0px 16px;
    display: flex;
  }
  .card:hover {
    border: 1px solid var(--v-secondary-base) !important;
  }
  @media only screen and (max-width: 960px) {
    .card {
      left: 10px;
    }
  }
</style>

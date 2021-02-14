<template>
  <v-card
    class="card"
  >
    <a
      href="https://calaster.com"
      rel="noopener"
      target="_blank"
      style="
        font-size: 12px;
        font-weight: bold;
        color: rgb(0, 0, 0, 0.33);
        align-self: center;
        display: flex;
        text-decoration: none;
      "
    >
      {{ $vuetify.breakpoint.xs ? '&copy; 2021' : 'CalAster, Inc. &copy; 2021' }}
    </a>
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
    right: 30px;
    padding: 0px 16px;
    display: flex;
    z-index: 5;
  }
  .card:hover {
    border: 1px solid var(--v-secondary-base) !important;
  }
  @media only screen and (max-width: 960px) {
    .card {
      right: 10px;
    }
  }
</style>

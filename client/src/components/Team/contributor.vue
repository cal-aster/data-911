<template>
  <v-card
    class="card"
    width="164px"
  >
    <v-hover v-slot="{ hover }">
      <v-avatar
        size="164px"
      >
        <v-img
          :src="picture"
          :lazy-src="lazy"
          :alt="firstname + ' ' + lastname"
        >
          <v-expand-transition>
            <div
              v-if="hover"
              style="
                height: 100%;
                width: 100%;
                padding: 26px 12px;
                background-color: rgb(255, 255, 255, 0.9);
              "
            >
              <p
                class="subtitle-3"
                style="
                  font-weight: bold;
                  text-align: center;
                "
              >
                {{ firstname }}
              </p>
              <p
                class="subtitle-3"
                style="
                  font-weight: bold;
                  color: var(--v-tertiary-base);
                  text-align: center;
                "
              >
                {{ role }}
              </p>
              <a
                class="subtitle-3"
                style="font-weight: bold;"
                :href="linkedin"
                target="_blank"
              >
                LinkedIn
              </a>
            </div>
          </v-expand-transition>
        </v-img>
      </v-avatar>
    </v-hover>
  </v-card>
</template>

<style type="scss" scoped>
  .card {
    cursor: pointer;
    border-radius: 4px !important;
    border: 1px solid #e5e9ed !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.14) !important;
  }
</style>

<script>
export default {
  props: {
    picture: {
      type: String,
      default: null,
    },
    lazy: {
      type: String,
      default: null
    },
    firstname: {
      type: String,
      default: null,
    },
    lastname: {
      type: String,
      default: null,
    },
    role: {
      type: String,
      default: null,
    },
    linkedin: {
      type: String,
      default: null,
    }
  }
};
</script>

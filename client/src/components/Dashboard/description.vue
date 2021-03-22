<template>
  <v-card
    color="surface"
    height="90vh"
    style="margin: 0; padding: 0; border-radius: 0;"
  >
    <v-row
      no-gutters
      style="background-color: var(--v-tertiary-base) !important;"
      v-bind:style="{
        padding: $vuetify.breakpoint.xs
          ? '12px 20px 12px 30px'
          : '12px 30px 12px 40px'
      }"
    >
      <span
        class="body surface--text"
        style="
          font-weight: bold;
          font-size: 14px;
          align-self: center;
          margin-right: 4px;
        "
      >
        {{ city.state_name }} -
      </span>
      <span
        class="body surface--text"
        style="
          font-weight: bold;
          font-size: 20px;
          align-self: center;
        "
      >
        {{ city.city }}
      </span>
      <v-spacer />
      <v-btn icon @click="$emit('close')">
        <v-icon color="surface">mdi-close</v-icon>
      </v-btn>
    </v-row>
    <perfect-scrollbar
      v-if="data"
      v-bind:style="{
        padding: $vuetify.breakpoint.xs ? '10px 20px' : '20px 30px',
        maxHeight: $vuetify.breakpoint.xs
          ? 'calc(100vh - 60px)'
          : 'calc(90vh - 60px)'
      }"
    >
      <span
        v-if="data.description"
        class="body"
        style="
          display: block;
          font-size: 16px;
          padding: 12px 10px 6px 10px;
          font-weight: bold;
        "
      >
        Description:
      </span>
      <span
        v-if="data.description"
        v-html="data.description"
        class="body"
        style="
          font-size: 16px;
          display: block;
          white-space: pre-line;
          background-color: var(--v-background-base) !important;
          border: 2px solid var(--v-background-base) !important;
          border-radius: 4px !important;
          margin: 0px 0px 12px 2px;
          padding: 12px 16px;
        "
      />
      <span
        v-if="data.data_url"
        v-html="`<a href=${data.data_url} target='_blank'>${data.data_url}</a>`"
        class="body"
        style="
          font-size: 16px;
          display: block;
          white-space: pre-line;
          background-color: rgba(113, 157, 224, 0.1) !important;
          border: 2px solid rgba(113, 157, 224, 0.2) !important;
          border-radius: 4px !important;
          margin: 0px 0px 12px 2px;
          padding: 12px 16px;
        "
      />
      <span
        v-if="data.notes"
        class="body"
        style="
          font-size: 16px;
          display: block;
          padding: 12px 10px 6px 10px;
          font-weight: bold;
        "
      >
        Notes:
      </span>
      <span
        v-if="data.notes"
        v-html="data.notes"
        class="body"
        style="
          font-size: 16px;
          display: block;
          white-space: pre-line;
          background-color: var(--v-background-base) !important;
          border: 2px solid var(--v-background-base) !important;
          border-radius: 4px !important;
          margin: 0px 0px 12px 2px;
          padding: 12px 16px;
        "
      />
      <span
        v-if="data.api_url"
        class="body"
        style="
          font-size: 16px;
          display: block;
          padding: 12px 10px 6px 10px;
          font-weight: bold;
        "
      >
        API:
      </span>
      <span
        v-if="data"
        v-html="`<a href=${data.api_url} target='_blank'>${data.api_url}</a>`"
        class="body"
        style="
          font-size: 16px;
          display: block;
          white-space: pre-line;
          background-color: rgba(113, 157, 224, 0.1) !important;
          border: 2px solid rgba(113, 157, 224, 0.2) !important;
          border-radius: 4px !important;
          margin: 0px 0px 12px 2px;
          padding: 12px 16px;
        "
      />
      <v-flex v-for="key in Object.keys(data.attributes).sort()" :key="key">
        <v-row
          class="body"
          style="
            font-size: 14px;
            white-space: pre-line;
            background-color: var(--v-background-base) !important;
            border: 2px solid var(--v-background-base) !important;
            border-radius: 4px !important;
            margin: 0px 0px 12px 2px;
            padding: 8px 16px;
          "
        >
          <b
            style="
              max-width: 70%;
              overflow: hidden;
              white-space: nowrap;
              text-overflow: ellipsis;
            "
          >
            {{ key }}
          </b>
          <v-spacer />
          <span class="variant--text">
            {{
              data.attributes[key]["type"]
                ? data.attributes[key]["type"]
                : "---"
            }}
          </span>
        </v-row>
      </v-flex>
    </perfect-scrollbar>
  </v-card>
</template>

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
      data: null
    };
  },
  created() {
    this.$http.get(`/city/description/${this.city.id}`).then(response => {
      this.data = response.data;
      this.data.attributes = JSON.parse(this.data.attributes);
    });
  }
};
</script>

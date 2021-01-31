<template>
  <v-tabs-items
    v-model="tab"
    style="
      height: 100%;
      background-color: transparent;
    "
  >
    <v-tab-item style="height: calc(100% - 100px)">
      <v-overlay
        v-model="loading"
        absolute
      >
        <v-btn
          text icon
          :loading="true"
          style="background-color: transparent;"
        />
      </v-overlay>
      <v-row
        style="width: 100%; margin: 20px 0px 0px 0px; padding: 0px"
      >
        <v-col cols="6" style="padding: 0px 12px 0px 0px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Number of inbound calls
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.avg_daily_calls : '---' }} calls per day
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" style="padding: 0px 0px 0px 12px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Number of inbound calls
            </v-card-title>
            <v-card-text v-if="city.id" style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.avg_hourly_calls : '---' }} calls per hour
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row
        style="width: 100%; margin: 20px 0px 0px 0px; padding: 0px"
      >
        <v-col cols="6" style="padding: 0px 12px 0px 0px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Number of calls dispatched
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">
              {{ stats ? stats.avg_dispatch : '---' }} calls per hour
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" style="padding: 0px 0px 0px 12px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Average time period between calls
            </v-card-title>
            <v-card-text v-if="city.id" style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.avg_between_calls : '---' }} seconds
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row
        style="width: 100%; margin: 20px 0px 0px 0px; padding: 0px"
      >
        <v-col cols="6" style="padding: 0px 12px 0px 0px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Percentage of overlapping calls
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.avg_overlapping_calls : '---' }} %
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" style="padding: 0px 0px 0px 12px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Reported arrest rate
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.arrest_rate : '---' }} %
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row
        style="width: 100%; margin: 20px 0px 0px 0px; padding: 0px"
      >
        <v-col cols="6" style="padding: 0px 12px 0px 0px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Number of maximum priority calls
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.num_call_top_priority.count : '---' }} calls
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" style="padding: 0px 0px 0px 12px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Response time of maximum priority calls
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.avg_call_response_top_priority : '---' }} seconds
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-tab-item>
    <v-tab-item style="height: calc(100% - 100px)">
      <v-overlay
        v-model="loading"
        absolute
      >
        <v-btn
          text icon
          :loading="true"
          style="background-color: transparent;"
        />
      </v-overlay>
      <v-row
        style="width: 100%; margin: 20px 0px 0px 0px; padding: 0px"
      >
        <v-col cols="6" style="padding: 0px 12px 0px 0px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Burglary related calls
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.burglary_calls.count : '---' }} calls, often around {{ stats ? stats.burglary_calls.most_common_hour : '---' }}:00
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" style="padding: 0px 0px 0px 12px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Domestic violence related calls
            </v-card-title>
            <v-card-text v-if="city.id" style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.domestic_violence_calls.count : '---' }} calls, often around {{ stats ? stats.domestic_violence_calls.most_common_hour : '---' }}:00
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row
        style="width: 100%; margin: 20px 0px 0px 0px; padding: 0px"
      >
        <v-col cols="6" style="padding: 0px 12px 0px 0px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Drug related calls
            </v-card-title>
            <v-card-text style="font-size: 20px; font-weight: bold; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">
              {{ stats ? stats.drug_calls.count : '---' }} calls, often around {{ stats ? stats.drug_calls.most_common_hour : '---' }}:00
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="6" style="padding: 0px 0px 0px 12px;">
          <v-card dark elevation="4" color="#121212" style="padding: 0px 12px;">
            <v-card-title style="font-size: 14px; color: #6495ED;">
              Gun violence related calls
            </v-card-title>
            <v-card-text v-if="city.id" style="font-size: 20px; font-weight: bold;">
              {{ stats ? stats.gun_violence_calls.count : '---' }} calls, often around {{ stats ? stats.gun_violence_calls.most_common_hour : '---' }}:00
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-tab-item>
  </v-tabs-items>
</template>

<script>
  export default {
    props: {
      tab: {
        type: Number,
        default: 0
      }
    }
  };
</script>
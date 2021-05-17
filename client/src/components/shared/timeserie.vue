<script>
import { Line } from 'vue-chartjs';

export default {
  extends: Line,
  props: {
    data: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false,
        },
        scales: {
          yAxes: [
            {
              ticks: {
                display: false,
                beginAtZero: true,
              },
              gridLines: {
                display: false,
                drawBorder: false,
                color: 'rgba(0, 0, 0, 0)',
              },
            },
          ],
          xAxes: [
            {
              ticks: {
                display: false,
              },
              gridLines: {
                display: false,
                drawBorder: false,
                color: 'rgba(0, 0, 0, 0)',
              },
            },
          ],
        },
        tooltips: {
          enabled: true,
          callbacks: {
            label: (tooltipItems) => {
              return tooltipItems.yLabel;
            },
          },
        },
      },
    };
  },
  mounted() {
    this.renderChart(this.data, this.options);
  },
};
</script>

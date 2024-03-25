// Function to render Chart.js graph
function renderChart(labels, data, chartContainerId, label) {
  var ctx = document.getElementById(chartContainerId).getContext("2d");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: label,
          data: data,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  });
}

// Example chart data
var labels = ["January", "February", "March", "April", "May", "June", "July"];
var temperatures = [10, 15, 20, 25, 30, 35, 40];

// Render chart with example data
renderChart(labels, temperatures, "chartContainer", "Chennai Temperature (°C)");

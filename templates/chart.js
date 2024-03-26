document.addEventListener("DOMContentLoaded", function () {
  // Fetch data from SQL table
  Promise.all([
    fetch("/api/weather-data/chennai").then((response) => response.json()),
    fetch("/api/weather-data/madurai").then((response) => response.json())
  ]).then(([chennaiData, maduraiData]) => {
    const chartData = {
      labels: chennaiData.labels,
      datasets: [
        {
          label: "Chennai Temperature (°C)",
          data: chennaiData.temperatures,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
          yAxisID: 'y',
        },
        {
          label: "Madurai Temperature (°C)",
          data: maduraiData.temperatures,
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
          yAxisID: 'y1',
        },
      ],
    };

    const ctx = document.getElementById("weatherChart").getContext("2d");

    new Chart(ctx, {
      type: "line",
      data: chartData,
      options: {
        responsive: true,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        stacked: false,
        plugins: {
          title: {
            display: true,
            text: 'Chennai and Madurai Weather Chart'
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            grid: {
              drawOnChartArea: false,
            },
          },
        }
      },
    });
  }).catch((error) => {
    console.error("Error fetching weather data:", error);
  });
});
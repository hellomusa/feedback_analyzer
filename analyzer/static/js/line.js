$(function(){

  //get the line chart canvas
  var ctx = $("#line-chartcanvas");

  //line chart data
  var data = {
    labels: ["00:00", "06:00", "12:00", "18:00", "24:00"],
    datasets: [
      {
        label: "Tweet Health",
        data: [60, 50, 25, 70, 40],
        backgroundColor: "#4e73df",
        borderColor: "#4e73df",
        fill: false,
        lineTension: 0.5,
        radius: 5
      },
      {
        label: "Site Health",
        data: [69, 35, 35, 60, 50],
        backgroundColor: "#1cc88a",
        borderColor: "lightgreen",
        fill: false,
        lineTension: 0.5,
        radius: 5
      }
    ]
  };

  //options
  var options = {
    responsive: true,
    title: {
      display: true,
      position: "top",
      fontSize: 18,
      fontColor: "#4e73df"
    },
    legend: {
      display: true,
      position: "bottom",
      labels: {
        fontColor: "#333",
        fontSize: 16
      }
    }
  };

  //create Chart class object
  var chart = new Chart(ctx, {
    type: "line",
    data: data,
    options: options
  });
});
google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart);

function drawBarChart() {
  const arrayLength = monthly_spendings.length;
  let content = [["month", "monthly spending"]];
  for (var i = 0; i < arrayLength; i++) {
    content.push([months[i], monthly_spendings[i]]);
  }

  var data = new google.visualization.arrayToDataTable(
      content
      );

  var options = {
    legend: { position: "none" },
    bar: { groupWidth: "50%" },
    axes: {
      x: {
        0: { side: "bottom", label: "" },
      },
    },
  };

  options.colors = ["#0598aa"];
  var chart = new google.charts.Bar(
    document.getElementById("customerSpending")
  );
  chart.draw(data, google.charts.Bar.convertOptions(options));
}

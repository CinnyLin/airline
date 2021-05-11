google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart);

const person6 = ppl2[0];
const person7 = ppl2[1];
const person8 = ppl2[2];
const person9 = ppl2[3];
const person10 = ppl2[4];
const num6 = commissions[0];
const num7 = commissions[1];
const num8 = commissions[2];
const num9 = commissions[3];
const num10 = commissions[4];

function drawBarChart() {
  var data = new google.visualization.arrayToDataTable([
    ["Commission", "amount of commission"],
    [person6, num6],
    [person7, num7],
    [person8, num8],
    [person9, num9],
    [person10, num10],
  ]);

  var options = {
    legend: { position: "none" },
    chart: {
      //title: "Top 5 Customers",
      title: "based on amount of commission in the past year",
    },
    bar: { groupWidth: "50%" },
    axes: {
      x: {
        0: { side: "bottom", label: "" },
      },
    },
  };

  options.colors = ["#0598aa"];
  var chart = new google.charts.Bar(document.getElementById("topCommission"));
  chart.draw(data, google.charts.Bar.convertOptions(options));
}

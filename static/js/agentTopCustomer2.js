google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart2);

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

// the color is not rendering 
function drawBarChart2() {
  var data = new google.visualization.arrayToDataTable([
    ["Commission", "amount of commission", {role: 'style'}],
    [person6, num6, '#0598AA'],
    [person7, num7, '#0598AA'],
    [person8, num8, '#0598AA'],
    [person9, num9, '#0598AA'],
    [person10, num10, '#0598AA'],
  ]);

  var options = {
    legend: { position: "none" },
    chart: {
      title: "Top 5 Customers",
      subtitle: "based on amount of commission in the past year",
    },
    axes: {
      x: {
        0: { side: "bottom", label: "amount of commission in the past year" },
      },
    },
    bar: { groupWidth: "50%" },
  };

  var chart = new google.charts.Bar(document.getElementById("right"));
  // Convert the Classic options to Material options.
  chart.draw(data, google.charts.Bar.convertOptions(options));
}

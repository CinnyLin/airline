google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart);

const person1 = ppl1[0];
const person2 = ppl1[1];
const person3 = ppl1[2];
const person4 = ppl1[3];
const person5 = ppl1[4];
const num1 = tickets[0];
const num2 = tickets[1];
const num3 = tickets[2];
const num4 = tickets[3];
const num5 = tickets[4];

function drawBarChart() {
  var data = new google.visualization.arrayToDataTable([
    ["Tickets", "#tickets"],
    [person1, num1],
    [person2, num2],
    [person3, num3],
    [person4, num4],
    [person5, num5],
  ]);

  var options = {
    legend: { position: "none" },
    chart: {
      // title: "Top 5 Customers",
      title: "based on #tickets in the past 6 months",
    },
    bar: { groupWidth: "50%" },
    axes: {
      x: {
        0: { side: "bottom", label: "" },
      },
    },
  };

  options.colors = ["#0598aa"];
  var chart = new google.charts.Bar(document.getElementById("topTickets"));
  chart.draw(data, google.charts.Bar.convertOptions(options));
}

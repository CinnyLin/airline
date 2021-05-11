google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart);

const time0 = new_time;
const monthticket0 = new_monthticket;

function drawBarChart() {
  var d=[];
  var Header= ["Month", "#tickets"];
  d.push(Header);
  for (var i = 0; i < time0.length; i++) {
      var temp=[];
      temp.push(time0[i]);
      temp.push(monthticket0[i]);

      d.push(temp);
  }
  var data = new google.visualization.arrayToDataTable(d);

  var options = {
    width: 800,
    legend: { position: "none" },
    chart: {
      //title: "amounts of ticket sold",
      title: "based on #tickets monthly",
    },
    axes: {
      x: {
        0: { side: "bottom", label: " " },
      },
    },
    bar: { groupWidth: "50%" },
  };

  options.colors = ["#0598aa"];
  var chart = new google.charts.Bar(document.getElementById("staffTicket"));
  chart.draw(data, google.charts.Bar.convertOptions(options));
}

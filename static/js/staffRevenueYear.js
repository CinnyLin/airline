google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

const ydirect0 = ydirect[0];
const yindirect0 = yindirect[0];

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ['Sales', 'Amount'],
    ['Bought by customer', ydirect0],
    ['Bought via agent', yindirect0],
  ]);

  var options = {
    title: 'Total Revenue Last Year'
  };

  options.colors = ["#6ec6ca", "#0598aa"];
  var chart = new google.visualization.PieChart(document.getElementById('revenueYear'));

  chart.draw(data, options);
}

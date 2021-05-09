d3.csv("toy.csv").then(gotData);


let w = 900;
let h = 500;
let xpadding = 100;
let ypadding = 50;
let viz = d3.select("#container")
  .append("svg")
  .style("width", w)
  .style("height", h)
  .style("outline", "solid black")
  ;

function filterFunction(d) {
    return +d.values > 30;
}

function gotData(incomingData) {
  
  console.log(incomingData);

  let sortedData = incomingData.sort(function (a, b) { return b.values - a.values })
  console.log(sortedData);
  console.log(+sortedData[6].values);

  let reducedData = incomingData.filter(function(d){ return +d.values > +sortedData[6].values; });
  console.log(reducedData);

  let allNames = reducedData.map(function (d) { return d.person });
  console.log(allNames)
  
  let xScale = d3.scaleBand().domain(allNames).range([xpadding, w - xpadding]);
  let xAxis = d3.axisBottom(xScale);
  let xAxisGroup = viz.append("g")
    .attr("class", "xaxisgroup")
    .attr("transform", "translate(0," + (h - ypadding) + ")")
    ;
  xAxisGroup.call(xAxis);

  let yMax = d3.max(reducedData, function (d) {
    return +d.values;
  })
  let yDomain = [0, yMax];
  let yScale = d3.scaleLinear().domain(yDomain).range([h - ypadding, ypadding]);
  let yAxis = d3.axisLeft(yScale);
  let yAxisGroup = viz.append("g")
    .attr("class", "yaxisgroup")
    .attr("transform", "translate(" + (xpadding / 2) + ",0)")
    ;
  yAxisGroup.call(yAxis);


  let graphGroup = viz.append("g").attr("class", "graphGroup");

  let elementsForPage = graphGroup.selectAll(".datapoint").data(reducedData);

  let enteringElements = elementsForPage.enter();
  let exitingElements = elementsForPage.exit();

  let enteringDataGroups = enteringElements.append("g").classed("datapoint", true)

  enteringDataGroups.selectAll(".datapoint").data(reducedData).enter()
    .append("rect")
    .attr("class", "datapoint")
    .attr("fill", "steelblue")
    .attr("x", function(d) { return xScale(d.person); })
    .attr("width", xScale.bandwidth()-5)
    .attr("y", function(d) { return yScale(+d.values); })
    .attr("height", function(d) { return h - yScale(d.values) - ypadding; })
    ;

}
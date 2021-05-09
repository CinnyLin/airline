myData = {
  Direct:34,
  Indirect:56
}

let color = d3.scaleOrdinal()
  .domain(myData)
  .range(['#98abc5', '#a05d56'])

let w = 500;
let h = 300;
let radius = Math.min(w, h) / 2
let xpadding = 100;
let ypadding = 50;
let viz = d3.select("#container")
  .append("svg")
  .style("width", w)
  .style("height", h)
  .style("outline", "solid black")
  .append("g")
    .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")")
  ;

let pie = d3.pie().value(function(d) {return d.value; })
let data_ready = pie(d3.entries(myData))

viz
  .selectAll('whatever')
  .data(data_ready)
  .enter()
  .append('path')
  .attr('d', d3.arc()
    .innerRadius(0)
    .outerRadius(radius)
  )
  .attr('fill', function(d){ return(color(d.data.key)) })
  .attr("stroke", "black")
  .style("stroke-width", "2px")
  .style("opacity", 0.7)

viz.selectAll('path')
  .on('mouseover', mouseOver)
  .on('mouseout', mouseOut)

function mouseOver(d, i){

    console.log('mouseover!')
    d3.select(this)
        .transition('mouseover').duration(100)
        .attr('opacity', 1)
        .attr('stroke-width', 5)
        .attr('stroke', 'black')
        
    d3.select('#tooltip')
        .style('left', (d3.event.pageX + 10)+ 'px')
        .style('top', (d3.event.pageY - 25) + 'px')
        .style('display', 'inline-block')
        .html(`<strong></strong> ${d.data.key}: ${d.data.value}`)
}

function mouseOut(d, i){
    d3.select('#tooltip')
        .style('display', 'none')

    d3.select(this)
        .transition('mouseout').duration(100)
        .attr('opacity', 0.8)
        .attr('stroke-width', 0)
}
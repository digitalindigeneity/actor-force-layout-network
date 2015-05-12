$( document ).ready(function() { 

  var width = 700,
      height = 800;

  var tooltip = d3.select("#tooltip");

  // var color = d3.scale.category20();

  var force = d3.layout.force()
      .linkStrength(0.5)
      .friction(0.9)
      .linkDistance(40)
      .charge(-150)
      .gravity(0.1)
      .theta(0.8)
      .alpha(0.1)
      .size([width, height]);

  var svg = d3.select("svg")
      .attr("width", width)
      .attr("height", height);

  var borderPath = svg.append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("height", height)
      .attr("width", width)
      .style("stroke", "gray")
      .style("fill", "none")
      .style("stroke-width", "0.9");


  d3.json("data/res.json", function(error, graph) {
    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var link = svg.selectAll(".link")
        .data(graph.links)
      .enter().append("line")
        .attr("class", "link")
        .style("stroke", function(d) { return lineColor(d.linkType) })
        .style("stroke-width", 1.5);

    var node = svg.selectAll(".node")
        .data(graph.nodes)
      .enter().append("circle")
        .attr("class", "node")
        .attr("r", function(d) { return size(d); })
        .style("fill", function(d) { return color(d.nodeType); })
        // .on("click", click)
        .on("mouseover",mouseover)
        .call(force.drag);

    node.append("title")
        .text(function(d) { return d.name; });



    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });
    });
  });

  function mouseover(d){
    tooltip.select("div").remove();
    tooltip
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("background-color","#E6E6E6")

      .html("Name: "        + d.name        + "<br/>" +
            "Description: " + d.description + "<br/>" +
            "Date"          + d.created_date + "<br/>" +
            "Message: "     + d.message     + "<br/>" + 
            "Media Type: "  + d.media_type  + "<br/>" +
            "Media URL: <a href=\"" + d.url +"\" target=\"_newtab\">" + "source</a>"  + "<br/>" + 

            "<br/>" + "DEBUG INFO:" + "<br/>" + 
            "year: "        + d.year + "<br/>" +
            "node type: "   + d.nodeType    + "<br/>" + 
            "node size: "   + d.size    + "<br/>" + 
            "node xid: "    + d.xid         + "<br/>" 
            );

  }
 // Math.sqrt(d.size) * 5 || size(d.nodeType);
  function size(d) {

    switch (d.nodeType) {
      case "likerNode":
        return Math.sqrt(d.size) * 5 || 6;
      case "taggedNode":
        return Math.sqrt(d.size) * 5 || 4;
      case "postNode":
        return Math.sqrt(d.size) * 5 || 4.5;
      case "coreNode":
        return  20;
      case "year":
        return Math.sqrt(d.size) / 5 || 8;
      default:
        return Math.sqrt(d.size) * 5 || 4.5;
    }
  }

  function color(d) {
    switch (d) {
      case "likerNode":
        return "#5C85FF";
      case "taggedNode":
        return "#0099CC";
      case "postNode":
        return "#FF9900";
      case "coreNode":
        return "#999980";
      case "year":
        return "green";
      default:
        return "pink";
    }

  }

  function lineColor(d) {
    switch (d) {
      case "coreLink": 
        return '#999'

      case "likeLink": 
        return '#4C0000'

      case "taggedLink": 
        return '#B84D4D'

      default:
       return '#999'
    }

  }




});

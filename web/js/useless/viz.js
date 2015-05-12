$( document ).ready(function() { 
  var width = 960,
      height = 500,
      nodes,
      links;

  var force = d3.layout.force()
      .linkStrength(0.5)
      .friction(0.9)
      .linkDistance(40)
      .charge(-500)
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
      .style("stroke-width", "1.9");

  var link = svg.selectAll(".link"),
      node = svg.selectAll(".node");

  d3.json("data/miserables.json", function(error, json) {
    nodes = json.nodes;
    links = json.links
    update();
  });

  function update() {

    force
        .nodes(nodes)
        .links(links)
        .start();



    link = svg.selectAll(".link")
        .data(links)
      .enter().append("line")
        .attr("class", "link")

    // update nodes
    node = node.data(nodes, function(d) { return d.id; })
               .style("fill", color);

    // enter nodes
    // node = svg.selectAll(".node")
    //     .data(nodes)
    //   .enter().append("g")
    //     .attr("class", "node")
    //     .call(force.drag);

    // Enter any new nodes.
    node.enter().append("circle")
        .attr("class", "node")
        .attr("cx", function(d) { console.log(d.x);return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", function(d) { return Math.sqrt(d.size) / 10 || 4.5; })
        .style("fill", color)
        // .on("click", click)
        .call(force.drag);



    // node.append("image")
    //     .attr("xlink:href", "https://github.com/favicon.ico")
    //     .attr("x", -8)
    //     .attr("y", -8)
    //     .attr("width", 16)
    //     .attr("height", 16);

    // node.append("circle")
    //       .attr("r", function(d){return d.size})
    //       .attr("style","fill:steelblue")

    // node.append("text")
    //     .attr("dx", 12)
    //     .attr("dy", ".15em")
    //     .text(function(d) { return d.name });
    //     
    //     
    // node.append("svg:text")
    //     .attr("class", "nodetext")
    //     .attr("dx", 12)
    //     .attr("dy", ".35em")
    //     .text(function(d) { return d.name });


    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });



  }


  function color(d) {
    // return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
    switch (d.type) {
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


});

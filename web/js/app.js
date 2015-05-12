$( document ).ready(function() { 

  var width = 500,
      height = 500,
      root,
      likesAndTags;

  var force = d3.layout.force()
      .linkStrength(0.5)
      .friction(0.9)
      .linkDistance(40)
      .charge(-80)
      .gravity(0.1)
      .theta(0.8)
      .alpha(0.1)
      .size([width, height])
      .on("tick", tick);

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

  var link = svg.selectAll(".link"),
      node = svg.selectAll(".node");

  d3.json("data/example3.json", function(json) {
    root = json.posts;
    likesAndTags = json.relations;
    update();
  });

  function update() {
    var nodes = flatten(root),
        links = d3.layout.tree().links(nodes);
        // console.log(links);
        addLikesandTags(likesAndTags, nodes, links);
                // console.log(links);

        // console.log(nodes);
        // newlink = {'source:' nodes[0]
        
        // console.log(nodes);
        // console.log(links);

    // Restart the force layout.
    force
        .nodes(nodes)
        .links(links)
        .start();
    console.log(link);
    // Update the links…
    link = link.data(links, function(d) { 
                                  console.log(d.target.id);
                                  return d.target.id; });

    // Exit any old links.
    link.exit().remove();

    // Enter any new links.
    link.enter().insert("line", ".node")
        .attr("class", "link")
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    // Update the nodes…
    node = node.data(nodes, function(d) { return d.id; }).style("fill", color);

    // Exit any old nodes.
    node.exit().remove();

    // Enter any new nodes.
    node.enter().append("circle")
        .attr("class", "node")
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", function(d) { return Math.sqrt(d.size) / 10 || 4.5; })
        .style("fill", color)
        .on("click", click)
        .call(force.drag);
  }

  function tick() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  }

  // Color leaf nodes orange, and packages white or blue.
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

  // Toggle children on click.
  function click(d) {
    if (!d3.event.defaultPrevented) {
      if (d.children) {
        d._children = d.children;
        d.children = null;
      } else {
        d.children = d._children;
        d._children = null;
      }
      console.log(d.name);
      console.log(d.type);
      console.log(d.id);

      update();
    }
  }

  // Returns a list of all nodes under the root.
  function flatten(root) {
    var nodes = [], i = 0;

    function recurse(node) {
      if (node.children) node.children.forEach(recurse);
      if (!node.id) node.id = ++i;
      nodes.push(node);
    }

    recurse(root);
    return nodes;
  }

  function addLikesandTags(x, nodes,links) {
    var count = 10; 
    for (var i = x.length - 1; i >= 0; i--) {
      x[i].id = count+1;
      nodes.push(x[i]);

      if (x[i].relations) {
        for (var j = x[i].relations.length - 1; j >= 0; j--) {
          for (var k = nodes.length - 1; k >= 0; k--) {
              if (nodes[k].id == x[i].relations[j]) {
                var newLink;
                newLink = {'source': nodes[k], 'target': x[i]}
                // console.log("pusshin");
                // console.log(newLink);

                links.push(newLink);
              };
          };

        };
      }

    };
    console.log(links);


  }

});

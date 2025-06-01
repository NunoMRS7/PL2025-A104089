function renderTree(treeData) {
    const width = window.innerWidth;
    const height = window.innerHeight - 200;
  
    const svg = d3.select("#tree-container").append("svg")
      .attr("width", width)
      .attr("height", height);
  
    const g = svg.append("g");
  
    svg.call(
      d3.zoom().on("zoom", (event) => {
        g.attr("transform", event.transform);
      })
    );
  
    const root = d3.hierarchy(treeData);
    const treeLayout = d3.tree().size([height, width - 160]);
    treeLayout(root);
  
    // Draw links
    g.selectAll(".link")
      .data(root.links())
      .join("path")
      .attr("class", "link")
      .attr("d", d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x)
      );
  
    // Draw nodes
    const node = g.selectAll(".node")
      .data(root.descendants())
      .join("g")
      .attr("class", "node")
      .attr("transform", d => `translate(${d.y},${d.x})`)
      .on("click", (event, d) => {
        if (d.children) {
          d._children = d.children;
          d.children = null;
        } else {
          d.children = d._children;
          d._children = null;
        }
        update(root);
      });
  
    node.append("circle")
      .attr("r", 4);
  
    node.append("text")
      .attr("dy", 3)
      .attr("x", d => d.children ? -8 : 8)
      .style("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name);
  
    function update(source) {
      treeLayout(root);
  
      // Update links
      g.selectAll(".link")
        .data(root.links())
        .join("path")
        .attr("class", "link")
        .attr("d", d3.linkHorizontal()
            .x(d => d.y)
            .y(d => d.x)
        );
  
      // Update nodes
      const nodes = g.selectAll(".node")
        .data(root.descendants())
        .join("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.y},${d.x})`);
  
      nodes.selectAll("circle").attr("r", 4);
  
      nodes.selectAll("text")
        .attr("dy", 3)
        .attr("x", d => d.children ? -8 : 8)
        .style("text-anchor", d => d.children ? "end" : "start")
        .text(d => d.data.name);
    }
  }
  
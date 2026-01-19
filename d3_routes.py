"""
Flask routes for D3.js treemap visualization
"""

from flask import render_template_string, request
import json
import csv
from pathlib import Path

def load_csv_to_dict(nodes_file, edges_file):
    """Convert CSV files to hierarchical format"""
    nodes_dict = {}
    
    # Load nodes from CSV
    with open(nodes_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes_dict[row['id']] = {
                'id': row['id'],
                'label': row['label'],
                'color': row['color'],
                'title': row['title'],
                'level': int(row['level'])
            }
    
    # Load edges and build hierarchy
    edges = []
    with open(edges_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append({
                'from': row['from'],
                'to': row['to'],
                'label': row['label'],
                'type': row.get('type', 'default')
            })
    
    return nodes_dict, edges

def build_hierarchy(nodes_dict, edges):
    """Build hierarchical tree structure from nodes and edges"""
    # Build parent-child map
    parent_map = {}
    child_map = {}
    
    for edge in edges:
        parent = edge['from']
        child = edge['to']
        if parent not in parent_map:
            parent_map[parent] = []
        parent_map[parent].append(child)
        child_map[child] = parent
    
    # Find root nodes (those with no parent)
    all_nodes = set(nodes_dict.keys())
    root_nodes = all_nodes - set(child_map.keys())
    
    # Build tree recursively
    def build_node(node_id):
        node_data = nodes_dict[node_id]
        children = parent_map.get(node_id, [])
        
        tree_node = {
            'name': node_data['label'],
            'id': node_id,
            'color': node_data['color'],
            'level': node_data['level'],
            'value': 1
        }
        
        if children:
            tree_node['children'] = [build_node(child_id) for child_id in children]
        
        return tree_node
    
    # Build complete hierarchy
    roots = [build_node(rid) for rid in sorted(root_nodes)]
    
    # If multiple roots, wrap in a virtual root
    if len(roots) > 1:
        return {'name': 'Infrastructure', 'children': roots, 'id': 'root', 'color': '#ffffff', 'level': -1}
    else:
        return roots[0] if roots else {'name': 'Empty', 'children': [], 'id': 'root', 'color': '#ffffff'}

def get_treemap_html():
    """Get D3.js treemap visualization HTML"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Infrastructure Treemap</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f5f5f5;
                padding: 20px;
            }
            .header {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 20px;
                border-radius: 4px;
                margin-bottom: 20px;
                text-align: center;
            }
            .header h1 {
                font-size: 28px;
                font-weight: 300;
                letter-spacing: 1px;
                margin: 0;
            }
            .container {
                background: white;
                border-radius: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            #treemap {
                width: 100%;
                height: 900px;
            }
            .node {
                overflow: hidden;
                position: absolute;
                cursor: pointer;
                border: 2px solid rgba(0,0,0,0.1);
                box-sizing: border-box;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 8px;
                font-weight: bold;
                color: white;
                font-size: 12px;
                transition: all 0.2s ease;
            }
            .node:hover {
                border: 2px solid rgba(0,0,0,0.3);
                filter: brightness(1.1);
            }
            .node-label {
                pointer-events: none;
                text-shadow: 0 1px 2px rgba(0,0,0,0.3);
            }
            .legend {
                padding: 15px;
                background-color: #ecf0f1;
                border-top: 1px solid #bdc3c7;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Infrastructure Treemap - Nested View</h1>
        </div>
        <div class="container">
            <div id="treemap"></div>
            <div class="legend">
                <strong>How to read:</strong> Larger boxes contain smaller boxes. 
                Service Groups contain Services, which run on Hosts, which expose Ports, showing Status.
            </div>
        </div>

        <script>
            async function loadData() {
                const response = await fetch('/api/treemap-data?type=' + new URLSearchParams(window.location.search).get('type'));
                return await response.json();
            }

            async function render() {
                const data = await loadData();
                
                const container = document.getElementById('treemap');
                const width = container.offsetWidth;
                const height = 900;
                
                // Create hierarchy
                const hierarchy = d3.hierarchy(data)
                    .sum(d => 1)
                    .sort((a, b) => b.value - a.value);
                
                // Create treemap layout
                const treemap = d3.treemap()
                    .size([width, height])
                    .paddingTop(0)
                    .paddingRight(4)
                    .paddingBottom(4)
                    .paddingLeft(4)
                    .round(true);
                
                treemap(hierarchy);
                
                // Remove existing nodes
                container.innerHTML = '';
                
                // Create nodes
                hierarchy.leaves().forEach(node => {
                    const div = document.createElement('div');
                    div.className = 'node';
                    div.style.left = node.x0 + 'px';
                    div.style.top = node.y0 + 'px';
                    div.style.width = (node.x1 - node.x0) + 'px';
                    div.style.height = (node.y1 - node.y0) + 'px';
                    div.style.backgroundColor = node.data.color;
                    div.title = node.data.id;
                    
                    // Calculate font size based on box size
                    const fontSize = Math.max(10, Math.min(14, (node.x1 - node.x0) / 10));
                    
                    const label = document.createElement('div');
                    label.className = 'node-label';
                    label.style.fontSize = fontSize + 'px';
                    label.textContent = node.data.name;
                    
                    div.appendChild(label);
                    container.appendChild(div);
                });
            }
            
            render();
            window.addEventListener('resize', render);
        </script>
    </body>
    </html>
    '''

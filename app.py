"""
Flask app to serve hierarchical visualizations with configurable data
Supports: family tree, infrastructure topology, organizational charts, etc.
Data input: JSON or CSV format
"""

import json
import csv
from pathlib import Path
from flask import Flask, request, jsonify
from pyvis.network import Network

app = Flask(__name__)

def load_csv_to_dict(nodes_file, edges_file):
    """Convert CSV files to the JSON format used by the app"""
    nodes = []
    edges = []
    
    # Load nodes from CSV
    with open(nodes_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            node = {
                'id': row['id'],
                'label': row['label'],
                'color': row['color'],
                'size': int(row['size']),
                'title': row['title'],
                'level': int(row['level']),
                'font': {
                    'size': 14 if int(row['level']) == 0 else 12,
                    'color': row.get('font_color', 'white')
                }
            }
            nodes.append(node)
    
    # Load edges from CSV
    with open(edges_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edge = {
                'from': row['from'],
                'to': row['to'],
                'label': row['label'],
                'color': row['color'],
                'type': row.get('type', 'default')
            }
            edges.append(edge)
    
    return {'nodes': nodes, 'edges': edges}

def load_tree_data(data_file='family_tree_data.json'):
    """Load nodes and edges from JSON file or CSV pair"""
    # Check if CSV files exist
    csv_nodes = data_file.replace('.json', '_nodes.csv')
    csv_edges = data_file.replace('.json', '_edges.csv')
    
    if Path(csv_nodes).exists() and Path(csv_edges).exists():
        return load_csv_to_dict(csv_nodes, csv_edges)
    else:
        # Fall back to JSON
        with open(data_file, 'r') as f:
            return json.load(f)

def build_hierarchy_tree(nodes, edges):
    """Build hierarchical tree from nodes and edges"""
    # Create nodes dict
    nodes_dict = {n['id']: n for n in nodes}
    
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
    
    # Find root nodes
    all_node_ids = set(nodes_dict.keys())
    root_ids = all_node_ids - set(child_map.keys())
    
    def build_node_tree(node_id):
        node_data = nodes_dict[node_id]
        children = parent_map.get(node_id, [])
        
        tree = {
            'name': node_data['label'],
            'id': node_id,
            'color': node_data['color'],
            'level': node_data['level'],
            'value': 1
        }
        
        if children:
            tree['children'] = [build_node_tree(cid) for cid in children]
        
        return tree
    
    roots = [build_node_tree(rid) for rid in sorted(root_ids)]
    
    if len(roots) > 1:
        return {
            'name': 'Root',
            'id': 'root',
            'color': '#ffffff',
            'level': -1,
            'children': roots
        }
    
    return roots[0] if roots else {'name': 'Empty', 'id': 'root', 'color': '#ffffff', 'level': -1}

@app.route('/api/treemap-data')
def treemap_data():
    """API endpoint for treemap D3 visualization"""
    viz_type = request.args.get('type', 'family')
    data_file = 'infrastructure_data.json' if viz_type == 'infrastructure' else 'family_tree_data.json'
    
    data = load_tree_data(data_file)
    hierarchy = build_hierarchy_tree(data['nodes'], data['edges'])
    
    return jsonify(hierarchy)

def create_hierarchy_tree(data_file='family_tree_data.json'):
    """Create and return a hierarchy tree from data file"""
    net = Network(height='900px', width='100%', directed=True)
    
    # Disable physics for clean hierarchy
    net.toggle_physics(False)
    
    # Load data
    data = load_tree_data(data_file)
    
    # Build parent-child relationships map
    parent_map = {}
    for edge in data['edges']:
        parent = edge['from']
        child = edge['to']
        if parent not in parent_map:
            parent_map[parent] = []
        parent_map[parent].append(child)
    
    # Add nodes from data
    for node in data['nodes']:
        label = node['label']
        level = node['level']
        
        # Adjust width/height based on level for visual containment
        if level == 0:  # Service groups - largest
            width = 150
            height = 70
        elif level == 1:  # Services - large
            width = 130
            height = 60
        elif level == 2:  # Hosts - medium
            width = 120
            height = 60
        elif level == 3:  # Ports - small
            width = 90
            height = 45
        else:  # Status - smallest
            width = 80
            height = 40
        
        node_config = {
            'label': label,
            'shape': 'box',
            'color': {
                'background': node['color'],
                'border': node['color'],
                'highlight': {
                    'background': node['color'],
                    'border': '#888888'
                },
                'hover': {
                    'background': node['color'],
                    'border': '#888888'
                }
            },
            'title': node['title'],
            'level': node['level'],
            'borderWidth': 2,
            'borderWidthSelected': 3,
            'widthConstraint': {
                'minimum': width,
                'maximum': width
            },
            'heightConstraint': {
                'minimum': height,
                'maximum': height
            },
            'margin': {
                'top': 8,
                'bottom': 8,
                'left': 12,
                'right': 12
            },
            'font': {
                'size': 13,
                'color': '#ffffff',
                'face': 'Arial',
                'align': 'center',
                'multi': True,
                'bold': {
                    'mod': 'bold'
                }
            },
            'physics': False
        }
        
        net.add_node(node['id'], **node_config)
    
    # Add edges from data
    for edge in data['edges']:
        edge_type = edge.get('type', 'default')
        
        edge_config = {
            'label': edge['label'],
            'color': edge['color'],
            'arrows': 'to'
        }
        
        if edge_type == 'spouse':
            edge_config['arrows'] = 'to, from'
            edge_config['smooth'] = True
        elif edge_type == 'sibling':
            edge_config['arrows'] = 'to, from'
            edge_config['dashes'] = True
        
        net.add_edge(edge['from'], edge['to'], **edge_config)
    
    # Configure hierarchical layout
    options = {
        "physics": {
            "enabled": False
        },
        "layout": {
            "hierarchical": {
                "enabled": True,
                "levelSeparation": 200,
                "nodeSpacing": 150,
                "direction": "UD",
                "sortMethod": "directed"
            }
        },
        "edges": {
            "smooth": {
                "type": "cubicBezier",
                "forceDirection": "vertical"
            },
            "font": {
                "size": 10,
                "color": "#666",
                "align": "middle"
            },
            "widthConstraint": {
                "maximum": 90
            }
        },
        "nodes": {
            "shape": "box",
            "margin": {
                "top": 10,
                "bottom": 10,
                "left": 15,
                "right": 15
            },
            "font": {
                "size": 14,
                "color": "white",
                "face": "Arial",
                "align": "center",
                "multi": False,
                "bold": {
                    "mod": "bold"
                }
            },
            "borderWidth": 1,
            "borderWidthSelected": 2
        },
        "interaction": {
            "navigationButtons": True,
            "keyboard": True,
            "zoomView": True
        }
    }
    
    net.set_options(str(options).replace("'", '"').replace("True", "true").replace("False", "false"))
    
    return net

def create_nodegraph(data_file='nodegraph_data.json'):
    """Create a Grafana-style node graph"""
    net = Network(height='900px', width='100%', directed=True)
    
    # Enable physics for force-directed layout
    net.toggle_physics(True)
    
    # Load data
    data = load_tree_data(data_file)
    
    # Status colors for health indicators
    status_colors = {
        'healthy': '#22c55e',
        'warning': '#f59e0b',
        'critical': '#ef4444',
        'unknown': '#9ca3af'
    }
    
    # Shape mapping for PyVis
    shape_map = {
        'star': 'star',
        'box': 'box',
        'diamond': 'diamond',
        'cylinder': 'ellipse'  # PyVis doesn't have cylinder, use ellipse
    }
    
    # Add nodes
    for node in data['nodes']:
        label = node['label']
        status = node.get('status', 'unknown')
        error_rate = float(node.get('error_rate', 0))
        latency = float(node.get('latency', 0))
        throughput = float(node.get('throughput', 0))
        
        # Build node title with metrics
        metrics_title = f"<b>{label}</b><br>"
        metrics_title += f"Status: {status.upper()}<br>"
        metrics_title += f"Error Rate: {error_rate}%<br>"
        metrics_title += f"Latency: {latency}ms<br>"
        metrics_title += f"Throughput: {throughput} RPS"
        
        # Use status color if available, otherwise use node color
        color = node.get('color', '#4A90E2')
        if status in status_colors:
            # Mix status indicator with node color
            color = status_colors[status]
        
        node_config = {
            'label': label,
            'shape': shape_map.get(node.get('shape', 'star'), 'star'),
            'color': {
                'background': color,
                'border': color,
                'highlight': {
                    'background': color,
                    'border': '#ffffff'
                },
                'hover': {
                    'background': color,
                    'border': '#ffffff'
                }
            },
            'title': metrics_title,
            'size': int(node.get('size', 40)),
            'borderWidth': 2,
            'borderWidthSelected': 4,
            'font': {
                'size': 12,
                'color': '#ffffff',
                'face': 'Arial',
                'align': 'center',
                'bold': {
                    'mod': 'bold'
                }
            },
            'scaling': {
                'label': {
                    'enabled': True,
                    'min': 10,
                    'max': 14
                }
            }
        }
        
        net.add_node(node['id'], **node_config)
    
    # Add edges with metrics labels
    for edge in data['edges']:
        latency = float(edge.get('latency_ms', 0))
        error_rate = float(edge.get('error_rate', 0))
        throughput = float(edge.get('throughput_rps', 0))
        edge_status = edge.get('status', 'unknown')
        
        # Create edge label with metrics
        label = f"↓ {throughput} RPS"
        
        # Color based on status
        edge_color = '#22c55e'  # healthy green
        if edge_status == 'warning':
            edge_color = '#f59e0b'
        elif edge_status == 'critical':
            edge_color = '#ef4444'
        
        # Width based on throughput (normalized)
        width = 1 + (throughput / 2000 * 3)  # Range 1-4
        
        edge_config = {
            'label': label,
            'color': {
                'color': edge_color,
                'highlight': '#ffffff',
                'hover': '#ffffff'
            },
            'arrows': 'to',
            'width': width,
            'font': {
                'size': 10,
                'color': edge_color,
                'align': 'middle',
                'background': {
                    'enabled': True,
                    'color': 'rgba(255, 255, 255, 0.8)'
                }
            },
            'smooth': {
                'type': 'continuous'
            },
            'title': f"Latency: {latency}ms\nError Rate: {error_rate}%\nThroughput: {throughput} RPS"
        }
        
        net.add_edge(edge['from'], edge['to'], **edge_config)
    
    # Configure physics and layout for Grafana-like appearance
    options = {
        "physics": {
            "enabled": True,
            "barnesHut": {
                "gravitationalConstant": -30000,
                "centralGravity": 0.3,
                "springLength": 200,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 0.1
            },
            "solver": "barnesHut",
            "timestep": 0.5,
            "stabilization": {
                "iterations": 200
            }
        },
        "edges": {
            "smooth": {
                "type": "continuous",
                "roundness": 0.5
            },
            "font": {
                "size": 10,
                "color": "#666",
                "align": "middle",
                "background": {
                    "enabled": True,
                    "color": "rgba(255, 255, 255, 0.8)",
                    "size": 0.8
                }
            },
            "widthConstraint": {
                "maximum": 90
            }
        },
        "nodes": {
            "font": {
                "size": 12,
                "color": "white",
                "face": "Arial",
                "align": "center",
                "bold": {
                    "mod": "bold"
                }
            },
            "borderWidth": 2,
            "borderWidthSelected": 4
        },
        "interaction": {
            "navigationButtons": True,
            "keyboard": True,
            "zoomView": True,
            "hover": True
        }
    }
    
    net.set_options(str(options).replace("'", '"').replace("True", "true").replace("False", "false"))
    
    return net

@app.route('/nodegraph')
def nodegraph():
    """Render the Grafana-style node graph"""
    net = create_nodegraph('nodegraph_data.json')
    html_string = net.generate_html()
    
    # Add professional styling
    professional_css = """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        #mynetwork {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 300;
            letter-spacing: 1px;
        }
        .header p {
            margin: 8px 0 0 0;
            font-size: 12px;
            opacity: 0.9;
        }
        .container {
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }
        .legend {
            margin-bottom: 15px;
            padding: 12px 15px;
            background-color: #ecf0f1;
            border-radius: 4px;
            font-size: 11px;
            border-left: 4px solid #34495e;
        }
        .legend-item {
            display: inline-block;
            margin-right: 20px;
        }
        .legend-color {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 2px;
            margin-right: 6px;
            vertical-align: middle;
        }
        .nav-links {
            text-align: center;
            margin-bottom: 10px;
            font-size: 12px;
        }
        .nav-links a {
            color: #34495e;
            text-decoration: none;
            margin: 0 10px;
            padding: 6px 12px;
            border-radius: 3px;
            background-color: white;
            border: 1px solid #bdc3c7;
            display: inline-block;
        }
        .nav-links a:hover {
            background-color: #34495e;
            color: white;
        }
        .nav-links a.active {
            background-color: #34495e;
            color: white;
        }
        .info {
            background-color: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 12px 15px;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 11px;
        }
    </style>
    """
    
    legend_html = '''
    <div class="legend">
        <div class="legend-item"><span class="legend-color" style="background-color: #22c55e;"></span> Healthy</div>
        <div class="legend-item"><span class="legend-color" style="background-color: #f59e0b;"></span> Warning</div>
        <div class="legend-item"><span class="legend-color" style="background-color: #ef4444;"></span> Critical</div>
        <div class="legend-item" style="margin-left: 20px; font-style: italic;">Node size represents importance | Edge thickness represents throughput</div>
    </div>
    '''
    
    nav_links = '''
    <div class="nav-links">
        <a href="/?type=family">Family Tree</a>
        <a href="/?type=infrastructure">Infrastructure (PyVis)</a>
        <a href="/treemap?type=infrastructure">Infrastructure (Treemap)</a>
        <a href="/nodegraph" class="active">Node Graph</a>
    </div>
    '''
    
    info_box = '''
    <div class="info">
        <strong>ℹ️ Node Graph Guide:</strong> Hover over nodes for detailed metrics. Edge labels show throughput (RPS). 
        Thickness of edges indicates data flow volume. Color indicates health status (green = healthy, orange = warning, red = critical).
    </div>
    '''
    
    # Insert header and styling
    html_string = html_string.replace(
        '<body>',
        '<body>' + professional_css + 
        '<div class="header"><h1>Grafana Node Graph Mimic</h1><p>Service Dependencies with Metrics</p></div>'
    )
    html_string = html_string.replace(
        '<center>\n<h1></h1>\n</center>',
        '<div class="container">' + nav_links + info_box + legend_html
    )
    
    # Add auto-fit and stabilization script at the end
    fit_script = """
    <script type="text/javascript">
        // Auto-fit and stabilize
        setTimeout(function() {
            if (typeof network !== 'undefined') {
                network.fit({
                    animation: {
                        duration: 1000,
                        easingFunction: 'easeInOutQuad'
                    }
                });
            }
        }, 1500);
    </script>
    """
    html_string = html_string.replace('</body>', fit_script + '</div></body>')
    
    return html_string

@app.route('/')
def index():
    """Render the visualization"""
    # Determine which data file to use
    viz_type = request.args.get('type', 'family')
    
    if viz_type == 'infrastructure':
        data_file = 'infrastructure_data.json'
        title = 'Infrastructure Topology'
        legend = (
            '<strong>Legend:</strong> ' +
            '<span style="color: #1a1a2e; font-weight: bold;">■</span> Service Group | ' +
            '<span style="color: #0f3460; font-weight: bold;">■</span> Service | ' +
            '<span style="color: #16a34a; font-weight: bold;">■</span> Host | ' +
            '<span style="color: #dc2626; font-weight: bold;">■</span> Port | ' +
            '<span style="color: #22c55e; font-weight: bold;">■</span> Healthy | ' +
            '<span style="color: #f59e0b; font-weight: bold;">■</span> Warning'
        )
    else:
        data_file = 'family_tree_data.json'
        title = 'Family Hierarchy'
        legend = (
            '<strong>Color Legend:</strong> ' +
            '<span style="color: #2B5A75; font-weight: bold;">■</span> Male | ' +
            '<span style="color: #6B4C5C; font-weight: bold;">■</span> Female'
        )
    
    net = create_hierarchy_tree(data_file)
    html_string = net.generate_html()
    
    # Add professional styling
    professional_css = """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        #mynetwork {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 300;
            letter-spacing: 1px;
        }
        .header p {
            margin: 8px 0 0 0;
            font-size: 12px;
            opacity: 0.9;
        }
        .container {
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .legend {
            margin-bottom: 15px;
            padding: 12px 15px;
            background-color: #ecf0f1;
            border-radius: 4px;
            font-size: 12px;
            border-left: 4px solid #34495e;
        }
        .nav-links {
            text-align: center;
            margin-bottom: 10px;
            font-size: 12px;
        }
        .nav-links a {
            color: #34495e;
            text-decoration: none;
            margin: 0 15px;
            padding: 5px 10px;
            border-radius: 3px;
            background-color: white;
            border: 1px solid #bdc3c7;
        }
        .nav-links a:hover {
            background-color: #34495e;
            color: white;
        }
        .nav-links a.active {
            background-color: #34495e;
            color: white;
        }
    </style>
    """
    
    # Determine active link
    family_active = ' class="active"' if viz_type == 'family' else ''
    infra_active = ' class="active"' if viz_type == 'infrastructure' else ''
    
    nav_links = (
        '<div class="nav-links">' +
        f'<a href="/?type=family"{family_active}>Family Tree</a>' +
        f'<a href="/?type=infrastructure"{infra_active}>Infrastructure (PyVis)</a>' +
        f'<a href="/treemap?type={viz_type}">Infrastructure (Treemap)</a>' +
        f'<a href="/nodegraph">Node Graph</a>' +
        '</div>'
    )
    
    # Insert header and styling
    html_string = html_string.replace(
        '<body>',
        '<body>' + professional_css + 
        '<div class="header"><h1>' + title + '</h1></div>'
    )
    html_string = html_string.replace(
        '<center>\n<h1></h1>\n</center>',
        '<div class="container">' + nav_links + 
        '<div class="legend">' + legend + '</div>'
    )
    
    # Add auto-fit script at the end before closing body
    fit_script = """
    <script type="text/javascript">
        // Auto-fit the graph to show all nodes when page loads
        setTimeout(function() {
            if (typeof network !== 'undefined') {
                network.fit({
                    animation: {
                        duration: 500,
                        easingFunction: 'easeInOutQuad'
                    }
                });
            }
        }, 500);
    </script>
    """
    html_string = html_string.replace('</body>', fit_script + '</div></body>')
    
    return html_string

@app.route('/treemap')
def treemap():
    """D3.js Treemap visualization"""
    return '''<!DOCTYPE html>
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
            .nav-links {
                text-align: center;
                margin-bottom: 15px;
                font-size: 12px;
            }
            .nav-links a {
                color: #34495e;
                text-decoration: none;
                margin: 0 10px;
                padding: 5px 10px;
                border-radius: 3px;
                background-color: white;
                border: 1px solid #bdc3c7;
                display: inline-block;
            }
            .nav-links a:hover, .nav-links a.active {
                background-color: #34495e;
                color: white;
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
                position: relative;
            }
            .node {
                overflow: hidden;
                position: absolute;
                cursor: pointer;
                border: 2px solid rgba(0,0,0,0.2);
                box-sizing: border-box;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 6px;
                font-weight: bold;
                color: white;
                font-size: 11px;
                transition: all 0.2s ease;
            }
            .node:hover {
                border: 2px solid rgba(0,0,0,0.4);
                filter: brightness(1.1);
                z-index: 100;
            }
            .node-label {
                pointer-events: none;
                text-shadow: 0 1px 2px rgba(0,0,0,0.4);
                word-wrap: break-word;
                line-height: 1.2;
            }
            .legend {
                padding: 15px 20px;
                background-color: #ecf0f1;
                border-top: 1px solid #bdc3c7;
                font-size: 11px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Infrastructure Treemap - Nested Hierarchy</h1>
        </div>
        <div class="nav-links">
            <a href="/?type=infrastructure">Back to PyVis</a>
        </div>
        <div class="container">
            <div id="treemap"></div>
            <div class="legend">
                <strong>Visualization Guide:</strong> Larger boxes contain smaller boxes. 
                Service Groups → Services → Hosts (ports nested inside) → Status.
                Hover over any box to highlight it.
            </div>
        </div>

        <script>
            async function loadData() {
                const type = new URLSearchParams(window.location.search).get('type') || 'infrastructure';
                const response = await fetch('/api/treemap-data?type=' + type);
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
                
                // Create treemap layout with padding
                const treemap = d3.treemap()
                    .size([width, height])
                    .paddingTop(2)
                    .paddingRight(2)
                    .paddingBottom(2)
                    .paddingLeft(2)
                    .round(true);
                
                treemap(hierarchy);
                
                // Clear container
                container.innerHTML = '';
                
                // Render all nodes (not just leaves, to show full hierarchy)
                function renderNodes(node) {
                    if (node.x1 - node.x0 > 20 && node.y1 - node.y0 > 20) {
                        const div = document.createElement('div');
                        div.className = 'node';
                        div.style.left = node.x0 + 'px';
                        div.style.top = node.y0 + 'px';
                        div.style.width = (node.x1 - node.x0) + 'px';
                        div.style.height = (node.y1 - node.y0) + 'px';
                        div.style.backgroundColor = node.data.color;
                        div.title = node.data.id;
                        div.dataset.id = node.data.id;
                        
                        // Calculate font size
                        const fontSize = Math.max(9, Math.min(13, (node.x1 - node.x0) / 12));
                        
                        const label = document.createElement('div');
                        label.className = 'node-label';
                        label.style.fontSize = fontSize + 'px';
                        label.textContent = node.data.name;
                        
                        div.appendChild(label);
                        container.appendChild(div);
                    }
                    
                    if (node.children) {
                        node.children.forEach(renderNodes);
                    }
                }
                
                renderNodes(hierarchy);
            }
            
            render();
            window.addEventListener('resize', render);
        </script>
    </body>
    </html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

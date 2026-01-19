# Hierarchical Visualization - Kharkai

Interactive hierarchical visualizations supporting family trees, infrastructure topology, organizational charts, and more.

## Features

- 📊 Multi-layer hierarchical visualization
- 🎨 Professional styling with customizable colors
- 🔄 Switch between Family Tree and Infrastructure views
- 📥 Support for JSON and CSV input formats
- 🎯 Auto-fit visualization to view all nodes
- 🖱️ Interactive navigation and zoom controls

## Quick Start

### Using Docker

```bash
docker-compose up
```

Then open `http://localhost:5000` in your browser.

## Data Input Formats

### JSON Format

Define nodes and edges in a single JSON file:

```json
{
  "nodes": [
    {
      "id": "node1",
      "label": "Node Label",
      "color": "#FF0000",
      "size": 30,
      "title": "Tooltip text",
      "level": 0,
      "font": {"size": 14, "color": "white"}
    }
  ],
  "edges": [
    {
      "from": "node1",
      "to": "node2",
      "label": "relationship",
      "color": "#666666",
      "type": "parent"
    }
  ]
}
```

### CSV Format (Recommended for Large Datasets)

#### Nodes CSV (`*_nodes.csv`)

```csv
id,label,color,size,title,level,font_color
sg1,Web Services,#1a1a2e,40,Service Group: Web Layer,0,white
svc1,API Gateway,#0f3460,35,Service: API Gateway,1,white
```

**Columns:**
- `id`: Unique identifier
- `label`: Display name
- `color`: Hex color code
- `size`: Node size (20-50)
- `title`: Tooltip text
- `level`: Hierarchy level (0=top, 4=bottom)
- `font_color`: Text color

#### Edges CSV (`*_edges.csv`)

```csv
from,to,label,color,type
sg1,svc1,contains,#666666,parent
svc1,host1,runs on,#666666,parent
port1,status1,status,#22c55e,status
```

**Columns:**
- `from`: Source node ID
- `to`: Target node ID
- `label`: Edge label
- `color`: Hex color code
- `type`: Relationship type (`parent`, `sibling`, `spouse`, `status`)

## Usage

### View Different Visualizations

- **Family Tree**: `http://localhost:5000/?type=family`
- **Infrastructure**: `http://localhost:5000/?type=infrastructure`

### Using Your Own Data

1. **Option A - JSON:**
   - Edit `family_tree_data.json` or `infrastructure_data.json`
   - Restart container: `docker-compose restart`

2. **Option B - CSV (Preferred):**
   - Edit `infrastructure_nodes.csv` and `infrastructure_edges.csv`
   - Changes reload automatically (no restart needed!)
   - The app detects `*_nodes.csv` and `*_edges.csv` files and uses them

## Example: Add Infrastructure Components

### Add a Node to `infrastructure_nodes.csv`:
```csv
api-gateway-01,API Gateway Instance,#4CAF50,30,Host: api-gateway-01,2,white
```

### Add an Edge to `infrastructure_edges.csv`:
```csv
svc1,api-gateway-01,deployed on,#666666,parent
```

## Color Reference

### Infrastructure Layers
- **Service Groups**: `#1a1a2e` (Dark gray)
- **Services**: `#0f3460` (Dark blue)
- **Hosts**: `#16a34a` (Green)
- **Ports**: `#dc2626` (Red)
- **Status - Healthy**: `#22c55e` (Bright green)
- **Status - Warning**: `#f59e0b` (Orange)
- **Status - Critical**: `#ef4444` (Red)

### Family Tree
- **Male**: `#2B5A75` (Blue)
- **Female**: `#6B4C5C` (Purple)

## File Structure

```
/workspaces/kharkai/
├── app.py                           # Flask application
├── family_tree_data.json           # Family tree (JSON format)
├── infrastructure_data.json        # Infrastructure (JSON format)
├── infrastructure_nodes.csv        # Infrastructure nodes (CSV)
├── infrastructure_edges.csv        # Infrastructure edges (CSV)
├── Dockerfile                      # Container configuration
├── docker-compose.yml              # Docker Compose setup
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Development

### Local Setup (without Docker)

```bash
pip install -r requirements.txt
python app.py
```

### Modify Visualization Settings

Edit the Python configuration in `app.py`:
- Change layout direction: `"direction": "UD"` (Up-Down) or `"LR"` (Left-Right)
- Adjust spacing: `"levelSeparation": 200`, `"nodeSpacing": 150`
- Customize colors in your data files

## Advanced Features

### Relationship Types in CSV

Define edge types using the `type` column:
- `parent`: Parent-child relationships (solid arrows)
- `sibling`: Sibling relationships (dashed lines)
- `spouse`: Spouse relationships (bidirectional curved)
- `status`: Status indicators

### Custom Fonts

Add font customization in nodes:
```json
"font": {
  "size": 14,
  "color": "white",
  "bold": {"mod": "bold"}
}
```

## Performance

- Tested with 200+ nodes and 300+ edges
- Auto-fit works smoothly with deep hierarchies (5+ levels)
- CSV format recommended for datasets with 50+ nodes

## License

MIT

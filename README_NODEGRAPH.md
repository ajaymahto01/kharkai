# Grafana Node Graph Mimic - PyVis Implementation

A comprehensive microservices visualization system with multiple interactive views, including a Grafana-style Node Graph with service dependencies, metrics, and health status indicators.

## Features

### 🌐 Node Graph View (`/nodegraph`)
Interactive force-directed graph visualization mimicking Grafana's Node Graph panel:
- **Service Nodes**: Visualized with different shapes (stars, boxes, diamonds, ellipses)
- **Health Status**: Color-coded nodes (green = healthy, orange = warning, red = critical)
- **Metrics Display**: Hover over nodes to see detailed metrics:
  - Error Rate (%)
  - Latency (ms)
  - Throughput (RPS - Requests Per Second)
  - Service Status
- **Connection Metrics**: Edge labels show throughput, thickness represents data volume
- **Interactive Physics**: Force-directed layout for organic, easy-to-understand topology
- **Zoom & Pan**: Full interaction support with physics simulation stabilization

### 📊 Additional Views
- **Family Tree** (`/?type=family`): 4-generation hierarchical family structure
- **Infrastructure PyVis** (`/?type=infrastructure`): Hierarchical infrastructure topology
- **Infrastructure Treemap** (`/treemap?type=infrastructure`): D3.js nested box visualization

## Microservices Topology

The default Node Graph visualizes a complete microservices architecture:

```
├── API Gateway (Primary entry point)
│   ├── Frontend Service
│   ├── Auth Service (⚠️ Warning status)
│   ├── User Service
│   ├── Product Service
│   └── Order Service (⚠️ Warning status)
├── Backend Services
│   ├── User Service → Cache, Database
│   ├── Product Service → Database, Elasticsearch (🔴 Critical)
│   ├── Order Service → Database, Message Queue
│   └── Auth Service → Database
├── Infrastructure
│   ├── Redis Cache (High throughput: 2000 RPS)
│   ├── PostgreSQL Primary
│   ├── PostgreSQL Replica
│   ├── Elasticsearch (Issues: 5.2% error rate)
│   └── Message Queue (RabbitMQ-style)
└── Monitoring (Prometheus/Grafana)
```

## Data Format

### CSV Format (Nodes)
```csv
id,label,shape,color,size,status,error_rate,latency,throughput
api-gateway,API Gateway,star,#4A90E2,50,healthy,0.1,45,1200
auth-service,Auth Service,star,#F5A623,45,warning,1.5,380,600
```

**Columns:**
- `id`: Unique identifier for the service
- `label`: Display name
- `shape`: Node shape (`star`, `box`, `diamond`, `cylinder`)
- `color`: Hex color code
- `size`: Node size (30-50 recommended)
- `status`: Health status (`healthy`, `warning`, `critical`)
- `error_rate`: Error percentage
- `latency`: Response time in milliseconds
- `throughput`: Requests per second

### CSV Format (Edges)
```csv
from,to,latency_ms,error_rate,throughput_rps,status
api-gateway,frontend,45,0.1,1200,healthy
order-service,db-primary,15,0,200,healthy
```

**Columns:**
- `from`: Source service ID
- `to`: Destination service ID
- `latency_ms`: Connection latency
- `error_rate`: Error percentage on connection
- `throughput_rps`: Requests per second flowing through connection
- `status`: Connection health status

### JSON Format

Equivalent data structure with richer metadata:
```json
{
  "nodes": [
    {
      "id": "api-gateway",
      "label": "API Gateway",
      "shape": "star",
      "color": "#4A90E2",
      "size": 50,
      "status": "healthy",
      "error_rate": 0.1,
      "latency": 45,
      "throughput": 1200,
      "level": 0
    }
  ],
  "edges": [
    {
      "from": "api-gateway",
      "to": "frontend",
      "latency_ms": 45,
      "error_rate": 0.1,
      "throughput_rps": 1200,
      "status": "healthy"
    }
  ]
}
```

## Visual Design

### Color Scheme
- **Healthy**: `#22c55e` (Green) - All systems operational
- **Warning**: `#f59e0b` (Orange) - Issues detected, monitoring recommended
- **Critical**: `#ef4444` (Red) - Service degradation or errors

### Node Shapes
- **Star** ⭐: Microservices (API Gateway, Services)
- **Box** ▭: Frontend/UI Services
- **Diamond** ◊: Caching layers (Redis)
- **Ellipse** ⬭: Databases and Search engines

### Edge Visualization
- **Thickness**: Proportional to throughput (RPS)
- **Color**: Matches status (green/orange/red)
- **Labels**: Show throughput in RPS format (↓ 1200 RPS)

## File Structure

```
/workspaces/kharkai/
├── app.py                          # Flask application
├── nodegraph_nodes.csv             # Node definitions (CSV format)
├── nodegraph_edges.csv             # Connection definitions (CSV format)
├── nodegraph_data.json             # Node/edge data (JSON fallback)
├── family_tree_data.json           # Family tree sample data
├── infrastructure_nodes.csv        # Infrastructure topology
├── infrastructure_edges.csv        # Infrastructure connections
├── infrastructure_data.json        # Infrastructure data (JSON)
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Container definition
├── requirements.txt                # Python dependencies
└── README_VISUALIZATION.md         # Visualization guide
```

## Development Setup

### Local Development (Without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Visit http://localhost:5000/nodegraph
```

### Docker Development
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Restart after code changes (hot-reload enabled)
docker-compose restart
```

## URLs

| URL | View |
|-----|------|
| `http://localhost:5000/` | Home (Family Tree) |
| `http://localhost:5000/?type=family` | Family Tree Visualization |
| `http://localhost:5000/?type=infrastructure` | Infrastructure (PyVis Graph) |
| `http://localhost:5000/treemap?type=infrastructure` | Infrastructure (D3 Treemap) |
| `http://localhost:5000/nodegraph` | **Node Graph (Grafana-style)** |
| `http://localhost:5000/api/treemap-data` | API: Treemap JSON |

## Customization

### Adding New Services
Edit `nodegraph_nodes.csv`:
```csv
my-service,My Service,star,#4A90E2,40,healthy,0.5,150,1000
```

Then define connections in `nodegraph_edges.csv`:
```csv
api-gateway,my-service,150,0.5,1000,healthy
```

### Changing Colors
Update the hex color codes in the CSV or JSON files:
- Blue: `#4A90E2`
- Green: `#22c55e` (healthy)
- Orange: `#f59e0b` (warning)
- Red: `#ef4444` (critical)
- Purple: `#BD10E0`
- Teal: `#50E3C2`

### Adjusting Node Sizes
Modify the `size` column in nodes CSV (range: 20-70):
- Small: 30-35
- Medium: 35-45
- Large: 45-55
- Extra Large: 55+

### Tweaking Physics Simulation
Edit `create_nodegraph()` in `app.py`, `barnesHut` section:
```python
"barnesHut": {
    "gravitationalConstant": -30000,  # -50000 = more spread, -10000 = more compact
    "centralGravity": 0.3,              # 0.0 = no center pull, 1.0 = strong pull
    "springLength": 200,                # 150-250 recommended
    "springConstant": 0.04,             # Higher = stiffer connections
    "damping": 0.09                     # 0.05-0.15 recommended
}
```

## Features Explained

### Health Status Visualization
Nodes are colored based on their status:
- **Green nodes**: All metrics normal
- **Orange nodes**: Warning thresholds exceeded
- **Red nodes**: Critical issues detected (elasticsearch in demo)

The color is determined by the highest severity status across metrics.

### Metrics Indicators
When hovering over a node, a tooltip displays:
- Service name
- Current status
- Error rate percentage
- Response latency in milliseconds
- Throughput in requests per second

### Edge Metrics
Connections show:
- **Label**: Primary data flow (e.g., "↓ 1200 RPS")
- **Thickness**: Proportional to throughput volume
- **Color**: Matches connection health
- **Hover**: Shows detailed latency and error metrics

### Physics Simulation
The force-directed layout uses the Barnes-Hut algorithm:
- Automatically arranges nodes for clarity
- Prevents node overlap
- Creates natural groupings
- Stabilizes after 200 iterations (automatic)

## Performance Characteristics

Typical metrics in the example configuration:
- **Healthy services**: 0-1% error rate, <200ms latency
- **Warning services**: 1-5% error rate, 300-600ms latency
- **Critical services**: >5% error rate, >1000ms latency

The Elasticsearch service in the demo shows critical status with:
- 5.2% error rate (high)
- 2100ms latency (very slow)
- Only 400 RPS throughput (low)

This indicates a service requiring immediate attention.

## Use Cases

1. **Microservices Monitoring**: Monitor interconnected services in real-time
2. **Infrastructure Visualization**: Understand service dependencies
3. **Performance Analysis**: Identify bottlenecks via edge thickness and color
4. **Incident Response**: Quickly spot critical services
5. **Architecture Documentation**: Visual service topology reference
6. **Capacity Planning**: Identify high-throughput paths requiring optimization

## Troubleshooting

### Nodes overlapping?
Reduce `gravitationalConstant` to -50000 in physics settings.

### Connections too loose?
Reduce `springLength` to 150-170.

### Nodes moving too much?
Increase `damping` to 0.15 or higher.

### Colors not showing?
Verify hex codes start with `#` and are valid (e.g., `#4A90E2`).

## Requirements

- Python 3.11+
- Flask 3.0.0+
- PyVis 0.3.2+
- Docker & Docker Compose (optional, for containerization)

See `requirements.txt` for exact versions.

# Visualization Suite - Complete Overview

## 🎯 Available Visualizations

Your workspace now includes **4 different visualization types** for exploring hierarchical and relational data:

### 1. 🌳 Family Tree (Hierarchical)
**URL**: `http://localhost:5000/?type=family`
- **Technology**: PyVis (Network visualization)
- **Data**: 4 generations of family members
- **Features**:
  - Hierarchical tree layout
  - Gender-based color coding (blue males, purple females)
  - Interactive drag-and-drop nodes
  - Relationship types (parent, spouse, sibling)

### 2. 🏗️ Infrastructure Topology (Hierarchical)
**URL**: `http://localhost:5000/?type=infrastructure`
- **Technology**: PyVis (Network visualization)
- **Data**: 5-layer infrastructure (Service Groups → Services → Hosts → Ports → Status)
- **Features**:
  - Multi-level hierarchy visualization
  - Service dependency mapping
  - Color-coded by layer
  - Professional enterprise styling

### 3. 📦 Infrastructure Treemap (Nested Boxes)
**URL**: `http://localhost:5000/treemap?type=infrastructure`
- **Technology**: D3.js v7 (SVG-based)
- **Data**: Same infrastructure data, nested visual containment
- **Features**:
  - True visual nesting (boxes within boxes)
  - Service Groups contain Services
  - Services run on Hosts
  - **Ports nested inside Host boxes** (user requirement)
  - Color-coded by component type

### 4. 🌐 Grafana Node Graph Mimic ⭐ **NEW**
**URL**: `http://localhost:5000/nodegraph`
- **Technology**: PyVis (Force-directed physics layout)
- **Data**: Microservices topology with connection metrics
- **Features**:
  - **Interactive force-directed layout** (Barnes-Hut algorithm)
  - **Real-time metrics display** (Error %, Latency, Throughput)
  - **Health status indicators** (green/orange/red)
  - **Edge metrics** (connection thickness = throughput volume)
  - **12 microservices** in example (API Gateway, Auth, User, Product, Order, Database, Cache, Elasticsearch, Queue, etc.)
  - Automatic physics stabilization
  - Hover tooltips with detailed metrics
  - Responsive design

## 📊 Quick Comparison

| Feature | Family Tree | Infrastructure | Treemap | Node Graph |
|---------|------------|-----------------|---------|-----------|
| **Layout** | Hierarchical | Hierarchical | Nested Boxes | Force-Directed |
| **Best For** | Genealogy | Infrastructure | Containment | Microservices |
| **Interactivity** | Drag nodes | Drag nodes | Hover | Drag + Physics |
| **Metrics** | Basic titles | Basic titles | None | Full metrics |
| **Visual Nesting** | No | No | Yes ✓ | No |
| **Status Indicators** | No | No | No | Yes ✓ |
| **Technology** | PyVis | PyVis | D3.js | PyVis |

## 🗂️ Data Files

### Node Graph (NEW)
- `nodegraph_nodes.csv` - Service definitions (12 services)
- `nodegraph_edges.csv` - Connection definitions (16 connections)
- `nodegraph_data.json` - JSON format with full metadata

### Infrastructure
- `infrastructure_nodes.csv` - 20 infrastructure components
- `infrastructure_edges.csv` - 20 connections
- `infrastructure_data.json` - JSON fallback

### Family Tree
- `family_tree_data.json` - 14 family members, 20 relationships

## 🔄 Navigation

All visualizations have a **unified navigation bar** at the top:
```
[Family Tree] [Infrastructure (PyVis)] [Infrastructure (Treemap)] [Node Graph]
```

You can easily switch between views without losing data.

## 🎨 Node Graph Specifics (NEW)

### Microservices Included
1. **API Gateway** ⭐ - Entry point (healthy, 1200 RPS)
2. **Frontend** - UI service (healthy)
3. **Auth Service** ⚠️ - Authentication (warning: 1.5% errors)
4. **User Service** - User management (healthy)
5. **Product Service** - Product catalog (healthy)
6. **Order Service** ⚠️ - Order processing (warning: 2.1% errors)
7. **Redis Cache** - In-memory cache (5ms latency!)
8. **PostgreSQL Primary** - Main database
9. **PostgreSQL Replica** - Read-only copy
10. **Elasticsearch** 🔴 - Search engine (critical: 5.2% error, 2100ms latency)
11. **Message Queue** - Async processing (RabbitMQ-style)
12. **Monitoring** - Prometheus/Grafana collection

### Color Coding
- 🟢 **Green**: Healthy services
- 🟠 **Orange**: Warning threshold exceeded
- 🔴 **Red**: Critical issues (Elasticsearch in demo)

### Edge Information
Shows real-time metrics between services:
- **Throughput** (RPS) as edge label
- **Edge thickness** represents traffic volume
- **Color** indicates health status
- **Hover** reveals latency and error rates

## 🚀 Getting Started

### View Node Graph
```bash
# Open browser
http://localhost:5000/nodegraph
```

### View All Available Options
```
http://localhost:5000/           # Home (shows all links)
http://localhost:5000/?type=family
http://localhost:5000/?type=infrastructure
http://localhost:5000/treemap?type=infrastructure
http://localhost:5000/nodegraph
```

### Docker Management
```bash
# Start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Restart (after file edits)
docker-compose restart

# Stop
docker-compose down
```

## 📝 Customization

### Add New Microservices to Node Graph
Edit `nodegraph_nodes.csv`:
```csv
my-db,My Database,cylinder,#BD10E0,45,healthy,0,12,800
```

### Add New Connections
Edit `nodegraph_edges.csv`:
```csv
my-service,my-db,12,0,800,healthy
```

### Restart
```bash
docker-compose restart
```

## 🎯 Use Cases by Visualization

### Family Tree
- Genealogy tracking
- Organizational hierarchy
- Reporting structure
- Family relationship mapping

### Infrastructure (PyVis)
- Network topology
- System architecture
- Component relationships
- Hierarchical layout preference

### Infrastructure (Treemap)
- Space visualization
- Resource allocation
- Nested structures
- Container relationships (main use case)

### Node Graph
- Microservices monitoring
- Service dependency analysis
- Performance metrics display
- Real-time health indicators
- Incident response
- Capacity planning

## 📚 Documentation

- `README.md` - Project overview
- `README_NODEGRAPH.md` - Complete Node Graph guide (9.4KB)
- `README_VISUALIZATION.md` - General visualization guide
- `NODEGRAPH_QUICKSTART.md` - Quick start guide (this file)

## 🔧 Technical Stack

- **Backend**: Python 3.11, Flask 3.0.0
- **Visualization Libraries**: PyVis 0.3.2, D3.js v7
- **Containerization**: Docker, Docker Compose
- **Data Formats**: CSV, JSON
- **Styling**: HTML5, CSS3, Gradients

## 💡 Key Features (Node Graph)

✅ **Force-Directed Layout** - Services arrange themselves for clarity
✅ **Real-Time Metrics** - Error rate, latency, throughput visible
✅ **Health Indicators** - Color-coded status (green/orange/red)
✅ **Interactive Physics** - Automatic stabilization
✅ **Zoom & Pan** - Full navigation control
✅ **Hover Details** - Tooltip with comprehensive metrics
✅ **Edge Metrics** - Connection thickness = throughput
✅ **Professional Design** - Enterprise-grade styling
✅ **Hot Reload** - Changes reflect without restart
✅ **Multiple Data Formats** - CSV or JSON

## 🎓 Learning Path

1. **Start**: View Node Graph at `/nodegraph`
2. **Explore**: Hover over nodes and edges
3. **Customize**: Edit `nodegraph_nodes.csv` with your services
4. **Update**: Restart with `docker-compose restart`
5. **Compare**: Switch between visualization types
6. **Scale**: Add more services and connections as needed

---

**All visualizations are live and running on `http://localhost:5000`** 🎉

Choose the visualization that best fits your data:
- Family/Org hierarchies → **Family Tree** or **Infrastructure (PyVis)**
- Nested containment → **Infrastructure (Treemap)**
- Service dependencies with metrics → **Node Graph** ⭐


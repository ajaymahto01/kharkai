# Grafana Node Graph Mimic - Quick Start Guide

## 🚀 Launch the Visualization

### Access the Node Graph
Open your browser and navigate to:
```
http://localhost:5000/nodegraph
```

### Access Other Visualizations
- **Family Tree**: http://localhost:5000/?type=family
- **Infrastructure (PyVis)**: http://localhost:5000/?type=infrastructure  
- **Infrastructure (Treemap)**: http://localhost:5000/treemap?type=infrastructure
- **Node Graph**: http://localhost:5000/nodegraph ⭐ **NEW**

## 📋 What You'll See

### Node Graph Features
1. **Interactive Nodes** - Drag to reposition services
2. **Visual Status** - Color-coded health (green=healthy, orange=warning, red=critical)
3. **Service Dependencies** - Arrows showing service-to-service communication
4. **Metrics Display** - Hover over any node or edge to see:
   - Error Rate (%)
   - Latency (ms)
   - Throughput (RPS)
   - Service Status

### Example Services in Demo
- **API Gateway** (Primary entry point)
- **Frontend Service** 
- **Auth Service** (⚠️ Warning - 1.5% error rate)
- **User Service**
- **Product Service**
- **Order Service** (⚠️ Warning - 2.1% error rate)
- **Redis Cache** (Fast: 5ms latency)
- **PostgreSQL Primary** (Database)
- **Elasticsearch** (🔴 Critical - 5.2% error rate, 2100ms latency)
- **Message Queue**
- **Monitoring System**

## 🎨 Visual Design

### Node Shapes
- ⭐ **Star**: Microservices (API Gateway, Auth, User, Product, Order)
- ▭ **Box**: Frontend UI Services
- ◊ **Diamond**: Cache layers
- ⬭ **Ellipse**: Databases

### Status Colors
- 🟢 **Green (#22c55e)**: Healthy - All systems normal
- 🟠 **Orange (#f59e0b)**: Warning - Issues detected
- 🔴 **Red (#ef4444)**: Critical - Service degradation

### Edge Information
- **Thickness**: Represents throughput (thicker = more traffic)
- **Color**: Matches connection status
- **Label**: Shows requests per second (RPS)

## 📊 Understanding the Metrics

### Error Rate
- **Healthy**: 0-0.5% (occasional errors)
- **Warning**: 0.5-2% (attention needed)
- **Critical**: >2% (urgent intervention)

Example: Elasticsearch shows 5.2% error rate (critical)

### Latency
- **Healthy**: <100ms
- **Warning**: 100-500ms
- **Critical**: >500ms

Example: Elasticsearch at 2100ms is very slow

### Throughput
- Measured in RPS (Requests Per Second)
- Shows data volume flowing through connection
- Edge thickness represents this visually

## 🔧 Customization

### Edit Services (CSV Format)
Edit `nodegraph_nodes.csv` to add/modify services:
```csv
id,label,shape,color,size,status,error_rate,latency,throughput
my-service,My Service,star,#4A90E2,40,healthy,0.5,150,1000
```

### Edit Connections (CSV Format)
Edit `nodegraph_edges.csv` to change service dependencies:
```csv
from,to,latency_ms,error_rate,throughput_rps,status
api-gateway,my-service,150,0.5,1000,healthy
```

### Docker Restart (After Changes)
```bash
docker-compose restart
```
Changes are automatically reflected due to hot-reload.

## 📚 File Organization

```
nodegraph_nodes.csv         # Service definitions
nodegraph_edges.csv         # Connection definitions  
nodegraph_data.json         # JSON fallback format
app.py                      # Flask application (updated with Node Graph route)
```

## 🎯 Use Cases

1. **Microservices Monitoring** - See all services at a glance
2. **Dependency Mapping** - Understand service interactions
3. **Performance Analysis** - Identify bottlenecks (thick edges, red nodes)
4. **Incident Response** - Spot critical services instantly
5. **Capacity Planning** - Analyze high-throughput paths
6. **Architecture Documentation** - Visual service topology

## 💡 Tips

- **Zoom**: Use mouse wheel to zoom in/out
- **Pan**: Click and drag background to move around
- **Hover**: Move mouse over nodes/edges for detailed metrics
- **Drag**: Click and drag any node to reposition it
- **Physics**: Graph automatically stabilizes after ~1.5 seconds

## 🐛 Troubleshooting

**Nodes overlapping?**
- Increase gravitational constant (less negative)

**Can't see all nodes?**
- Zoom out with mouse wheel
- Let physics simulation run for 2-3 seconds

**Docker not updating changes?**
- Run: `docker-compose restart`

**Container not starting?**
- Check: `docker-compose logs`

## 🔗 Learn More

See `README_NODEGRAPH.md` for:
- Detailed configuration options
- Physics simulation parameters
- Color customization
- Advanced data formats
- Performance optimization

---

**Ready to explore?** Open http://localhost:5000/nodegraph in your browser! 🎉

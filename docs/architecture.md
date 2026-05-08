# System Architecture
## Smart Waste Management Portal - A Coruña

**Version**: 1.0  
**Date**: May 2026  
**Status**: Design Draft

---

## System Overview

The Smart Waste Management Portal is built on a modern microservices architecture leveraging FIWARE components for context management. The system integrates real-time IoT data, implements intelligent route optimization, and provides comprehensive analytics to municipal waste management operations.

### Design Principles
- **Scalability**: Horizontal scaling of services and data stores
- **Resilience**: Fault tolerance and circuit breaker patterns
- **Interoperability**: NGSI-LD standard compliance (ETSI)
- **Observability**: Comprehensive logging, monitoring, and tracing
- **Security**: Defense in depth with encryption and access control

---

## Architecture Layers

### 1. Presentation Layer
**Components**: Web Portal, Mobile App, Admin Dashboard, Grafana

**Technologies**:
- Frontend Framework: React.js or Vue.js
- Mapping: Leaflet.js + OpenStreetMap
- Charting: Chart.js, D3.js
- Responsive Design: Bootstrap 5+

**Responsibilities**:
- User interface for citizens, drivers, dispatchers, admins
- Real-time map visualization
- Data queries and reporting
- User authentication UI

**Deployment**: CDN + Static Hosting (AWS S3, Azure Blob Storage)

---

### 2. Application Layer
**Components**: REST APIs, GraphQL Layer, Business Logic Services

**Technologies**:
- Backend: Python (Flask, FastAPI)
- API Gateway: Kong or AWS API Gateway
- Service Mesh: Istio (optional, for advanced deployments)
- Caching: Redis

**Key Services**:
1. **Auth Service**: Token management, MFA, role-based access
2. **Container API**: CRUD operations for waste containers
3. **Route Service**: Route optimization orchestration
4. **Notification Service**: Real-time alerts and push notifications
5. **Reporting Service**: Analytics and export functionality

**Deployment**: Docker containers on Kubernetes or Docker Swarm

---

### 3. FIWARE Context Management Layer
**Components**: Orion Context Broker, IoT Agent, QuantumLeap

#### 3.1 Orion Context Broker
- **Role**: Central context management and NGSI-LD endpoint
- **Protocol**: NGSI-LD REST API
- **Data Model**: All entities as NGSI-LD with temporal support
- **Update Pattern**: Subscriptions for real-time data propagation

#### 3.2 IoT Agent
- **Role**: Protocol translation (MQTT, CoAP, HTTP to NGSI-LD)
- **Protocols Supported**:
  - MQTT: Primary for battery-powered sensors
  - HTTP: Fallback and webhook support
  - CoAP: Alternative for resource-constrained devices
- **Features**: Device provisioning, attribute mapping, bidirectional commands

#### 3.3 QuantumLeap
- **Role**: Time-series data persistence and query
- **Backend**: PostgreSQL + TimescaleDB extension
- **Retention Policy**: 24 months minimum
- **Query Capability**: Historical aggregations, trend analysis

**Deployment**: Docker containers, Helm charts for Kubernetes

---

### 4. Data Layer

#### Data Stores
| Component | Technology | Purpose | Replication |
|-----------|-----------|---------|------------|
| **Entity Store** | PostgreSQL (JSONB) | NGSI-LD entities | Master-Replica |
| **TimeSeries** | TimescaleDB | Historical observations | Replicated |
| **Cache** | Redis | Session & query cache | Sentinel |
| **Search** | Elasticsearch | Full-text search & logs | Cluster |
| **GIS Database** | PostGIS | Geospatial queries | Replicated |

#### Data Architecture
```
┌──────────────────────────────────────────────────────────┐
│                   Application Layer                       │
│              (APIs & Business Logic)                      │
└──────────────┬───────────────────────────────────────────┘
               │
        ┌──────┴──────┬──────────────┬───────────┐
        │             │              │           │
    ┌───▼──┐  ┌──────▼──┐  ┌───────▼──┐   ┌────▼──┐
    │Redis │  │Postgres │  │Timescale │   │  ES   │
    │Cache │  │ JSONB   │  │  TimeSeries  │Search │
    └──────┘  └─────────┘  └──────────┘   └───────┘
               │
    ┌──────────▼──────────┐
    │  PostgreSQL with    │
    │  PostGIS (Spatial)  │
    └─────────────────────┘
```

---

## Component Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      CITIZEN / DRIVER / ADMIN                    │
│                    (Web Browser + Mobile)                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───▼────┐       ┌────▼────┐       ┌──▼───┐
    │Web App │       │Mobile   │       │Admin │
    │React   │       │PWA/App  │       │Portal│
    │Leaflet │       │         │       │      │
    └───┬────┘       └────┬────┘       └──┬───┘
        │                 │               │
        └─────────────────┼───────────────┘
                          │
        ┌─────────────────▼──────────────────┐
        │      API GATEWAY / Kong             │
        │    (Auth, Rate Limit, Routing)      │
        └─────────────────┬──────────────────┘
                          │
        ┌─────────────────┴──────────────────┐
        │                                     │
    ┌───▼──────────────┐            ┌────────▼─────┐
    │  Container API   │            │  Route       │
    │  & Management    │            │  Optimization│
    │  (FastAPI)       │            │  Service     │
    └───┬──────────────┘            └────────┬─────┘
        │                                     │
        └──────────────────┬──────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │   FIWARE Context Management         │
        │                                     │
        │  ┌─────────────────────────────┐   │
        │  │ Orion Context Broker        │   │
        │  │ (NGSI-LD Endpoint)          │   │
        │  └────────┬────────────────────┘   │
        │           │                        │
        │  ┌────────▼──────┐   ┌──────────┐ │
        │  │ IoT Agent     │   │QL (Time) │ │
        │  │ (MQTT/CoAP)   │   │ Series   │ │
        │  └────────┬──────┘   └──────────┘ │
        │           │                        │
        └───────────┼────────────────────────┘
                    │
        ┌───────────▼─────────────┐
        │   IoT Devices / Sensors │
        │   - Fill Level          │
        │   - Temperature         │
        │   - Tamper Detection    │
        └─────────────────────────┘
        
        [Parallel Data Flow]
        
        ┌───────────────────────────────────┐
        │  Data Layer                        │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │ PostgreSQL + PostGIS         │ │
        │  │ - Entities (JSONB)           │ │
        │  │ - Geospatial Queries         │ │
        │  │ - Configuration              │ │
        │  └──────────────────────────────┘ │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │ TimescaleDB                  │ │
        │  │ - Historical Observations    │ │
        │  │ - 24-month Retention         │ │
        │  └──────────────────────────────┘ │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │ Redis Cache                  │ │
        │  │ - Session Store              │ │
        │  │ - Query Cache                │ │
        │  └──────────────────────────────┘ │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │ Elasticsearch                │ │
        │  │ - Logs & Metrics             │ │
        │  │ - Full-text Search           │ │
        │  └──────────────────────────────┘ │
        └────────────────────────────────────┘
        
        ┌──────────────────────────────────────┐
        │  Analytics & Visualization           │
        │                                      │
        │  ┌──────────────────────────────┐   │
        │  │ Grafana                      │   │
        │  │ - Real-time Dashboards       │   │
        │  │ - Custom Reports             │   │
        │  └──────────────────────────────┘   │
        │                                      │
        │  ┌──────────────────────────────┐   │
        │  │ Kibana (optional)            │   │
        │  │ - Log Analysis               │   │
        │  └──────────────────────────────┘   │
        └──────────────────────────────────────┘
```

---

## FIWARE Stack Integration

### Data Flow: Sensor → Application

```
┌───────────────────┐
│  IoT Device       │
│  (Waste Container)│
│                   │
│ ┌─────────────┐   │
│ │ Ultrasonic  │   │
│ │ Sensor      │   │
│ └──────┬──────┘   │
│        │          │
│ ┌──────▼──────┐   │
│ │ MQTT Client │   │
│ └──────┬──────┘   │
└────────┼──────────┘
         │ (MQTT)
         │ Topic: /devices/container-001/attrs/fillLevel
         │
┌────────▼────────────────────────────┐
│  IoT Agent                          │
│  (Protocol Translation)             │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ MQTT Driver                 │   │
│  │ - Device Provisioning       │   │
│  │ - Attribute Mapping         │   │
│  │ - Data Transformation       │   │
│  └──────────┬──────────────────┘   │
└─────────────┼──────────────────────┘
              │ (NGSI-LD)
              │ PUT /ngsi-ld/v1/entities/...
              │
┌─────────────▼──────────────────────┐
│  Orion Context Broker              │
│  (Entity Update & Subscription)     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Entity Store                │   │
│  │ (In-Memory + Persistence)   │   │
│  └──────────┬──────────────────┘   │
└─────────────┼──────────────────────┘
              │ (Event Notification)
              │
    ┌─────────┴──────────┐
    │                    │
┌───▼─────────────┐  ┌──▼───────────┐
│ Application API │  │ QuantumLeap   │
│ (Subscribed)    │  │ (Time-Series) │
│                 │  │               │
└─────────────────┘  └───────────────┘
```

### Update Frequency & Latency
| Step | Technology | Latency | Notes |
|------|-----------|---------|-------|
| Sensor Reading | IoT Device | - | Every 5-15 minutes |
| MQTT Publish | IoT Device → Broker | <100ms | LAN connection |
| IoT Agent Process | Transformation | <50ms | Stateless |
| Orion Update | Context Broker | <100ms | Memory + DB |
| QuantumLeap Persist | Time-Series DB | <500ms | Async write |
| **Total Latency** | - | **~1 second** | E2E |

---

## Deployment Architecture

### Development Environment
```
Local Machine
├── Docker (docker-compose)
│   ├── Orion Context Broker
│   ├── IoT Agent (MQTT)
│   ├── QuantumLeap
│   ├── PostgreSQL
│   ├── TimescaleDB
│   ├── Redis
│   └── Backend API (localhost:8000)
└── Frontend (localhost:3000)
```

### Production Environment
```
Cloud Infrastructure (AWS/Azure/GCP)
├── Kubernetes Cluster
│   ├── Backend Services
│   │   ├── API Gateway
│   │   ├── Container Service (replicas)
│   │   ├── Route Optimization Service
│   │   └── Notification Service
│   │
│   ├── FIWARE Stack
│   │   ├── Orion (HA)
│   │   ├── IoT Agent (HA)
│   │   └── QuantumLeap
│   │
│   ├── Data Stores
│   │   ├── PostgreSQL (Primary + Replicas)
│   │   ├── TimescaleDB (Cluster)
│   │   ├── Redis (Sentinel)
│   │   └── Elasticsearch (Cluster)
│   │
│   └── Observability
│       ├── Prometheus
│       ├── Grafana
│       ├── ELK Stack
│       └── Jaeger (Tracing)
│
├── External Services
│   ├── CDN (Frontend static assets)
│   ├── SendGrid/Twilio (Notifications)
│   └── VROOM API (Route optimization)
│
└── Load Balancers & Firewalls
    ├── Application Load Balancer
    ├── Network Security Groups
    └── WAF (Web Application Firewall)
```

---

## Data Flow Architecture

### Real-Time Data Ingestion
```
1. IoT Device generates reading every 5 minutes
2. Publishes to MQTT broker (topic: /devices/{id}/attrs/{attr})
3. IoT Agent subscribes and transforms to NGSI-LD
4. Posts to Orion Context Broker
5. Orion triggers subscriptions (ApplicationAPI, QuantumLeap)
6. Data persisted in both real-time and time-series stores
```

### Request-Response Flow (API)
```
1. Client requests container status: GET /api/containers/coruna-001
2. API Gateway authenticates and routes
3. Application queries Redis cache (TTL: 30s)
4. Cache miss → Query Orion Context Broker
5. Orion returns NGSI-LD entity
6. API transforms to response format
7. Response cached and returned to client
```

### Batch Analytics Flow
```
1. Scheduled job (nightly) or on-demand query
2. Grafana queries TimescaleDB directly
3. QuantumLeap aggregations (e.g., avg fill level per isle per day)
4. Results visualized in dashboards
5. Reports exported to CSV/JSON
```

---

## Security Architecture

### Authentication & Authorization
```
┌─────────────────────────────────────────┐
│  Client                                 │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │  OAuth 2.0 / OIDC
         │  MFA (TOTP/SMS)
         └────────┬────────┘
                  │
┌─────────────────▼────────────────────────┐
│  API Gateway                             │
│  - Token Validation                      │
│  - Rate Limiting                         │
│  - Request Inspection                    │
└────────────────┬─────────────────────────┘
                 │
    ┌────────────▼──────────────┐
    │ RBAC & Policy Engine      │
    │ (Roles: Admin, Driver,    │
    │  Dispatcher, Citizen)     │
    └────────────┬───────────────┘
                 │
    ┌────────────▼──────────────┐
    │ Application Services      │
    │ (Authenticated Request)   │
    └──────────────────────────┘
```

### Data Protection
- **In Transit**: TLS 1.3+ for all HTTP(S) communications
- **At Rest**: AES-256 encryption for sensitive data (passwords, tokens)
- **Database**: Row-level security for multi-tenant data isolation
- **Logs**: Secrets masking, audit trails

### Network Security
- VPC/VNet isolation
- Network security groups / Security groups
- Web Application Firewall (AWS WAF / Azure WAF)
- DDoS protection (CloudFlare, AWS Shield)

---

## Scalability & Performance

### Horizontal Scaling Strategy
| Component | Scale Unit | Scaling Trigger |
|-----------|-----------|-----------------|
| API Servers | Pods/Instances | CPU > 70%, Memory > 80% |
| Orion | Instances | Request latency > 200ms |
| Database | Read Replicas | Query load > 80% |
| Cache | Cluster | Eviction rate > 10% |
| QuantumLeap | Partitions | Data ingestion > 1000 writes/sec |

### Performance Targets
- API p95 latency: 200ms
- Map render: <500ms (500 containers)
- Route calculation: <30s (100 stops)
- Cache hit rate: >80%
- Database query time: <100ms (p95)

---

## Monitoring & Observability

### Metrics Collected
- **Application**: Request latency, error rates, throughput
- **Infrastructure**: CPU, memory, disk, network utilization
- **Database**: Query time, connection pool, replication lag
- **FIWARE**: Entity update frequency, subscription performance
- **Business**: Active containers, collection efficiency, SLA compliance

### Dashboards
1. **Operational Dashboard**: System health, service status
2. **Business Dashboard**: KPIs, efficiency metrics
3. **Developer Dashboard**: Error rates, latency breakdown
4. **Grafana**: Pre-built waste management specific dashboards

### Alerting Thresholds
- Service down: Alert immediately
- Latency > 500ms: Alert after 5 minutes
- Error rate > 5%: Alert immediately
- Container data stale (>1 hour): Alert after 30 minutes

---

## Disaster Recovery & Business Continuity

### RTO & RPO Targets
- **RTO** (Recovery Time Objective): ≤ 1 hour
- **RPO** (Recovery Point Objective): ≤ 15 minutes

### Backup Strategy
- Database: Automated daily snapshots + point-in-time recovery
- Configuration: Version controlled in Git
- Secrets: Managed by HashiCorp Vault with replication
- Logs: Retained for minimum 90 days

### Failover Mechanisms
- Database: Automatic failover with read replicas
- Application: Load balancer redirects to healthy instances
- Cache: Sentinel for Redis high availability
- DNS: GeoDNS for regional failover (if multi-region)

---

## Implementation Roadmap

### Phase 1 (MVP - Week 1-12)
- [ ] Core FIWARE stack deployment
- [ ] Basic REST API
- [ ] Single container type support
- [ ] Simple mapping interface
- [ ] Real-time fill level monitoring

### Phase 2 (Beta - Week 13-20)
- [ ] Route optimization integration
- [ ] Multi-container type support
- [ ] Advanced analytics
- [ ] Driver mobile app
- [ ] Dispatcher dashboard

### Phase 3 (Production - Week 21-24)
- [ ] Full feature set
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Citizen portal launch
- [ ] Public API release

---

## References & External Resources

- **FIWARE Architecture Guide**: https://fiware-developer.readthedocs.io/
- **NGSI-LD Specification**: https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/
- **Orion User Manual**: https://fiware-orion.readthedocs.io/
- **QuantumLeap Documentation**: https://quantumleap.readthedocs.io/
- **IoT Agent (MQTT)**: https://github.com/telefonicaid/iotagent-node-lib
- **Kubernetes Best Practices**: https://kubernetes.io/docs/
- **VROOM API Documentation**: https://github.com/VROOM-Project/vroom/wiki

---

**Document Version History:**
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | May 2026 | Solutions Architect | Initial design |


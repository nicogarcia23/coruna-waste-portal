# Smart Waste Management Portal - A Coruña

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/coruna-waste-portal)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive, data-driven waste management system for the city of A Coruña, powered by FIWARE and NGSI-LD smart data models.

## Project Overview

The Smart Waste Management Portal provides real-time monitoring and optimization of waste collection across A Coruña. By integrating IoT sensors, contextual data management, and advanced routing algorithms, the system enables:

- **Real-time Container Monitoring**: Track fill levels and operational status of waste containers across the city
- **Optimized Collection Routes**: Data-driven route planning for waste collection vehicles
- **Citizen Engagement**: Mobile-friendly interface for citizens to report issues or locate containers
- **Data-Driven Insights**: Historical analytics and predictive modeling for waste generation patterns

## Technology Stack

### FIWARE & Context Management
- **Orion Context Broker**: NGSI-LD context management and temporal data repository
- **IoT Agent**: Device management and IoT protocol translation (MQTT, CoAP, etc.)
- **QuantumLeap**: Time-series data persistence and analytics
- **NGSI-LD Smart Data Models**: Standardized models for waste management (WasteContainer, WasteContainerIsle, WasteObserved)

### Frontend
- **Leaflet.js + OpenStreetMap**: Interactive mapping and geospatial visualization
- **Chart.js**: Real-time metrics and historical trend visualization
- **React/Vue.js**: Modern, responsive web application (framework TBD)

### Backend & Data Processing
- **Python**: Primary backend language
- **Pandas/GeoPandas**: Data analysis and manipulation
- **Polars**: High-performance data queries
- **PostgreSQL + PostGIS**: Geospatial database

### Visualization & Monitoring
- **Grafana**: Real-time dashboards and analytics
- **Kibana** (optional): Advanced log analysis and visualization

### Optimization
- **VROOM**: Vehicle Routing Optimization for waste collection routes

### Deployment
- **Docker & Docker Compose**: Containerized deployment
- **Kubernetes** (optional): Production orchestration

## System Architecture

The system follows a microservices architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│              (Web & Mobile Frontends - Leaflet, Charts)      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 Application Layer                            │
│         (REST/GraphQL APIs, Business Logic, Auth)           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              FIWARE Context Broker Layer                      │
│  (Orion CB, IoT Agent, QuantumLeap - NGSI-LD)              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Data Layer                                  │
│    (PostgreSQL+PostGIS, TimescaleDB, Redis Cache)          │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture information, see [docs/architecture.md](docs/architecture.md).

## Getting Started

### Prerequisites
- Docker & Docker Compose (v20.10+)
- Git
- Python 3.9+ (for backend development)
- Node.js 16+ (for frontend development)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/coruna-waste-portal.git
   cd coruna-waste-portal
   ```

2. **Start the FIWARE stack**
   ```bash
   cd infra
   docker-compose up -d
   ```

3. **Run the backend**
   ```bash
   cd ../backend
   pip install -r requirements.txt
   python app.py
   ```

4. **Run the frontend**
   ```bash
   cd ../frontend
   npm install
   npm start
   ```

5. **Access the portal**
   - Web UI: http://localhost:3000
   - Grafana: http://localhost:3001 (default: admin/admin)
   - Orion Context Broker: http://localhost:1026

For detailed setup instructions, see the [Getting Started Guide](docs/README.md).

## Data Models

The project uses NGSI-LD smart data models for semantic interoperability:

### Core Models
- **WasteContainer**: Individual waste collection points with metadata
- **WasteContainerIsle**: Grouped collection zones or "isles"
- **WasteContainerModel**: Technical specifications and capabilities
- **WasteObserved**: Real-time observations (fill levels, temperature, etc.)

See [docs/data_model.md](docs/data_model.md) for complete specifications and examples.

## Project Requirements

For comprehensive product requirements and user stories, see [docs/PRD.md](docs/PRD.md).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit changes: `git commit -m "feat: description"`
3. Push to branch: `git push origin feature/your-feature-name`
4. Submit a Pull Request

## Project Structure

```
coruna-waste-portal/
├── docs/                    # Documentation files
│   ├── PRD.md              # Product Requirements Document
│   ├── data_model.md       # NGSI-LD Data Models
│   └── architecture.md     # System Architecture
├── frontend/               # Frontend application
├── backend/                # Backend application
├── iot/                    # IoT device firmware & configurations
├── data/                   # Data files and utilities
│   └── mock/               # Mock/test data
├── infra/                  # Docker Compose & infrastructure configs
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── LICENSE                # License file
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support & Contact

For questions, issues, or suggestions, please open an issue on GitHub or contact the development team.

---

**Last Updated**: May 2026
**Maintained by**: A Coruña Smart City Initiative

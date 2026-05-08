# Product Requirements Document (PRD)
## Smart Waste Management Portal - A Coruña

**Version**: 1.0  
**Date**: May 2026  
**Status**: Draft

---

## Overview

The Smart Waste Management Portal is a data-driven system designed to optimize waste collection operations across A Coruña. By leveraging IoT sensors, real-time context management through FIWARE, and intelligent route optimization, the system will improve operational efficiency, reduce environmental impact, and enhance citizen engagement.

### Objectives
- Minimize waste collection costs through optimized routing
- Reduce response times to overflow incidents
- Provide transparent, real-time information to citizens
- Enable data-driven decision-making for municipal planning
- Support sustainability goals by tracking collection patterns

---

## User Stories

### Citizen Personas

#### UC1: Citizen - Locate Nearby Container
**As a** citizen,  
**I want to** locate the nearest waste container on a map,  
**So that** I can dispose of waste quickly and conveniently.

**Acceptance Criteria:**
- Map displays all active containers
- Container filters by type (organic, glass, paper, plastic, etc.)
- Distance and directions are shown
- Real-time fill level is displayed

#### UC2: Citizen - Report Container Issue
**As a** citizen,  
**I want to** report a full or damaged container,  
**So that** municipal services can respond quickly.

**Acceptance Criteria:**
- Simple reporting form with issue type and location
- Photo attachment option
- Acknowledgment and ticket reference
- Status tracking available

#### UC3: Citizen - View Collection Schedule
**As a** citizen,  
**I want to** know when waste is collected in my area,  
**So that** I can plan accordingly.

**Acceptance Criteria:**
- Calendar view by location
- Push notifications before collection
- Integration with personal calendar (iCal, Google Calendar)

---

### Waste Collection Service Personas

#### UC4: Driver - Optimized Route
**As a** waste collection driver,  
**I want to** receive an optimized route based on real-time container data,  
**So that** I minimize drive time and fuel consumption.

**Acceptance Criteria:**
- Route is calculated with fill level and proximity
- In-vehicle navigation interface (Android/iOS compatible)
- Real-time traffic integration
- Route can be adjusted manually
- Completion confirmation with timestamp

#### UC5: Dispatcher - Monitor Fleet
**As a** fleet dispatcher,  
**I want to** monitor all collection vehicles in real-time,  
**So that** I can respond to emergencies and track efficiency.

**Acceptance Criteria:**
- Live vehicle tracking on map
- Route progress and ETA display
- Incident alerts and notifications
- Historical trip analytics

#### UC6: Maintenance - Predict Issues
**As a** maintenance manager,  
**I want to** receive alerts when containers show anomalies (temperature, tampering, malfunction),  
**So that** I can schedule maintenance proactively.

**Acceptance Criteria:**
- Anomaly detection based on sensor data
- Maintenance ticket auto-creation
- Equipment lifecycle tracking
- Predictive maintenance recommendations

---

### Administrator & Data Analyst Personas

#### UC7: Administrator - System Configuration
**As a** system administrator,  
**I want to** configure container types, zones, and operational parameters,  
**So that** the system adapts to municipal policies.

**Acceptance Criteria:**
- Zone/isle creation and management
- Container type definitions
- Capacity and collection frequency settings
- User access control and permissions

#### UC8: Data Analyst - Historical Reports
**As a** data analyst,  
**I want to** analyze historical waste generation patterns,  
**So that** I can support strategic planning and forecasting.

**Acceptance Criteria:**
- Customizable report generation
- Data export (CSV, JSON, Parquet)
- Visualization of trends and anomalies
- Predictive insights (ML-based)

---

## Functional Requirements

### FR1: Real-Time Container Monitoring
- System shall collect fill level, temperature, and status from each IoT-enabled container every 5 minutes
- Data shall be stored in Orion Context Broker using NGSI-LD format
- Historical time-series data shall be retained in QuantumLeap (minimum 2 years)

### FR2: Container Localization
- Container location (latitude, longitude) shall be stored with accuracy ±5 meters
- Interactive map shall display containers with OpenStreetMap/Leaflet
- Container clustering for high-density areas

### FR3: Route Optimization
- System shall generate optimized collection routes using VROOM algorithm
- Routes shall consider: container fill level, distance, traffic, vehicle capacity
- Alternative routes shall be available for manual selection

### FR4: Real-Time Notifications
- Citizens shall receive notifications when containers are full (if public tracking enabled)
- Dispatchers shall receive alerts for overflow, malfunction, or anomalies
- Drivers shall receive turn-by-turn navigation updates

### FR5: Data Integration
- Integration with municipal waste collection systems (existing)
- Integration with traffic/weather services
- Export capability to third-party analytics tools

### FR6: User Authentication & Authorization
- Multi-factor authentication (MFA) for sensitive operations
- Role-based access control (RBAC): Citizen, Driver, Dispatcher, Admin, Analyst
- Audit log of all actions

### FR7: Mobile Responsiveness
- Frontend shall be fully responsive (mobile, tablet, desktop)
- Native apps (iOS, Android) or progressive web app (PWA)
- Offline mode for critical operations (to be determined)

### FR8: Reporting & Analytics
- Pre-built dashboards in Grafana for KPIs
- Customizable report generation
- Data export in multiple formats (CSV, JSON, GeoJSON)

---

## Non-Functional Requirements

### NFR1: Performance
- API response time: ≤ 200ms (p95)
- Map rendering: ≤ 500ms for 500+ containers
- Route calculation: ≤ 30 seconds for 100+ stops

### NFR2: Scalability
- System shall handle ≥ 5,000 active containers
- Support ≥ 100 simultaneous users
- Container queries shall scale horizontally

### NFR3: Availability
- System uptime: ≥ 99.5%
- RTO (Recovery Time Objective): ≤ 1 hour
- RPO (Recovery Point Objective): ≤ 15 minutes
- Automated failover mechanisms

### NFR4: Security
- All data in transit shall use TLS 1.3+
- Data at rest shall be encrypted (AES-256)
- OWASP Top 10 compliance
- Annual security audits

### NFR5: Data Privacy (GDPR)
- Personal data collection shall be minimized
- Right to be forgotten implementation
- Data retention policies shall be explicit
- Privacy impact assessments for new features

### NFR6: Interoperability
- NGSI-LD compliant (ETSI standard)
- OpenAPI 3.0 specification for all REST endpoints
- Support for standard IoT protocols (MQTT, CoAP, HTTP)

### NFR7: Maintainability
- Code coverage: ≥ 80%
- Automated testing (unit, integration, E2E)
- CI/CD pipeline with automated deployments
- Documentation-first development

### NFR8: Sustainability
- Reduce collection vehicle travel by ≥ 15% (Year 1)
- Carbon footprint tracking for routes
- Integration with municipal sustainability goals

---

## Out of Scope

### Phase 1 Exclusions
- **AI/ML Anomaly Detection**: Future phase (ML pipeline architecture TBD)
- **Waste Composition Analysis**: Requires additional hardware (spectroscopy sensors)
- **Automated Waste Sorting**: Complex logistical dependency
- **Public API Monetization**: Policy decision required first
- **Multi-language Support**: English only in Phase 1
- **Mobile Native Apps**: PWA sufficient for Phase 1
- **Blockchain Integration**: Regulatory clarity needed
- **Real-time Driver Dash Cameras**: Privacy concerns in review

---

## Success Metrics (KPIs)

| Metric | Baseline | Target | Timeline |
|--------|----------|--------|----------|
| Route Efficiency | TBD | +15% reduction in drive time | 6 months |
| Container Overflow Incidents | TBD | -30% | 6 months |
| System Uptime | - | 99.5% | Ongoing |
| Citizen Engagement | 0 | 1,000+ active users | 12 months |
| Data Latency | - | <5 min | Ongoing |
| Cost Savings | Baseline | €50K/year | 12 months |

---

## Timeline & Milestones

| Milestone | Date | Deliverables |
|-----------|------|--------------|
| Architecture Review | Week 2 | System design, API specs |
| MVP Release | Week 12 | Core features, basic dashboard |
| Beta Testing | Week 16 | 5-10 containers, select drivers |
| Public Beta | Week 20 | City-wide pilot, 100+ containers |
| Full Launch | Week 24 | All planned containers, full feature set |

---

## Assumptions & Constraints

### Assumptions
- IoT sensors will be provided by municipal IT department
- FIWARE infrastructure will be hosted by municipal cloud provider
- Existing waste management database is available for integration
- Citizens have internet access for portal usage

### Constraints
- Budget: €XXX,XXX (TBD)
- Team size: 6-8 engineers
- Timeline: 6 months to MVP
- Regulatory compliance: GDPR, Local Data Protection Laws

---

## Appendices

### Appendix A: Glossary
- **FIWARE**: Framework for the development of smart applications
- **NGSI-LD**: RESTful API for managing context information (linked data)
- **Orion CB**: FIWARE's Context Broker component
- **IoT Agent**: FIWARE protocol adapter
- **VROOM**: Vehicle Routing Open source Optimization Machine

### Appendix B: References
- ETSI NGSI-LD Specification: https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/gs_cim_009v010801p.pdf
- FIWARE Documentation: https://fiware-developer.readthedocs.io/
- Smart Data Models: https://smartdatamodels.org/

---

**Document Version History:**
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | May 2026 | Project Team | Initial draft |


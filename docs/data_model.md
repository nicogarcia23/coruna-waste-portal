# NGSI-LD Data Models
## Smart Waste Management Portal - A Coruña

**Version**: 1.0  
**Date**: May 2026  
**Format**: NGSI-LD (ETSI standard)  
**Reference**: https://smartdatamodels.org/

---

## Overview

All entities in the Smart Waste Management Portal follow the NGSI-LD specification for semantic data representation. This ensures interoperability with FIWARE components and other smart city systems following ETSI standards.

### Core Principles
- **Linked Data**: URIs identify entities and relationships
- **JSON-LD Format**: Machine-readable and human-readable data
- **Temporal Semantics**: Historical data tracking through QuantumLeap
- **Composability**: Entities can be extended without breaking changes

---

## Context Strategy

Use a layered @context stack for every entity:

1. ETSI NGSI-LD core context.
2. Smart Data Models base context.
3. Entity-specific Smart Data Models context.
4. Local extension namespace for project-only fields.

Recommended local namespace:

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    "https://smartdatamodels.org/extra/ngsi-ld_waste-container.jsonld",
    {
      "coruña-waste": "urn:ngsi-ld:coruña-waste:"
    }
  ]
}
```

## NGSI-LD Entity Models

### 1. WasteContainer

Represents a physical waste collection point.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteContainer:coruna-001",
  "type": "WasteContainer",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    "https://smartdatamodels.org/extra/ngsi-ld_waste-container.jsonld",
    {
      "coruña-waste": "urn:ngsi-ld:coruña-waste:"
    }
  ],
  
  "name": {
    "type": "Property",
    "value": "Container_Praza_Xeneral_Franco_01"
  },
  
  "description": {
    "type": "Property",
    "value": "Waste container for mixed waste collection"
  },
  
  "containerType": {
    "type": "Property",
    "value": "recycling"  // "organic", "glass", "paper", "plastic", "mixed", "bulky"
  },
  
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [-8.3879, 43.3734]  // [longitude, latitude]
    }
  },
  
  "capacity": {
    "type": "Property",
    "value": 240,  // liters
    "unitCode": "LTR"
  },
  
  "isleId": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:WasteContainerIsle:coruna-isle-01"
  },
  
  "modelId": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:WasteContainerModel:model-wheelbin-240l"
  },
  
  "installationDate": {
    "type": "Property",
    "value": "2022-03-15T10:00:00Z"
  },
  
  "status": {
    "type": "Property",
    "value": "operational"  // "operational", "maintenance", "out_of_service"
  },
  
  "nextCollection": {
    "type": "Property",
    "value": "2026-05-09T06:30:00Z"
  },
  
  "municipalityCode": {
    "type": "Property",
    "value": "15030"
  },
  
  "hasOperator": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Organization:coruna-waste-services"
  }
}
```

#### Attribute Table
| Attribute | NGSI-LD Type | Static/Dynamic | Notes |
|-----------|--------------|----------------|-------|
| id | Identifier | Static | URN for the physical container |
| type | Type | Static | Must be `WasteContainer` |
| name | Property | Static | Human-readable name |
| description | Property | Static | Optional descriptive text |
| containerType | Property | Static | organic, glass, paper, plastic, general waste, etc. |
| location | GeoProperty | Static | Point geometry for the container position |
| capacity | Property | Static | Container capacity in liters |
| isleId | Relationship | Static | Link to parent WasteContainerIsle |
| modelId | Relationship | Static | Link to WasteContainerModel |
| installationDate | Property | Static | Asset lifecycle timestamp |
| status | Property | Dynamic | operational, maintenance, out_of_service |
| nextCollection | Property | Dynamic | Operational schedule target |
| municipalityCode | Property | Static | Municipal code for A Coruña |
| hasOperator | Relationship | Static | Operator/organization relation |

---

### 2. WasteObserved

Real-time observations from waste containers.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteObserved:coruna-001-2026-05-08T15:30:00Z",
  "type": "WasteObserved",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    "https://smartdatamodels.org/extra/ngsi-ld_waste-observed.jsonld",
    {
      "coruña-waste": "urn:ngsi-ld:coruña-waste:"
    }
  ],
  
  "refContainer": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:WasteContainer:coruna-001"
  },
  
  "dateObserved": {
    "type": "Property",
    "value": "2026-05-08T15:30:00Z"
  },
  
  "fillLevel": {
    "type": "Property",
    "value": 0.85,  // 0.0 to 1.0 (percentage)
    "unitCode": "C62"  // Percentage
  },
  
  "temperature": {
    "type": "Property",
    "value": 22.5,
    "unitCode": "CEL"  // Celsius
  },
  
  "methaneLevel": {
    "type": "Property",
    "value": 0.02,  // ppm (optional, if sensor available)
    "unitCode": "PPM"
  },
  
  "tamperAlert": {
    "type": "Property",
    "value": false
  },
  
  "malfunctionAlert": {
    "type": "Property",
    "value": false
  },
  
  "moistureLevel": {
    "type": "Property",
    "value": 0.45,  // 0.0 to 1.0
    "unitCode": "C62"
  },
  
  "lastEmptyingDate": {
    "type": "Property",
    "value": "2026-05-08T06:30:00Z"
  },
  
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [-8.3879, 43.3734]
    }
  },
  
  "source": {
    "type": "Property",
    "value": "iot-agent-mqtt"  // Data collection source
  }
}
```

#### Attribute Table
| Attribute | NGSI-LD Type | Static/Dynamic | Notes |
|-----------|--------------|----------------|-------|
| id | Identifier | Static | Observation URN |
| type | Type | Static | Must be `WasteObserved` |
| refContainer | Relationship | Static | Link to the source container |
| dateObserved | Property | Dynamic | Timestamp of the observation |
| fillLevel | Property | Dynamic | 0.0 to 1.0 percentage fraction |
| temperature | Property | Dynamic | Environmental temperature |
| methaneLevel | Property | Dynamic | Optional gas sensor reading |
| tamperAlert | Property | Dynamic | Boolean tamper indicator |
| malfunctionAlert | Property | Dynamic | Boolean malfunction indicator |
| moistureLevel | Property | Dynamic | Environmental moisture reading |
| lastEmptyingDate | Property | Dynamic | Updated when the container is serviced |
| location | GeoProperty | Dynamic | Usually copied from the container for convenience |
| source | Property | Static | Ingestion source or adapter name |

---

### 3. WasteContainerIsle

Grouping of waste containers in a geographic zone.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteContainerIsle:coruna-isle-01",
  "type": "WasteContainerIsle",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    "https://smartdatamodels.org/extra/ngsi-ld_waste-container-isle.jsonld",
    {
      "coruña-waste": "urn:ngsi-ld:coruña-waste:"
    }
  ],
  
  "name": {
    "type": "Property",
    "value": "Praza Xeneral Franco Zone 01"
  },
  
  "description": {
    "type": "Property",
    "value": "Collection zone in downtown A Coruña"
  },
  
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Polygon",
      "coordinates": [[
        [-8.3900, 43.3700],
        [-8.3850, 43.3700],
        [-8.3850, 43.3750],
        [-8.3900, 43.3750],
        [-8.3900, 43.3700]
      ]]
    }
  },
  
  "hasContainers": {
    "type": "Relationship",
    "object": [
      "urn:ngsi-ld:WasteContainer:coruna-001",
      "urn:ngsi-ld:WasteContainer:coruna-002",
      "urn:ngsi-ld:WasteContainer:coruna-003"
    ]
  },
  
  "collectionSchedule": {
    "type": "Property",
    "value": {
      "monday": "06:30",
      "wednesday": "06:30",
      "friday": "06:30"
    }
  },
  
  "areaServed": {
    "type": "Property",
    "value": "Downtown"
  },
  
  "address": {
    "type": "Property",
    "value": "Praza Xeneral Franco, A Coruña, Spain"
  },
  
  "municipalityCode": {
    "type": "Property",
    "value": "15030"
  },
  
  "status": {
    "type": "Property",
    "value": "operational"
  }
}
```

#### Attribute Table
| Attribute | NGSI-LD Type | Static/Dynamic | Notes |
|-----------|--------------|----------------|-------|
| id | Identifier | Static | URN for the isle |
| type | Type | Static | Must be `WasteContainerIsle` |
| name | Property | Static | Human-readable zone name |
| description | Property | Static | Optional descriptive text |
| location | GeoProperty | Static | Polygon boundary for the zone |
| hasContainers | Relationship | Mostly static | Membership changes only when containers move |
| collectionSchedule | Property | Mostly static | Weekly collection definition |
| areaServed | Property | Static | District or neighborhood name |
| address | Property | Static | Display address or centroid label |
| municipalityCode | Property | Static | Municipal administrative code |
| status | Property | Dynamic | operational, maintenance, inactive |

---

### 4. WasteContainerModel

Technical specifications and capabilities of container types.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteContainerModel:model-wheelbin-240l",
  "type": "WasteContainerModel",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    "https://smartdatamodels.org/extra/ngsi-ld_waste-container-model.jsonld",
    {
      "coruña-waste": "urn:ngsi-ld:coruña-waste:"
    }
  ],
  
  "name": {
    "type": "Property",
    "value": "Wheelbin 240L Standard"
  },
  
  "manufacturer": {
    "type": "Property",
    "value": "Remondis"
  },
  
  "modelName": {
    "type": "Property",
    "value": "REM-WB240-STD"
  },
  
  "containerType": {
    "type": "Property",
    "value": "wheelbin"
  },
  
  "capacity": {
    "type": "Property",
    "value": 240,
    "unitCode": "LTR"
  },
  
  "weight": {
    "type": "Property",
    "value": 35,
    "unitCode": "KGM"
  },
  
  "dimensions": {
    "type": "Property",
    "value": {
      "length": 1.2,  // meters
      "width": 0.77,
      "height": 1.1
    }
  },
  
  "sensors": {
    "type": "Property",
    "value": [
      "ultrasonic_distance",
      "temperature",
      "tamper_detection"
    ]
  },
  
  "communicationProtocol": {
    "type": "Property",
    "value": "mqtt"  // "mqtt", "coap", "http"
  },
  
  "batteryLife": {
    "type": "Property",
    "value": 24,  // months
    "unitCode": "MON"
  },
  
  "warranty": {
    "type": "Property",
    "value": 60,  // months
    "unitCode": "MON"
  }
}
```

#### Attribute Table
| Attribute | NGSI-LD Type | Static/Dynamic | Notes |
|-----------|--------------|----------------|-------|
| id | Identifier | Static | URN for the model |
| type | Type | Static | Must be `WasteContainerModel` |
| name | Property | Static | Display name for the catalog entry |
| manufacturer | Property | Static | Vendor or brand name |
| modelName | Property | Static | Technical catalog name |
| containerType | Property | Static | Physical family or waste category |
| capacity | Property | Static | Capacity in liters |
| weight | Property | Static | Container weight in kg |
| dimensions | Property | Static | Physical dimensions object |
| sensors | Property | Static | Supported sensor list |
| communicationProtocol | Property | Static | mqtt, coap, or http |
| batteryLife | Property | Static | Expected battery duration in months |
| warranty | Property | Static | Warranty duration in months |

---

## Cross-Sector Smart Data Models References

The project aligns with the following FIWARE Smart Data Models and adjacent semantic vocabularies.

### StandardizedDataModels
| Model | Reference | Usage |
|-------|-----------|-------|
| **WasteContainer** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-container.jsonld) | Main collection entity |
| **WasteContainerIsle** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-container-isle.jsonld) | Zoning and grouping |
| **WasteContainerModel** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-container-model.jsonld) | Technical specs |
| **WasteObserved** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-observed.jsonld) | Real-time data |

### Cross-Sector Alignment

- schema.org for name, description, address, areaServed, and manufacturer fields.
- SAREF4ENVI and SOSA for temperature, moisture, methane, and sensor-observation semantics.
- Civic and administrative vocabularies for address and municipal references.
- Organization semantics for operators and service providers.
- Point-of-interest semantics for spatial container and isle location.

---

## Static vs Dynamic Attributes

### Update Strategy
```
┌─────────────────────────────────────────────┐
│      Device Sensor Reading                  │
│      (Every 5-15 minutes)                   │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│   IoT Agent (MQTT/CoAP/HTTP)                │
│   Protocol Translation & Mapping            │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│   Orion Context Broker                      │
│   Entity Update (NGSI-LD POST /entities)    │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│   QuantumLeap                               │
│   Time-Series Persistence (PostgreSQL)      │
└─────────────────────────────────────────────┘
```

---

## JSON-LD Context

All entities use the layered @context strategy described above. A concrete entity payload may look like this:

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    "https://smartdatamodels.org/extra/ngsi-ld_waste-container.jsonld",
    {
      "coruña-waste": "urn:ngsi-ld:coruña-waste:"
    }
  ]
}
```

---

## Example NGSI-LD Queries

### 1. Get All High Fill Level Containers
```bash
curl -X GET \
  'http://localhost:1026/ngsi-ld/v1/entities?type=WasteObserved&q=fillLevel%3E%3D0.8'
```

### 2. Get Containers in Geographic Area
```bash
curl -X GET \
  'http://localhost:1026/ngsi-ld/v1/entities?type=WasteContainer&georel=within&geometry=Polygon&coordinates=...'
```

### 3. Get Historical Data from QuantumLeap
```bash
curl -X GET \
  'http://localhost:8668/v2/entities/urn:ngsi-ld:WasteContainer:coruna-001/attrs/fillLevel?type=WasteContainer'
```

---

## Extensibility & Future Models

### Planned Extensions
- **Vehicle**: Collection truck metadata
- **Route**: Optimized route plans
- **CollectionService**: Service availability and SLA
- **EnvironmentalMetrics**: CO2 tracking per route
- **IncidentReport**: Citizen-reported issues

### Extension Pattern
```json
{
  "id": "urn:ngsi-ld:CustomEntity:example",
  "type": "CustomEntity",
  "customAttribute": {
    "type": "Property",
    "value": "...",
    "wasteManagement:customMetadata": "value"
  }
}
```

---

## References & Standards

- **ETSI NGSI-LD**: https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.08.01_60/
- **JSON-LD**: https://www.w3.org/TR/json-ld/
- **Smart Data Models**: https://smartdatamodels.org/
- **FIWARE Documentation**: https://fiware-developer.readthedocs.io/

---

**Document Version History:**
| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 1.0 | May 2026 | Data Architect | Initial specification |


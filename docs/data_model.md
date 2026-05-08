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

## NGSI-LD Entity Models

### 1. WasteContainer

Represents a physical waste collection point.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteContainer:coruna-001",
  "type": "WasteContainer",
  "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
  
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

#### Static Attributes
| Attribute | Type | Description | Multiplicity |
|-----------|------|-------------|--------------|
| id | URI | Unique identifier | 1 |
| type | String | "WasteContainer" | 1 |
| name | Property | Container display name | 1 |
| description | Property | Descriptive text | 0..1 |
| containerType | Property | Waste type | 1 |
| location | GeoProperty | Geographic coordinates | 1 |
| capacity | Property | Container capacity (liters) | 1 |
| isleId | Relationship | Parent isle reference | 0..1 |
| modelId | Relationship | Container model reference | 1 |
| installationDate | Property | ISO8601 date | 1 |
| status | Property | Operational status | 1 |
| municipalityCode | Property | Municipal code (DANE) | 1 |
| hasOperator | Relationship | Operator organization | 0..1 |

#### Dynamic Attributes
See `WasteObserved` model for real-time measurements.

---

### 2. WasteObserved

Real-time observations from waste containers.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteObserved:coruna-001-2026-05-08T15:30:00Z",
  "type": "WasteObserved",
  "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
  
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

#### Dynamic Attributes (Real-Time)
| Attribute | Type | Unit | Range | Update Frequency |
|-----------|------|------|-------|------------------|
| fillLevel | Float | % | 0-1 | 5 min |
| temperature | Float | °C | -10 to 60 | 5 min |
| methaneLevel | Float | ppm | 0-1000 | 15 min |
| tamperAlert | Boolean | - | true/false | 1 min |
| malfunctionAlert | Boolean | - | true/false | 1 min |
| moistureLevel | Float | % | 0-1 | 15 min |
| lastEmptyingDate | DateTime | - | - | On collection |
| location | Point | - | - | 1 hour |

---

### 3. WasteContainerIsle

Grouping of waste containers in a geographic zone.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteContainerIsle:coruna-isle-01",
  "type": "WasteContainerIsle",
  "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
  
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

#### Attributes
| Attribute | Type | Description |
|-----------|------|-------------|
| name | Property | Isle identifier |
| location | GeoProperty | Geographic boundary (Polygon) |
| hasContainers | Relationship | List of containers in isle |
| collectionSchedule | Property | Weekly collection times |
| areaServed | Property | District or area name |
| address | Property | Street address |

---

### 4. WasteContainerModel

Technical specifications and capabilities of container types.

#### Entity Definition
```json
{
  "id": "urn:ngsi-ld:WasteContainerModel:model-wheelbin-240l",
  "type": "WasteContainerModel",
  "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
  
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

#### Attributes
| Attribute | Type | Description |
|-----------|------|-------------|
| name | Property | Model name |
| manufacturer | Property | Manufacturer name |
| capacity | Property | Volume in liters |
| weight | Property | Weight in kg |
| dimensions | Property | Physical dimensions |
| sensors | Property | List of available sensors |
| communicationProtocol | Property | IoT protocol used |
| batteryLife | Property | Expected battery duration |

---

## Cross-Sector Smart Data Models References

The project aligns with the following FIWARE Smart Data Models:

### StandardizedDataModels
| Model | Reference | Usage |
|-------|-----------|-------|
| **WasteContainer** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-container.jsonld) | Main collection entity |
| **WasteContainerIsle** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-container-isle.jsonld) | Zoning and grouping |
| **WasteContainerModel** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-container-model.jsonld) | Technical specs |
| **WasteObserved** | [Smart Data Models](https://smartdatamodels.org/extra/ngsi-ld_waste-observed.jsonld) | Real-time data |

### Related Domains
- **Civic** → Address, Organization
- **Device** → Sensor capabilities, Battery status
- **PointOfInterest** → Location context
- **Organization** → Service providers, Operators

---

## Static vs Dynamic Attributes

### Static Attributes (Rarely Change)
- Container ID, type, capacity
- Physical location, dimensions
- Installation date
- Operator information

### Dynamic Attributes (Real-Time)
- Fill level (updated every 5 minutes)
- Temperature, humidity
- Tamper/malfunction alerts
- Last collection timestamp
- Container health status

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

All entities use the following @context:

```json
{
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://w3id.org/smartdatamodels/context.jsonld",
    {
      "wasteManagement": "https://example.com/smartcity/waste/ontology#"
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


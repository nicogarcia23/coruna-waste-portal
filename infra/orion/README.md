Orion subscription registration

This folder contains subscription payloads used to register Orion-LD subscriptions
for Phase 2. The docker-compose service `orion-subscriber` will post each JSON file
in `infra/orion/subscriptions` to the Orion broker on startup.

Files:
- `wasteobserved-to-quantumleap.json`: notifies QuantumLeap for time-series ingestion
- `wastecontainer-updates.json`: notifies backend hook for container updates

The one-shot container uses `curl` and will retry according to Docker service
restart policy (currently disabled). You can run the registration manually with:

```sh
curl -X POST http://localhost:1026/ngsi-ld/v1/subscriptions -H 'Content-Type: application/ld+json' -d @wasteobserved-to-quantumleap.json
```

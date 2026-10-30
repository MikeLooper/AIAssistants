---
type: llm
focus: trace
weight: 1
---

ISupplierService and SupplierService exist in Pilot.Services; SupplierService takes ISupplierRepository as a constructor parameter, and its public methods take and return SupplierDto, not SupplierEntity.

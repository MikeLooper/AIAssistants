# Unit Test Logic Assessment Report (Sample: Detailed)

## Classes

| Code class name |
|---|
| OrderService |
| PricingEngine |
| InventoryAllocator |
| PaymentGatewayClient |

## Class Logic

| Code class name | Name of method or property | Type of element | Logic branch summary |
|---|---|---|---|
| OrderService | SubmitOrder | Method | returns validation error when cart is empty |
| OrderService | SubmitOrder | Method | creates order when cart contains at least one line item |
| OrderService | SubmitOrder | Method | rejects order when customer account is suspended |
| PricingEngine | CalculateTotal | Method | applies tax when taxable flag is true |
| PricingEngine | CalculateTotal | Method | bypasses tax when taxable flag is false |
| InventoryAllocator | Allocate | Method | returns backorder when stock is insufficient |

## Unit Test Classes

| Unit test class name | Code class name |
|---|---|
| OrderServiceTests | OrderService |
| PricingEngineTests | PricingEngine |

## Unit Test Elements

| Unit test class name | Related code class name | Name of test method | Name of code class method or property that is being tested by the test method |
|---|---|---|---|
| OrderServiceTests | OrderService | SubmitOrder_EmptyCart_ReturnsValidationError | SubmitOrder |
| OrderServiceTests | OrderService | SubmitOrder_WithValidCart_CreatesOrder | SubmitOrder |
| PricingEngineTests | PricingEngine | CalculateTotal_Taxable_AppliesTax | CalculateTotal |

## Tested Class Elements

| Code class name | Unit test class name | Name of method or property | Type of element |
|---|---|---|---|
| OrderService | OrderServiceTests | SubmitOrder | Method |
| PricingEngine | PricingEngineTests | CalculateTotal | Method |

## Untested Classes

| Code class name |
|---|
| InventoryAllocator |
| PaymentGatewayClient |

## Not Tested Class Elements

| Code class name | Unit test class name | Name of method or property | Type of element |
|---|---|---|---|
| OrderService | OrderServiceTests | CancelOrder | Method |
| OrderService | OrderServiceTests | LastProcessedOrderId | Property |
| PricingEngine | PricingEngineTests | ApplyPromotions | Method |

## Logic Covered

| Code class name | Unit test class name | Name of method or property | Type of element | Logic branch summary |
|---|---|---|---|---|
| OrderService | OrderServiceTests | SubmitOrder | Method | returns validation error when cart is empty |
| OrderService | OrderServiceTests | SubmitOrder | Method | creates order when cart contains at least one line item |
| PricingEngine | PricingEngineTests | CalculateTotal | Method | applies tax when taxable flag is true |

## Logic Not Covered

| Code class name | Unit test class name | Name of method or property | Type of element | Logic branch summary |
|---|---|---|---|---|
| OrderService | OrderServiceTests | SubmitOrder | Method | rejects order when customer account is suspended |
| PricingEngine | PricingEngineTests | CalculateTotal | Method | bypasses tax when taxable flag is false |
| InventoryAllocator | InventoryAllocatorTests | Allocate | Method | returns backorder when stock is insufficient |

## Summary

### Untested Class Percent

| Metric | Value |
|---|---|
| Untested Class Percent | 50.00% |

### Untested Element Percent (Per Class)

| Code class name | Untested Element Percent |
|---|---|
| OrderService | 40.00% |
| PricingEngine | 25.00% |
| InventoryAllocator | N/A |

Reason for N/A: class has no related unit test class.

### Overall Untested Elements Percent

| Metric | Value |
|---|---|
| Overall Untested Elements Percent | 36.36% |

### Logic Not Covered Percent (Per Class)

| Code class name | Logic Not Covered Percent |
|---|---|
| OrderService | 33.33% |
| PricingEngine | 50.00% |
| InventoryAllocator | 100.00% |

## Diagnostics Appendix (Optional)

### Unresolved Test-to-Element Mappings
- `OrderServiceTests.SubmitOrder_SuspensionCase_UsesFixtureOnly`: setup references `OrderService`, no explicit assertion tied to `SubmitOrder` suspended branch.

### Skipped Files
- `generated/AutoMapperConfig.g.cs`: generated file excluded by policy.

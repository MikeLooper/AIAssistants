# Unit Test Logic Assessment Report (Sample: Standard)

## Untested Classes

| Code class name |
|---|
| PaymentGatewayClient |
| LegacyDiscountPolicy |

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
| OrderService | OrderServiceTests | CancelOrder | Method | no-op when order is already cancelled |
| PricingEngine | PricingEngineTests | CalculateTotal | Method | bypasses tax when taxable flag is false |

## Summary

### Untested Class Percent

| Metric | Value |
|---|---|
| Untested Class Percent | 33.33% |

### Untested Element Percent (Per Class)

| Code class name | Untested Element Percent |
|---|---|
| OrderService | 40.00% |
| PricingEngine | 25.00% |
| InventoryAllocator | N/A |

Reason for N/A: no discovered class elements for InventoryAllocator.

### Overall Untested Elements Percent

| Metric | Value |
|---|---|
| Overall Untested Elements Percent | 31.25% |

### Logic Not Covered Percent (Per Class)

| Code class name | Logic Not Covered Percent |
|---|---|
| OrderService | 50.00% |
| PricingEngine | 33.33% |
| InventoryAllocator | N/A |

Reason for N/A: no discovered logic branches for InventoryAllocator.

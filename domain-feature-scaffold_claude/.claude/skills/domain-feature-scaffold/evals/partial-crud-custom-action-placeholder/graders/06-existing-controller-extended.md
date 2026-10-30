---
type: llm
focus: trace
weight: 1
---

CustomersController still takes ICustomerService and now also takes ICustomerNoteService as a constructor parameter; its existing GetAll and GetById actions are unchanged.

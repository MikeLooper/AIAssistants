---
type: llm
focus: trace
weight: 1
---

A Bruno collection (bruno.json, an environment defining baseUrl) contains a Supplier folder with one request per new endpoint (POST, GET by id, GET list, PUT, DELETE), each with a tests block asserting the status code from the action mapping, and a 404 check for a missing or deleted id.

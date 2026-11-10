# Reliability config signals

Local lookup table, not a standard. Use it for the remote-call rule (`SKILL.md` step 2), the circuit-breaker rule
(step 5), the deployment-config rule (step 7) and REL-04 … REL-08 evidence; cite the AZRL elements, never this file.
If a hosting, mesh, gateway or broker setting isn't listed, apply the closest row only when it clearly fits; otherwise
add `localized-standard-gap: unrecognized config <setting>` to `notes`.

"Deployment config in scope" means at least one file in the subject's list matches a cell in the **Deployable service
present** row.

| Signal | Azure (Bicep / ARM / Terraform `azurerm`) | AWS | GCP | Kubernetes / mesh / gateway |
|---|---|---|---|---|
| Deployable service present (step 7) | App Service, Container Apps, Functions, AKS, VM scale sets | ECS, EKS, Lambda, Auto Scaling group, Elastic Beanstalk | Cloud Run, GKE, managed instance group, App Engine | `Deployment`, `StatefulSet`, Helm charts |
| Instance count ≥ 2 (AZRL-27) | App Service plan `capacity` / `sku.capacity`; Container Apps `minReplicas`; VMSS `capacity`; autoscale `minimum`; Functions Consumption / Flex (platform-managed) | ECS `desired_count`; ASG `min_size`; Lambda (platform-managed) | Cloud Run `min_instance_count` (0 = scale to zero, platform-managed); MIG target size | `spec.replicas`; HPA `minReplicas` |
| Zones / failure domains (AZRL-48) | `zoneRedundant: true` (App Service plan, Container Apps environment, SQL, Service Bus Premium); Redis `zones`; VMSS `zones` | subnets in ≥ 2 AZs for ASG / ECS; RDS `multi_az`; ElastiCache `multi_az_enabled` | regional MIG; GKE regional cluster | `topologySpreadConstraints` on `topology.kubernetes.io/zone`; `podAntiAffinity` on `kubernetes.io/hostname` |
| Health-probe routing (AZRL-49) | App Service `healthCheckPath`; Application Gateway / Front Door probes; Load Balancer probes; Container Apps readiness probes | ALB / NLB target-group `health_check` | backend service health check; Cloud Run startup probes | `readinessProbe`; `startupProbe` |
| Auto-restart (AZRL-50) | App Service auto-heal; Container Apps liveness probes; VMSS automatic instance repairs | ECS health-check replacement; ASG health checks | MIG auto-healing; Cloud Run liveness probes | `livenessProbe`; `restartPolicy` |
| HA stateful tier (AZRL-51) | SQL zone redundancy / Business Critical / failover-group listener (in-region part); Cosmos DB zone redundancy; Redis Premium / Enterprise with zones; Service Bus Premium | RDS Multi-AZ; Aurora replicas; ElastiCache automatic failover | Cloud SQL `availability_type = "REGIONAL"`; Memorystore `STANDARD_HA` | StatefulSet with ≥ 2 replicas and operator-managed failover |
| Automated scaling (AZRL-52) | `Microsoft.Insights/autoscalesettings` / `azurerm_monitor_autoscale_setting`; Container Apps scale rules | target-tracking / step scaling policies | MIG autoscaler; Cloud Run autoscaling | HPA; KEDA `ScaledObject` |
| Graceful shutdown (AZRL-44) | Container Apps `terminationGracePeriodSeconds`; Functions drain mode | ECS `stopTimeout` | Cloud Run (SIGTERM, 10 s grace) | `terminationGracePeriodSeconds`; `preStop` hook |
| Dead-lettering and delivery limits (AZRL-39) | Service Bus `maxDeliveryCount`, `deadLetteringOnMessageExpiration`; Storage Queue poison queue (Functions) | SQS `redrive_policy` `maxReceiveCount`; SNS / Lambda DLQ or on-failure destination | Pub/Sub `dead_letter_policy.max_delivery_attempts` | RabbitMQ `x-dead-letter-exchange`; Kafka dead-letter topics |
| Platform breakers, retries and timeouts (AZRL-05, AZRL-21, step 2) | API Management `retry` policy / backend circuit breaker; Dapr resiliency spec | App Mesh retry policies | Traffic Director outlier detection | Istio `DestinationRule.trafficPolicy.outlierDetection` / `connectionPool`, `VirtualService` `retries` + `timeout`; Linkerd retries / timeouts; Envoy; Dapr `Resiliency` (`timeouts`, `retries`, `circuitBreakers`) |
| Gateway load limits (AZRL-32, AZRL-35) | API Management `rate-limit-by-key`, `quota-by-key`; Front Door rate-limit rules (edge: security) | API Gateway throttling; WAF rate rules (edge: security) | Cloud Armor rate limiting (edge: security) | ingress-nginx `limit-rps` / `limit-connections`; Kong `rate-limiting`; Envoy local rate limit |

A platform breaker, retry or timeout that the files apply to a dependency is judged in place of app code for that
dependency (steps 2 and 5). A service mesh or Dapr sidecar is a pass signal, not a requirement.

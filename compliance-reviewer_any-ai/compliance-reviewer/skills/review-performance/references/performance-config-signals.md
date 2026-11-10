# Performance config signals

Local lookup table, not a standard. Use it for the multi-instance rule (`SKILL.md` step 4), the config-in-scope rule
(step 5) and PERF-07 / PERF-08 evidence; cite the AZPE elements, never this file. If a hosting or scaling setting isn't
listed, apply the closest row only when it clearly fits; otherwise add
`localized-standard-gap: unrecognized config <setting>` to `notes`.

"Hosting/scaling config in scope" means at least one file in the subject's list matches a cell in the Session
affinity, Autoscale triggers, Resource limits or Compression / HTTP/2 rows.

| Signal | Azure (Bicep / ARM / Terraform `azurerm`) | AWS | GCP | Kubernetes / ingress | App / server config |
|---|---|---|---|---|---|
| Multi-instance evidence (step 4) | App Service plan `capacity` / `sku.capacity` > 1; `Microsoft.Insights/autoscalesettings` / `azurerm_monitor_autoscale_setting`; Container Apps `minReplicas` > 1 or `maxReplicas` > 1; Functions Consumption / Flex / Premium plans | ECS `desired_count` > 1; Auto Scaling group; `aws_appautoscaling_*`; Lambda | Cloud Run `max_instance_count` > 1; managed instance group autoscaler; Cloud Functions | `Deployment` `spec.replicas` > 1; `HorizontalPodAutoscaler`; KEDA `ScaledObject` | gunicorn / uWSGI with several worker processes (process-local caches and sessions aren't shared) |
| Session affinity (scope detection only; affinity is judged by review-twelve-factor TF-06) | App Service `clientAffinityEnabled: true`; Application Gateway `cookieBasedAffinity: 'Enabled'`; Front Door `sessionAffinityState: 'Enabled'` | ALB / ELB target group `stickiness` enabled | backend service `session_affinity` other than `NONE` | Service `sessionAffinity: ClientIP`; ingress-nginx annotation `nginx.ingress.kubernetes.io/affinity: cookie` | — |
| Autoscale triggers (AZPE-44, AZPE-49) | autoscale profile `rules` (`metricTrigger` threshold, `scaleAction` cooldown), `capacity.minimum`; Container Apps `scale.rules` (HTTP, queue, custom) | target-tracking / step scaling policies; SQS-depth-based scaling | autoscaler `cpu_utilization`, `load_balancing_utilization`; Cloud Run `max_instance_request_concurrency`, `min_instance_count` | HPA `metrics`, `minReplicas`, `behavior.scaleDown.stabilizationWindowSeconds`; KEDA queue scalers | — |
| Resource limits (AZPE-50) | Container Apps `resources.cpu` / `memory`; AKS pod specs (see Kubernetes) | ECS task definition `cpu` / `memory` | Cloud Run `resources.limits` | `resources.requests` / `resources.limits` on containers; `LimitRange` | JVM `-Xmx` / `-XX:MaxRAMPercentage`; .NET `GCHeapHardLimit` / `DOTNET_GCHeapHardLimit` |
| Compression / HTTP/2 (AZPE-51) | App Service `siteConfig.http20Enabled`; Front Door route `compressionSettings` / `isCompressionEnabled` | CloudFront `compress = true`; ALB HTTP/2 (on by default) | HTTPS load balancer HTTP/2 | ingress-nginx ConfigMap `use-gzip`, `use-http2` | `AddResponseCompression`; `server.compression.enabled`, `server.http2.enabled`; Django `GZipMiddleware`; nginx `gzip on`, `listen … http2` |
| CDN / static hosting (AZPE-52) | Front Door / CDN profiles; Static Web Apps; storage static website | CloudFront + S3 | Cloud CDN; Firebase Hosting | — | static files served by the app framework with no cache headers or CDN in front (fail signal when assets are significant) |
| Queue workers (AZPE-44, AZPE-53) | Container Apps / Functions with queue scale rules; WebJobs | ECS services or Lambdas triggered by SQS | Cloud Run jobs / Pub/Sub push subscribers | separate `Deployment` for workers; KEDA `ScaledObject` on queue length | a worker pinned to one instance (`replicas: 1` / `maxReplicas: 1`) consuming all of a queue's load is a fail signal for AZPE-53 |

# Monitoring-as-code signals

Local lookup table, not a standard. Use it to classify each file in the subject's list (`SKILL.md` step 2). Only the
resource types and files below count as monitoring-as-code. If a monitoring resource type isn't listed, apply the
closest row only when it clearly fits; otherwise add `localized-standard-gap: unrecognized monitoring resource <type>`
to `notes`.

"Alert rule" and "Dashboard" are the two signals that decide the no-monitoring-as-code rule (`SKILL.md` step 3).

## Resource types per platform

| Signal | Azure (Bicep / ARM / Terraform `azurerm`) | AWS (CloudFormation / Terraform `aws`) | GCP (Terraform `google`) | Kubernetes / Prometheus / Grafana | Datadog (Terraform `datadog`) |
|---|---|---|---|---|---|
| Alert rule | `Microsoft.Insights/metricAlerts`, `Microsoft.Insights/scheduledQueryRules`, `Microsoft.Insights/activityLogAlerts`, `Microsoft.AlertsManagement/prometheusRuleGroups`; `azurerm_monitor_metric_alert`, `azurerm_monitor_scheduled_query_rules_alert_v2`, `azurerm_monitor_activity_log_alert`, `azurerm_monitor_alert_prometheus_rule_group` | `AWS::CloudWatch::Alarm`, `AWS::CloudWatch::CompositeAlarm`; `aws_cloudwatch_metric_alarm`, `aws_cloudwatch_composite_alarm`, `aws_prometheus_rule_group_namespace` | `google_monitoring_alert_policy` | `PrometheusRule` (prometheus-operator CRD); Prometheus rule files (`groups:` with `alert:` entries, often `*.rules.yml`, `*rules*.yaml`); `grafana_rule_group` | `datadog_monitor` |
| Notification target / routing | `Microsoft.Insights/actionGroups`, `Microsoft.AlertsManagement/actionRules` (alert processing rules); `azurerm_monitor_action_group`, `azurerm_monitor_alert_processing_rule_*` | `AWS::SNS::Topic` / `AWS::SNS::Subscription` used as alarm actions; `aws_sns_topic`, `aws_sns_topic_subscription`, `aws_prometheus_alert_manager_definition` | `google_monitoring_notification_channel` | `alertmanager.yml` / `alertmanager*.yaml` (`route`, `receivers`, `inhibit_rules`), `AlertmanagerConfig` CRD; `grafana_contact_point`, `grafana_notification_policy` | `@` notify handles in `datadog_monitor` messages |
| Dashboard | `Microsoft.Portal/dashboards`, `Microsoft.Insights/workbooks`, `Microsoft.Dashboard/grafana`; `azurerm_portal_dashboard`, `azurerm_application_insights_workbook`, `azurerm_dashboard_grafana` | `AWS::CloudWatch::Dashboard`; `aws_cloudwatch_dashboard` | `google_monitoring_dashboard` | Grafana dashboard JSON (`"panels"` + `"title"`), `grafana_dashboard`, `GrafanaDashboard` (grafana-operator CRD), ConfigMaps labelled for the Grafana dashboard sidecar | `datadog_dashboard`, `datadog_dashboard_json` |
| Probe / availability test | `Microsoft.Insights/webtests`; `azurerm_application_insights_standard_web_test`; Network Watcher connection monitors | `AWS::Synthetics::Canary`, `AWS::Route53::HealthCheck`; `aws_synthetics_canary`, `aws_route53_health_check` | `google_monitoring_uptime_check_config` | `Probe` (prometheus-operator CRD) / blackbox-exporter config | `datadog_synthetics_test` |
| Diagnostic routing | `Microsoft.Insights/diagnosticSettings`; `azurerm_monitor_diagnostic_setting`; Azure Policy assignments with `deployIfNotExists` for diagnostic settings | CloudWatch Logs subscription filters, `aws_flow_log`, `aws_cloudtrail`; container/agent log configuration | `google_logging_project_sink` (and folder/org sinks) | `ServiceMonitor` / `PodMonitor` CRDs, scrape configs, OpenTelemetry Collector / agent config | Datadog agent / integration config |
| Platform-health alert | `activityLogAlerts` with category `ServiceHealth` or `ResourceHealth` | EventBridge rule (`AWS::Events::Rule`, `aws_cloudwatch_event_rule`) with `source: aws.health` | Alert policy on Personalized Service Health events | — | — |
| SLO definition | Stated in docs, tags or alert-rule descriptions | `AWS::ApplicationSignals::ServiceLevelObjective` | `google_monitoring_slo` | OpenSLO or Sloth specs (`PrometheusServiceLevel`), SLO recording rules | `datadog_service_level_objective` |
| Telemetry store | `Microsoft.OperationalInsights/workspaces` (`retentionInDays`), `Microsoft.Insights/components`, `Microsoft.Monitor/accounts`; `azurerm_log_analytics_workspace`, `azurerm_application_insights`; resource locks on these | `aws_cloudwatch_log_group` (`retention_in_days`), `aws_prometheus_workspace` | `google_logging_project_bucket_config` (`retention_days`) | Prometheus / Loki / Tempo / Mimir retention settings, persistent volumes for them | — |

## Other files that count

- CI steps that validate monitoring config (e.g. `promtool check rules`, `promtool test rules`, `amtool check-config`, rule unit-test files): MON-02 evidence (SREM-08).
- Self-hosted monitoring stack manifests or Helm values (Prometheus, Alertmanager, Grafana, Loki, OpenTelemetry Collector): MON-06 evidence (WAFM-38, SREM-27, SREM-28).

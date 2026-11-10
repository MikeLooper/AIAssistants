# Language Signals — Python (Reliability)

Local lookup table, not a standard. Use it to classify code and configuration for REL-01 … REL-08; cite the AZRL elements, never this file. If a library isn't listed and you can't classify it, add `localized-standard-gap: unrecognized library <name>` to `notes`.

## Default timeouts (AZRL-01, SKILL.md step 3)

| Client | Default timeout | AZRL-01 |
|---|---|---|
| `requests` | none | **fail** unless `timeout=` is passed (or a session/adapter wrapper sets it) |
| `urllib.request`, `http.client` | none (global socket default) | **fail** unless `timeout=` is passed or `socket.setdefaulttimeout` is set |
| `httpx` | 5 s | pass with note; `timeout=None` fails |
| `aiohttp` | total 300 s (`ClientTimeout`) | pass with note; `ClientTimeout(total=None)` with no other limits fails |
| `psycopg2` / `psycopg` | connect: none; statement: none | **fail** unless `connect_timeout` / `statement_timeout` (connection `options`) is set |
| SQLAlchemy | `pool_timeout` 30 s (pool acquisition only) | doesn't cover query time |
| `redis-py` | socket timeout: none | **fail** unless `socket_timeout` is set |
| boto3 / botocore | connect 60 s, read 60 s; built-in retry on | pass with note |
| Azure SDK for Python (azure-core) | connection 300 s, read 300 s; built-in retry on | pass with note |

## Signals

| Area | Pass signals | Anti-patterns / fail signals |
|---|---|---|
| Retries (REL-02) | `tenacity` (`stop_after_attempt`, `wait_random_exponential`, `retry_if_exception_type`); `urllib3.Retry(total, backoff_factor, status_forcelist, respect_retry_after_header=True)` on an `HTTPAdapter`; `backoff` library; botocore `retries={"mode": "standard" / "adaptive"}`; Celery `autoretry_for` + `retry_backoff` + `retry_jitter` + `max_retries` | `while True:` retry loops; bare `except:` / `except Exception:` + retry; `time.sleep(1)` fixed delays with many attempts; tenacity `@retry` without `stop=` (retries forever) |
| Idempotency (REL-03) | `urllib3.Retry` default `allowed_methods` (excludes POST); idempotency key created once | `allowed_methods=None` or including POST on non-idempotent endpoints without a key |
| Circuit breakers (REL-04) | `pybreaker` / `circuitbreaker` / `aiobreaker` breaker at module level per dependency | breaker created inside the request function |
| Isolation and load (REL-06) | `asyncio.Semaphore` per dependency; `slowapi` / `limits` rate limiting; fallback for optional calls | converting downstream 429/503 to 500 |
| Messaging and jobs (REL-07) | Celery `acks_late=True` + `task_reject_on_worker_lost=True` for tasks that must not be lost, with idempotent tasks; broker DLQ (SQS redrive, RabbitMQ DLX); Kafka `enable_auto_commit=False` + commit after processing; APScheduler `max_instances=1` + `coalesce` with a lock in multi-instance deployments; `SIGTERM` handler / gunicorn `graceful_timeout` | Celery default early ack (`task_acks_late` disabled) on non-idempotent long tasks that must not be lost; `queue.Queue` / in-memory lists as the only buffer for must-not-lose work; cron jobs on every replica without a lock |

# otel-postgres-demo
#  OpenTelemetry + PostgreSQL Observability Demo

This project demonstrates **two methods** to collect telemetry from PostgreSQL using **OpenTelemetry**, visualized through **Jaeger** (for traces) and **Prometheus** (for metrics). It is built to run fully inside **GitHub Codespaces** using Docker Compose — no local setup required.

---

##  What You'll Learn

- How to auto-instrument PostgreSQL queries in a Python app (client-side tracing)
- How to collect PostgreSQL metrics via `postgres_exporter` (server-side metrics)
- How to send data to OpenTelemetry Collector and visualize using Jaeger & Prometheus

---

##  Project Structure

```bash
otel-postgres-demo/
│
├── app/
│   └── main.py                  # Flask app with PostgreSQL query (Method 1)
│
├── .devcontainer/
│   └── devcontainer.json        # GitHub Codespaces setup
│
├── otel-collector-config.yml    # Config for OpenTelemetry Collector
├── docker-compose.yml           # Spins up all required services
├── requirements.txt             # Python dependencies
└── README.md                    # You’re here
```

---

##  Services Spun Up via Docker Compose

| Service            | Role                                                           |
|--------------------|----------------------------------------------------------------|
| `flask-app`        | Python app w/ OTel-instrumented DB client (psycopg2)           |
| `postgres`         | PostgreSQL database                                            |
| `postgres-exporter`| Exposes DB metrics to Prometheus                              |
| `otel-collector`   | Central OTel telemetry collector (traces + metrics)            |
| `jaeger`           | Observability backend for viewing traces                       |

---

##  Running This Project (GitHub Codespaces)

>  You can run this entire setup **without installing anything locally** using GitHub Codespaces.

### Step 1: Launch Codespace

1. Fork or clone this repo.
2. Open it in GitHub Codespaces.
3. Run the following command to spin up all services:

```bash
docker-compose up --build
```

You should see logs like:

```bash
flask-app        | * Running on http://0.0.0.0:5000
otel-collector   | Everything is ready. Begin collecting!
```

---

##  Method 1: Client-Side Tracing via OpenTelemetry SDK

The app connects to PostgreSQL using an OTel-instrumented client (`psycopg2`). It auto-generates spans that trace query duration and attaches them to the overall trace context.

### Why Use This?

- Correlates database query latency with user-facing endpoints
- Helps root-cause slowdowns (`/checkout is slow → 2s JOIN query`)

###  Steps

1. **Install Dependencies** (handled by Dockerfile)

   ```bash
   pip install opentelemetry-sdk opentelemetry-instrumentation-psycopg2
   ```

2. **Run the App**

   Open a terminal in Codespaces and trigger a request:

   ```bash
   curl http://localhost:5000/
   ```

   Expected response:
   ```json
   { "message": "Randoli loves observability!" }
   ```

3. **View Traces**

   - Open Jaeger UI: [http://localhost:16686](http://localhost:16686)
   - Look under `flask-app` service to inspect traces from PostgreSQL query

---

##  Method 2: Server-Side Metrics via Prometheus Exporter

This approach collects PostgreSQL internal metrics like query counts, slow queries, cache hits, etc., via `postgres_exporter`.

###  Why Use This?

- Gives macro-level visibility (e.g., cache hit ratio, active connections)
- Complements trace-level info with system-wide DB metrics

###  Steps

1. **Run `postgres_exporter`**

   It exposes metrics at: [http://localhost:9187/metrics](http://localhost:9187/metrics)

   Sample output:
   ```
   pg_stat_database_xact_commit{datname="demo"} 104  
   pg_stat_activity_count{state="active"} 3
   ```

2. **Configure OpenTelemetry Collector**

   The `otel-collector-config.yml` is already set to scrape from the exporter and send metrics to Prometheus (or other OTLP-compatible backends).

3. **Verify Metrics**

   - View raw metrics at: [http://localhost:9187/metrics](http://localhost:9187/metrics)
   - Hook into Grafana or any Prometheus frontend for dashboards

---

##  Demo Visuals

You can view:

-  Trace visualizations in **Jaeger** (`localhost:16686`)
-  Metrics exposed from **PostgreSQL Exporter** (`localhost:9187/metrics`)

Screenshots included in the `demo/` folder.
## Jaeger UI (Client-Side Instrumentation - Method 1)

This shows the OpenTelemetry traces from PostgreSQL queries captured via Flask client instrumentation:

![Jaeger Screenshot](./demo/Jaeger%20Screenshot.jpeg)

---

## Prometheus Metrics (Server-Side Monitoring - Method 2)

PostgreSQL exported metrics collected via OpenTelemetry Collector and Prometheus:

![Prometheus Screenshot](./demo/prometheus%20Screenshot.png)

---

##  What You Achieved

###  With Method 1 (Client-Side Tracing)
- Captured individual PostgreSQL queries as spans
- Linked DB performance to HTTP endpoints

###  With Method 2 (Server-Side Metrics)
- Monitored PostgreSQL health at system level
- Gained insight into active queries, buffer usage, cache hits

---

##  Please Note 

- This project is built to run inside **Codespaces**, so your local machine stays clean.
- If you're running locally instead, ensure you have Docker and Python 3.8+ installed.
- If Codespace is deleted, your data/config is lost unless

from flask import Flask
import psycopg2
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
Psycopg2Instrumentor().instrument()

# OpenTelemetry Setup
provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "demo-flask"}))
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
provider.add_span_processor(processor)
set_tracer_provider(provider)

@app.route("/users")
def users():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="db")
    cur = conn.cursor()
    cur.execute("SELECT 'Randoli loves observability!'")
    result = cur.fetchone()
    conn.close()
    return {"message": result[0]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask
import psycopg2
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider

# Set up OpenTelemetry Tracing
provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "demo-flask"}))
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)
set_tracer_provider(provider)

# Create Flask app
app = Flask(__name__)

# Instrument Flask and psycopg2
FlaskInstrumentor().instrument_app(app)
Psycopg2Instrumentor().instrument()

@app.route("/users")
def users():
    try:
        conn = psycopg2.connect(
            dbname="demo", user="demo", password="demo", host= "localhost"
        )
        cur = conn.cursor()
        cur.execute("SELECT 'Randoli loves observability!'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"message": result[0]}
    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

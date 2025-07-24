// frontend/src/tracer.js
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';

const resource = new Resource({
  [SemanticResourceAttributes.SERVICE_NAME]: 'ecommerce-frontend',
});

const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces', // Send traces to the OTel Collector
});

const provider = new WebTracerProvider({ resource });
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));

provider.register({
  contextManager: new ZoneContextManager(),
});

registerInstrumentations({
  instrumentations: [
    new FetchInstrumentation({
      propagateTraceHeaderCorsUrls: [
        'http://localhost:8000/api/products',
        'http://localhost:8000/api/cart/add',
        'http://localhost:8000/api/checkout',
      ],
    }),
  ],
});

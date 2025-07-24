import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { AWSXRayPropagator } from '@opentelemetry/propagator-aws-xray';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';

const provider = new WebTracerProvider({
  contextManager: new ZoneContextManager(),
  propagator: new AWSXRayPropagator(),
});
provider.addSpanProcessor(
  new SimpleSpanProcessor(new OTLPTraceExporter({ url: 'http://collector:4318/v1/traces' }))
);
provider.register();

registerInstrumentations({
  instrumentations: [new FetchInstrumentation({ propagateTraceHeaderCorsUrls: [/\/api\//] })],
});
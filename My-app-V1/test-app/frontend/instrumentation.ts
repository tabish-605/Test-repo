
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({ serviceName: 'next-frontend', exporterConfig: { url: 'http://localhost:4318/v1/traces' } })
}

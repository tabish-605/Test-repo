# ObservaStore - E-commerce Application with OpenTelemetry Observability

A complete full-stack e-commerce application demonstrating comprehensive observability using OpenTelemetry (OTel), with distributed tracing, metrics collection, and structured logging.

## 🏗️ Architecture

- **Frontend**: React application with OpenTelemetry browser instrumentation
- **Backend**: Python FastAPI with comprehensive tracing
- **Database**: PostgreSQL with sample e-commerce data
- **Observability**: OpenTelemetry Collector, Jaeger, Prometheus, Grafana

## 📋 Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available for containers
- Ports 80, 3000, 8000, 9090, 16686 available

## 🚀 Quick Start

1. **Extract and navigate to the project directory**:
   ```bash
   unzip observa-store.zip
   cd observa-store
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Wait for all services to start** (typically 2-3 minutes)

4. **Access the applications**:
   - **E-commerce App**: http://localhost
   - **Jaeger UI (Traces)**: http://localhost:16686
   - **Prometheus (Metrics)**: http://localhost:9090
   - **Grafana (Dashboards)**: http://localhost:3000 (admin/admin)

## 🔍 Testing Observability

1. **Generate some traffic**:
   - Visit http://localhost
   - Browse products
   - Add items to cart
   - Perform checkout (some will fail intentionally)

2. **View traces in Jaeger**:
   - Go to http://localhost:16686
   - Select "ecommerce-frontend" or "ecommerce-api" service
   - Click "Find Traces" to see distributed traces

3. **Check metrics in Prometheus**:
   - Visit http://localhost:9090
   - Query metrics like `http_requests_total`

4. **Setup Grafana dashboards**:
   - Login to http://localhost:3000 (admin/admin)
   - Add Prometheus data source: http://prometheus:9090
   - Add Jaeger data source: http://jaeger:16686

## 📁 Project Structure

```
observa-store/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # API routes
│   │   ├── db.py           # Database connection
│   │   └── instrumentation.py # OpenTelemetry setup
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js         # Main app component
│   │   ├── tracer.js      # OpenTelemetry setup
│   │   └── index.js       # Entry point
│   ├── Dockerfile
│   └── package.json
├── otel-collector/         # OpenTelemetry Collector config
├── prometheus/             # Prometheus configuration
├── postgres/               # Database initialization
├── docker-compose.yml      # Container orchestration
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

You can customize the deployment by modifying the `docker-compose.yml` file:

- **Database credentials**: Update `POSTGRES_USER` and `POSTGRES_PASSWORD`
- **OpenTelemetry endpoint**: Modify `OTEL_EXPORTER_OTLP_ENDPOINT`

### Scaling

To scale individual services:
```bash
docker-compose up --scale backend=3 --scale frontend=2
```

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 80, 3000, 8000, 9090, 16686 are available
2. **Memory issues**: Increase Docker memory limit to at least 4GB
3. **Services not starting**: Check logs with `docker-compose logs [service-name]`

### Useful Commands

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Restart a specific service
docker-compose restart backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📊 Key Observability Features

### Distributed Tracing
- End-to-end request tracing across frontend and backend
- Database query instrumentation
- Error propagation tracking

### Metrics Collection
- HTTP request metrics (count, duration, status codes)
- Custom business metrics (cart operations, checkout success rate)
- System metrics (memory, CPU usage)

### Structured Logging
- Correlated logs with trace IDs
- Structured JSON format
- Multiple log levels (INFO, ERROR, DEBUG)

## 🌐 AWS Deployment

To deploy on AWS:

1. **Push images to ECR**:
   ```bash
   # Build and tag images
   docker build -t observa-store-frontend ./frontend
   docker build -t observa-store-backend ./backend

   # Push to ECR (replace with your registry)
   docker tag observa-store-frontend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/observa-store-frontend:latest
   docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/observa-store-frontend:latest
   ```

2. **Use AWS ECS or EKS** with the provided container configurations

3. **Setup RDS PostgreSQL** and update connection strings

4. **Configure Application Load Balancer** for the frontend and backend services

## 📚 Additional Resources

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

## 🤝 Contributing

This is a demonstration application. For production use, consider:
- Adding authentication and authorization
- Implementing proper error handling
- Adding comprehensive unit and integration tests
- Setting up CI/CD pipelines
- Configuring production-grade security

## 📄 License

This project is for educational and demonstration purposes.

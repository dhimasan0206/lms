# Deployment Guide

## Overview

This guide outlines the deployment process for the API Gateway service in different environments. The service can be deployed using Docker containers or directly on a server.

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (for production)
- Access to container registry
- Environment-specific configuration
- SSL certificates (for production)

## Environment Configuration

### Development Environment
```env
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

### Staging Environment
```env
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
```

### Production Environment
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## Docker Deployment

### 1. Build Docker Image
```bash
# Build the image
docker build -t lms-api-gateway:latest .

# Tag the image for your registry
docker tag lms-api-gateway:latest your-registry/lms-api-gateway:latest
```

### 2. Push to Container Registry
```bash
# Login to registry
docker login your-registry

# Push the image
docker push your-registry/lms-api-gateway:latest
```

### 3. Deploy with Docker Compose
```bash
# Development
docker-compose -f docker-compose.yml up -d

# Staging
docker-compose -f docker-compose.staging.yml up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## Kubernetes Deployment

### 1. Create Kubernetes Secrets
```bash
# Create secrets from .env file
kubectl create secret generic api-gateway-secrets \
  --from-file=.env=./.env.production

# Create Redis secrets
kubectl create secret generic redis-secrets \
  --from-literal=REDIS_PASSWORD=your-redis-password
```

### 2. Deploy Redis
```bash
# Deploy Redis StatefulSet
kubectl apply -f k8s/redis/

# Verify Redis deployment
kubectl get pods -l app=redis
```

### 3. Deploy API Gateway
```bash
# Deploy API Gateway
kubectl apply -f k8s/api-gateway/

# Verify deployment
kubectl get pods -l app=api-gateway
```

### 4. Configure Ingress
```bash
# Deploy ingress
kubectl apply -f k8s/ingress/

# Verify ingress
kubectl get ingress
```

## Deployment Files

### Docker Compose (Development)
```yaml
version: '3.8'

services:
  api-gateway:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    volumes:
      - .:/app
    depends_on:
      - redis

  redis:
    image: redis:6.0
    ports:
      - "6379:6379"
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api-gateway
        image: your-registry/lms-api-gateway:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: api-gateway-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Deployment Checklist

### Pre-deployment
- [ ] Run all tests
- [ ] Update version numbers
- [ ] Update documentation
- [ ] Review security settings
- [ ] Backup current deployment
- [ ] Notify stakeholders

### Deployment
- [ ] Deploy Redis (if needed)
- [ ] Deploy API Gateway
- [ ] Verify health checks
- [ ] Check logs for errors
- [ ] Monitor metrics
- [ ] Test critical endpoints

### Post-deployment
- [ ] Verify all services are registered
- [ ] Check monitoring dashboards
- [ ] Update deployment documentation
- [ ] Notify stakeholders of completion

## Rollback Procedure

### Docker Compose Rollback
```bash
# Revert to previous version
docker-compose down
docker-compose -f docker-compose.previous.yml up -d
```

### Kubernetes Rollback
```bash
# Rollback deployment
kubectl rollout undo deployment/api-gateway

# Or rollback to specific revision
kubectl rollout undo deployment/api-gateway --to-revision=1
```

## Monitoring

### Health Checks
```bash
# Check service health
curl https://api-gateway/health

# Check Redis connection
curl https://api-gateway/health/redis
```

### Metrics
- Request rate
- Error rate
- Response time
- Service registry status
- Redis connection status

### Logs
```bash
# Docker logs
docker logs api-gateway

# Kubernetes logs
kubectl logs -l app=api-gateway
```

## Security Considerations

1. **SSL/TLS**
   - Use valid SSL certificates
   - Enable HTTPS only
   - Configure secure headers

2. **Network Security**
   - Use internal network for service communication
   - Configure firewall rules
   - Enable rate limiting

3. **Secrets Management**
   - Use Kubernetes secrets
   - Rotate secrets regularly
   - Audit secret access

4. **Access Control**
   - Implement RBAC
   - Use service accounts
   - Monitor access logs

## Maintenance

### Regular Tasks
- Update dependencies
- Rotate secrets
- Backup data
- Monitor resource usage
- Review logs
- Update documentation

### Scaling
```bash
# Scale horizontally
kubectl scale deployment api-gateway --replicas=5

# Scale vertically
kubectl set resources deployment api-gateway -c=api-gateway --limits=cpu=1000m,memory=1Gi
```

## Troubleshooting

### Common Issues
1. Service registration failures
2. Redis connection issues
3. Memory pressure
4. Network connectivity
5. SSL certificate expiration

### Debugging Tools
- Kubernetes dashboard
- Prometheus metrics
- Grafana dashboards
- Log aggregation
- Network debugging tools

## Support

### Getting Help
1. Check monitoring dashboards
2. Review logs
3. Consult documentation
4. Contact support team

### Escalation
1. On-call engineer
2. DevOps team
3. Security team
4. Management 
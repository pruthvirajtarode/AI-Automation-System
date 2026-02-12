# AWS Deployment Guide for AI Automation System with Openclaw Agent

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [AWS Services Setup](#aws-services-setup)
4. [Deployment Steps](#deployment-steps)
5. [Configuration](#configuration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Scaling & Performance](#scaling--performance)
8. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

### System Architecture on AWS

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS Cloud Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CloudFront (CDN) ──┐                                        │
│                     └──> S3 (Frontend Static Files)          │
│                                                              │
│  Application Load Balancer (ALB)                             │
│         │                                                    │
│         └──> ECS Fargate Cluster                             │
│              ├──> Backend Service (FastAPI)                  │
│              └──> Openclaw Agent Container                   │
│                                                              │
│  Data Layer:                                                 │
│  ├──> RDS PostgreSQL (Structured Data)                       │
│  ├──> DocumentDB (MongoDB Compatible - Document Data)        │
│  ├──> ElastiCache Redis (Session & Cache)                    │
│  └──> S3 (Agent State & Large Files)                         │
│                                                              │
│  Logging & Monitoring:                                       │
│  ├──> CloudWatch (Logs & Metrics)                            │
│  ├──> CloudTrail (Audit Logs)                                │
│  └──> X-Ray (Distributed Tracing)                            │
│                                                              │
│  Secrets Management:                                         │
│  └──> AWS Secrets Manager                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### AWS Account Setup
- AWS Account with appropriate IAM permissions
- AWS CLI v2 installed and configured
- Docker & Docker Compose installed locally
- Node.js v18+ (for frontend)
- Python 3.9+ (for backend)

### Required Tools
```bash
# AWS CLI
aws --version  # Should be 2.x or higher

# Docker
docker --version
docker compose --version

# Node.js and npm
node --version  # v18+
npm --version   # v9+

# Python
python --version  # 3.9+
pip --version
```

---

## AWS Services Setup

### 1. AWS RDS PostgreSQL Setup

```bash
# Create RDS Instance via AWS Console or CLI
aws rds create-db-instance \
  --db-instance-identifier ai-automation-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.3 \
  --master-username ai_user \
  --master-user-password "YourSecurePassword123!" \
  --allocated-storage 20 \
  --storage-type gp3 \
  --backup-retention-period 7 \
  --enable-cloudwatch-logs-exports postgresql
```

### 2. AWS DocumentDB Setup (MongoDB Compatible)

```bash
# Create DocumentDB Cluster
aws docdb create-db-cluster \
  --db-cluster-identifier ai-automation-mongo \
  --engine docdb \
  --master-username ai_user \
  --master-user-password "YourSecurePassword123!" \
  --backup-retention-period 7 \
  --enable-cloudwatch-logs-exports audit,error,general,slowquery
```

### 3. AWS ElastiCache Redis Setup

```bash
# Create ElastiCache Redis Cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id ai-automation-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-nodes 1 \
  --auto-failover-enabled
```

### 4. AWS S3 Bucket Setup (for Openclaw Agent Data)

```bash
# Create S3 bucket
aws s3 mb s3://ai-automation-agent-data \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket ai-automation-agent-data \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket ai-automation-agent-data \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Set lifecycle policy (optional - cleanup old agent data)
aws s3api put-bucket-lifecycle-configuration \
  --bucket ai-automation-agent-data \
  --lifecycle-configuration file://s3-lifecycle.json
```

---

## Deployment Steps

### Step 1: Prepare Docker Images

#### Build Backend Image
```bash
cd backend
docker build -t ai-automation-backend:latest .
```

#### Build Frontend Image
```bash
cd frontend
docker build -t ai-automation-frontend:latest .
```

### Step 2: Push to AWS ECR (Elastic Container Registry)

```bash
# Create ECR repositories
aws ecr create-repository --repository-name ai-automation-backend
aws ecr create-repository --repository-name ai-automation-frontend

# Get login token
aws ecr get-login-password --region us-east-1 | docker login \
  --username AWS \
  --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag and push backend
docker tag ai-automation-backend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-automation-backend:latest

docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-automation-backend:latest

# Tag and push frontend
docker tag ai-automation-frontend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-automation-frontend:latest

docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-automation-frontend:latest
```

### Step 3: Create ECS Cluster

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name ai-automation-cluster

# Create CloudWatch Log Groups
aws logs create-log-group --log-group-name /ecs/ai-automation-backend
aws logs create-log-group --log-group-name /ecs/ai-automation-frontend
aws logs create-log-group --log-group-name /ecs/ai-automation-migrations
```

### Step 4: Create ECS Task Definitions

#### Backend Task Definition
Create `ecs-backend-task-definition.json`:

```json
{
  "family": "ai-automation-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-automation-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environmentFiles": [
        {
          "value": "arn:aws:s3:::your-config-bucket/.env.aws",
          "type": "s3"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:openai-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-automation-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ],
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRoleWithSecrets"
}
```

#### Register Task Definition
```bash
aws ecs register-task-definition \
  --cli-input-json file://ecs-backend-task-definition.json
```

### Step 5: Create ECS Service

```bash
aws ecs create-service \
  --cluster ai-automation-cluster \
  --service-name ai-automation-backend-service \
  --task-definition ai-automation-backend:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:YOUR_ACCOUNT_ID:targetgroup/ai-backend/...,containerName=backend,containerPort=8000 \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## Configuration

### 1. Environment Variables in AWS Secrets Manager

```bash
# Create secrets
aws secretsmanager create-secret \
  --name openai-api-key \
  --secret-string "sk-..."

aws secretsmanager create-secret \
  --name rds-password \
  --secret-string "YourSecurePassword123!"

aws secretsmanager create-secret \
  --name documentdb-password \
  --secret-string "YourSecurePassword123!"

aws secretsmanager create-secret \
  --name redis-password \
  --secret-string "YourSecurePassword123!"
```

### 2. Create .env.aws Configuration

Use the provided `.env.aws` template and update:
- AWS_REGION
- RDS_ENDPOINT
- DOCUMENTDB_ENDPOINT
- ELASTICACHE_ENDPOINT
- OPENAI_API_KEY

### 3. Upload Configuration to S3

```bash
aws s3 cp .env.aws s3://your-config-bucket/.env.aws
```

---

## Monitoring & Logging

### CloudWatch Dashboards

```bash
# Create custom dashboard
aws cloudwatch put-dashboard \
  --dashboard-name AIAutomationDashboard \
  --dashboard-body file://dashboard-config.json
```

### CloudWatch Alarms

```bash
# CPU Utilization Alarm
aws cloudwatch put-metric-alarm \
  --alarm-name ai-backend-high-cpu \
  --alarm-description "Alert if CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold

# Task Count Alarm
aws cloudwatch put-metric-alarm \
  --alarm-name ai-backend-task-count \
  --alarm-description "Alert if task count < desired" \
  --metric-name RunningCount \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 1 \
  --comparison-operator LessThanThreshold
```

### View Logs

```bash
# Stream logs in real-time
aws logs tail /ecs/ai-automation-backend --follow

# Get logs for specific time period
aws logs filter-log-events \
  --log-group-name /ecs/ai-automation-backend \
  --start-time $(date -d '1 hour ago' +%s)000 \
  --end-time $(date +%s)000
```

---

## Scaling & Performance

### Auto Scaling Setup

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/ai-automation-cluster/ai-automation-backend-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --policy-name ai-backend-scaling-policy \
  --service-namespace ecs \
  --resource-id service/ai-automation-cluster/ai-automation-backend-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

### scaling-policy.json
```json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleOutCooldown": 60,
  "ScaleInCooldown": 300
}
```

---

## Troubleshooting

### Check ECS Service Status

```bash
# List services
aws ecs list-services --cluster ai-automation-cluster

# Describe service
aws ecs describe-services \
  --cluster ai-automation-cluster \
  --services ai-automation-backend-service

# List tasks
aws ecs list-tasks --cluster ai-automation-cluster

# Describe task
aws ecs describe-tasks \
  --cluster ai-automation-cluster \
  --tasks arn:aws:ecs:...
```

### Common Issues & Solutions

#### Issue: Tasks not starting
```bash
# Check CloudWatch logs
aws logs tail /ecs/ai-automation-backend --follow

# Check task events
aws ecs describe-tasks --cluster ai-automation-cluster --tasks <task-arn>
```

#### Issue: RDS Connection Errors
```bash
# Test RDS connectivity
psql -h <RDS_ENDPOINT> -U ai_user -d ai_automation

# Check security groups
aws ec2 describe-security-groups --group-ids sg-xxx
```

#### Issue: DocumentDB Connection Errors
```bash
# Check connection string
mongodb+srv://ai_user:PASSWORD@<ENDPOINT>/?retryWrites=true&w=majority
```

---

## Opclaw Agent on AWS

### Agent Capabilities on AWS

The Openclaw Agent leverages AWS services for:

1. **Persistent Storage**: AWS S3 stores agent decisions and analysis
2. **Scalability**: ECS Fargate automatically scales based on load
3. **High Availability**: Multi-AZ deployment across availability zones
4. **Monitoring**: CloudWatch tracks agent performance metrics
5. **Security**: Secrets Manager handles sensitive credentials

### Agent Endpoints

```bash
# Score a lead
curl -X POST https://api.yourdomain.com/api/agent/score \
  -H "Content-Type: application/json" \
  -d '{
    "id": "lead_123",
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Tech Corp",
    "company_size": 150
  }'

# Route a lead
curl -X POST https://api.yourdomain.com/api/agent/route \
  -H "Content-Type: application/json" \
  -d '{
    "lead": {...},
    "team_members": [...]
  }'

# Generate follow-up
curl -X POST https://api.yourdomain.com/api/agent/followup \
  -H "Content-Type: application/json" \
  -d '{
    "id": "lead_123",
    "name": "John Doe",
    "company": "Tech Corp"
  }'

# Batch score leads
curl -X POST https://api.yourdomain.com/api/agent/batch-score \
  -H "Content-Type: application/json" \
  -d '[...leads...]'

# Get agent status
curl https://api.yourdomain.com/api/agent/status

# Health check
curl https://api.yourdomain.com/api/agent/health
```

---

## Next Steps

1. **Configure Custom Domain**: Set up Route 53 and ACM certificate
2. **Enable HTTPS**: Configure ALB with SSL/TLS
3. **Setup CI/CD Pipeline**: Use AWS CodePipeline for automated deployments
4. **Configure Backups**: Setup backup policies for databases
5. **Performance Testing**: Load test the system (Apache JMeter, Locust)
6. **Security Audit**: Run AWS Security Hub scans

---

## Support & Documentation

- AWS ECS Documentation: https://docs.aws.amazon.com/ecs/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- AWS Best Practices: https://aws.amazon.com/architecture/best-practices/

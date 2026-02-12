"""
Quick Start Guide
Getting started with AI Automation System
"""

# Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ running locally

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Edit .env with your configuration
# At minimum: set DATABASE_URL, OPENAI_API_KEY, TWILIO credentials

# Initialize database
python -c "from app.core.database import init_db; init_db()"

# Run server
uvicorn main:app --reload
```

Backend will be available at: **http://localhost:8000**

### Step 2: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at: **http://localhost:3000**

## 🧪 Testing the System

### 1. Create a Customer

```bash
curl -X POST http://localhost:8000/api/crm/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "company": "Acme Corp",
    "business_type": "Software"
  }'
```

### 2. Send a Message

```bash
curl -X POST http://localhost:8000/api/messages/receive \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "john@example.com",
    "channel": "email",
    "content": "Hi, I am interested in your services",
    "direction": "inbound"
  }'
```

### 3. Create a Lead

```bash
curl -X POST http://localhost:8000/api/leads/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "customer_uuid_here",
    "status": "new"
  }'
```

## 📚 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔑 Key Environment Variables

```env
# Required for basic operation
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/ai_automation

# For SMS support
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...

# For email support
SENDGRID_API_KEY=SG....

# Optional: CRM Integration
SALESFORCE_CLIENT_ID=...
SALESFORCE_CLIENT_SECRET=...
```

## 🐳 Using Docker (Optional)

```bash
# Start full stack
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432
# MongoDB: localhost:27017
# Redis: localhost:6379

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop everything
docker-compose down
```

## 📁 Project Structure Quick Reference

```
backend/
  main.py              # FastAPI app entry point
  requirements.txt     # Python dependencies
  app/
    routes/            # API endpoints (messages, leads, etc.)
    services/          # Business logic (AI, CRM, Booking, etc.)
    models/            # Database models
    schemas/           # Pydantic schemas
    core/              # Config, database setup

frontend/
  src/
    pages/             # Page components (Dashboard, Leads, etc.)
    components/        # Reusable components
    services/          # API service
    styles/            # CSS styles
```

## 🔧 Common Tasks

### Check API Health

```bash
curl http://localhost:8000/health
```

### List All Leads

```bash
curl http://localhost:8000/api/leads/
```

### Create Task

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "lead_uuid",
    "title": "Follow up call",
    "task_type": "sales"
  }'
```

### Schedule Follow-up

```bash
curl -X POST http://localhost:8000/api/follow-ups/ \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "lead_uuid",
    "message_type": "reminder",
    "scheduled_time": "2024-01-15T10:00:00",
    "message_content": "Just checking in!"
  }'
```

## 📝 Database Setup

### Using PostgreSQL

```bash
# Create database
createdb ai_automation

# Create user
createuser ai_user --password

# Grant privileges
psql ai_automation -c "GRANT ALL PRIVILEGES ON DATABASE ai_automation TO ai_user;"
```

### Connection String
```
postgresql://ai_user:password@localhost:5432/ai_automation
```

## 🐛 Troubleshooting

### Backend won't start
- Check if PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env
- Check port 8000 is not in use

### Frontend fails to connect
- Check if backend is running: `curl http://localhost:8000/health`
- Verify REACT_APP_API_URL in .env.local

### Missing dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### Database errors
```bash
# Reset database (WARNING: deletes all data)
python -c "from app.core.database import Base, engine; Base.metadata.drop_all(engine); init_db()"
```

## 📞 Next Steps

1. **Configure API Keys**: Fill in .env with your API keys
2. **Test Endpoints**: Use the API docs at /docs
3. **Set up Webhooks**: Configure SMS/Email webhooks
4. **Create Users**: Add team members to the system
5. **Customize Flows**: Modify lead qualification logic
6. **Deploy**: Use Docker/Kubernetes for production

## 💡 Tips

- Start with simple messages and leads
- Use the dashboard to monitor system health
- Check logs for debugging: `docker-compose logs -f`
- Test API endpoints with Postman or cURL
- Review OpenAPI docs for all available endpoints

## 📖 Documentation Files

- [README.md](../README.md) - Full documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [API.md](./API.md) - Detailed API reference
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment

---

**Happy automating!** 🎉

"""
README - AI-Powered Messaging & Lead Automation System
"""

# AI-Powered Messaging & Lead Automation System

Complete automation solution for customer communication, lead qualification, CRM updates, appointment booking, task routing, and follow-ups.

## System Architecture

```
Customer Interaction → AI Response → Lead Qualification → CRM Update → Booking → Task Creation → Follow-Up
```

### Core Features

1. **Multi-Channel Message Reception**
   - SMS (Twilio)
   - Email (SendGrid)
   - Website Chat
   - Web Forms

2. **AI-Powered Response Generation**
   - Instant customer replies
   - Conversational AI using OpenAI GPT
   - Context-aware responses

3. **Intelligent Lead Qualification**
   - Automated lead scoring
   - Priority assessment
   - AI-driven qualification questions
   - CRM integration

4. **Appointment Booking**
   - Calendar integration
   - Meeting link generation
   - Availability management

5. **Automatic Task Routing**
   - Intelligent team assignment
   - Support/Sales/Technical categorization
   - Priority-based routing

6. **Follow-up Automation**
   - Scheduled follow-ups
   - Nurture sequences
   - Automated reminders

7. **Notifications & Alerts**
   - Real-time lead notifications
   - Priority alerts
   - Slack integration

## Project Structure

```
ai-automation-system/
├── backend/
│   ├── app/
│   │   ├── core/          # Configuration and database
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── routes/        # API endpoints
│   │   └── utils/         # Utilities
│   ├── main.py           # FastAPI app entry
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Container config
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── styles/       # CSS styles
│   └── package.json      # NPM dependencies
├── config/               # Configuration files
├── docs/                 # Documentation
└── docker-compose.yml    # Full stack setup
```

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- PostgreSQL 15+
- MongoDB 7+
- Redis 7+

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp ../.env.example .env
   # Edit .env with your API keys and database credentials
   ```

3. **Initialize database:**
   ```bash
   python -m app.core.database init_db
   ```

4. **Run server:**
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure API URL:**
   ```bash
   echo "REACT_APP_API_URL=http://localhost:8000/api" > .env.local
   ```

3. **Run development server:**
   ```bash
   npm start
   ```

### Docker Setup

```bash
# Start entire stack
docker-compose up -d

# Backend runs on http://localhost:8000
# Frontend runs on http://localhost:3000
# PostgreSQL on localhost:5432
# MongoDB on localhost:27017
# Redis on localhost:6379
```

## API Endpoints

### Messages
- `POST /api/messages/receive` - Receive incoming message
- `GET /api/messages/` - List messages
- `GET /api/messages/{id}` - Get message details
- `POST /api/messages/send/{channel}` - Send message

### Leads
- `POST /api/leads/` - Create lead
- `GET /api/leads/` - List leads
- `GET /api/leads/{id}` - Get lead details
- `PUT /api/leads/{id}` - Update lead
- `POST /api/leads/{id}/qualify` - Qualify lead
- `POST /api/leads/{id}/assign` - Assign lead

### Customers
- `POST /api/crm/customers` - Create customer
- `GET /api/crm/customers` - List customers
- `GET /api/crm/customers/{id}` - Get customer details
- `PUT /api/crm/customers/{id}` - Update customer
- `GET /api/crm/customers/{id}/history` - Get interaction history

### Bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/` - List bookings
- `GET /api/bookings/{id}` - Get booking details
- `PUT /api/bookings/{id}` - Update booking
- `DELETE /api/bookings/{id}` - Cancel booking
- `GET /api/bookings/availability/check` - Check availability

### Tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/{lead_id}/route` - Auto-route task
- `POST /api/tasks/{id}/assign` - Assign task
- `POST /api/tasks/{id}/status/{status}` - Update task status

### Follow-ups
- `POST /api/follow-ups/` - Schedule follow-up
- `GET /api/follow-ups/` - List follow-ups
- `POST /api/follow-ups/{lead_id}/sequence/{type}` - Create sequence
- `POST /api/follow-ups/send/pending` - Send due follow-ups

## Configuration

### Environment Variables
See `.env.example` for complete list:

- `OPENAI_API_KEY` - OpenAI API key for GPT
- `TWILIO_*` - Twilio SMS configuration
- `SENDGRID_API_KEY` - SendGrid email API
- `DATABASE_URL` - PostgreSQL connection
- `MONGODB_URL` - MongoDB connection
- `REDIS_URL` - Redis connection

### Database Models

- **Customer** - Customer information and contact details
- **Lead** - Lead information and qualification status
- **Message** - Customer messages and AI responses
- **Task** - Tasks assigned to team members
- **Booking** - Appointment bookings
- **FollowUp** - Automated follow-up messages

## Workflow Example

1. Customer sends SMS: "I'm interested in your software"
2. System receives message and generates AI response
3. AI asks qualifying questions
4. Lead qualification service scores the lead
5. High-priority leads trigger instant notifications
6. System routes to sales team
7. Booking link sent to customer
8. Customer schedules appointment
9. Follow-up sequence scheduled
10. Team tracks progress in dashboard

## Key Services

### AIService
- Message processing and understanding
- Lead qualification
- Follow-up message generation

### LeadQualificationService
- Lead scoring algorithm
- Priority determination
- Recommendation generation

### CRMService
- Customer data management
- Lead updates
- Interaction history tracking

### BookingService
- Appointment scheduling
- Calendar integration
- Meeting link generation

### TaskRoutingService
- Intelligent task routing
- Team assignment
- Task status tracking

### FollowUpService
- Follow-up scheduling
- Sequence creation
- Automated message sending

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Production Checklist
- [ ] Set strong SECRET_KEY in .env
- [ ] Configure HTTPS
- [ ] Set up proper database backups
- [ ] Configure monitoring and logging
- [ ] Set up error tracking (Sentry)
- [ ] Configure email/SMS providers with production keys
- [ ] Set up CI/CD pipeline
- [ ] Configure load balancer if needed

### Kubernetes Deployment
See `k8s/` directory for Kubernetes manifests.

## Support & Documentation

- API Documentation: `http://localhost:8000/docs`
- OpenAPI Schema: `http://localhost:8000/openapi.json`
- Additional docs: `/docs` folder

## License

All rights reserved.

## Contributing

1. Create feature branch
2. Commit changes
3. Push to branch
4. Create Pull Request

## Support

For issues and questions, please create an issue on GitHub or contact support.

---

## 🏆 Final Recommendation: AI Tool Selection

For the completion of the AI-Automation-System project, we recommend:

* **Primary Choice: [Abacus.AI DeepAgent](./FINAL_RECOMMENDATION_AI_TOOL.md)**
  - Recommended for professional application development.
  - "Corporate Super-Intelligence" tool.

* **Secondary Choice: OpenClaw**
  - Best as a personal assistant or private "toy".
  - "Hacker’s Personal Assistant" tool.

**Verdict**: Use **DeepAgent** for enterprise-grade automation and business building.

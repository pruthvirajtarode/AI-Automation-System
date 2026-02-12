"""
System Architecture Documentation
Detailed architecture of the AI Automation System
"""

# System Architecture

## Overview

The AI-Powered Messaging & Lead Automation System is built with a modern microservices-inspired architecture using:

- **Backend**: FastAPI (Python)
- **Frontend**: React (JavaScript)
- **Databases**: PostgreSQL (relational) + MongoDB (documents)
- **Cache**: Redis
- **Message Queue**: Optional (Celery)
- **AI Engine**: OpenAI GPT

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   React Web  │  │  Mobile App  │  │   Third-party Apps   │  │
│  │  Dashboard   │  │  (Optional)  │  │   (Webhooks)         │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼──────────────────┼────────────────────┼────────────────┘
          │                  │                    │
          └──────────────────┼────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   API Gateway    │
                    │   (FastAPI)      │
                    └────────┬─────────┘
                             │
┌─────────────────────────────┴──────────────────────────────────────┐
│                     API LAYER                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Messages    │  │  Leads       │  │  Customers   │             │
│  │  Routes      │  │  Routes      │  │  Routes      │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                 │                 │                     │
│  ┌──────▼────────┐  ┌──────▼────────┐  ┌───▼────────────┐        │
│  │  Bookings     │  │  Tasks        │  │  Follow-ups    │        │
│  │  Routes       │  │  Routes       │  │  Routes        │        │
│  └──────┬────────┘  └──────┬────────┘  └───┬────────────┘        │
└─────────┼───────────────────┼────────────────┼────────────────────┘
          │                   │                │
┌─────────┼───────────────────┼────────────────┼────────────────────┐
│         │  SERVICE LAYER    │                │                    │
│  ┌──────▼──────────────────────────────────────┐                  │
│  │                                              │                  │
│  │  ┌─────────────────────────────────────┐   │                  │
│  │  │      AI Service (OpenAI)            │   │                  │
│  │  │  - Message Processing              │   │                  │
│  │  │  - Lead Qualification              │   │                  │
│  │  │  - Response Generation             │   │                  │
│  │  └─────────────────────────────────────┘   │                  │
│  │                                              │                  │
│  │  ┌──────────────────┐  ┌────────────────┐  │                  │
│  │  │  CRM Service     │  │  Booking Svc   │  │                  │
│  │  │  - Customer Mgmt │  │  - Scheduling  │  │                  │
│  │  │  - Lead Tracking │  │  - Calendar    │  │                  │
│  │  └──────────────────┘  └────────────────┘  │                  │
│  │                                              │                  │
│  │  ┌──────────────────┐  ┌────────────────┐  │                  │
│  │  │ Task Service     │  │ Follow-up Svc  │  │                  │
│  │  │ - Routing        │  │ - Scheduling   │  │                  │
│  │  │ - Assignment     │  │ - Sequences    │  │                  │
│  │  └──────────────────┘  └────────────────┘  │                  │
│  │                                              │                  │
│  │  ┌──────────────────────────────────────┐  │                  │
│  │  │  Message Channel Handlers            │  │                  │
│  │  │  - SMS (Twilio)                      │  │                  │
│  │  │  - Email (SendGrid)                  │  │                  │
│  │  │  - Chat                              │  │                  │
│  │  │  - Forms                             │  │                  │
│  │  └──────────────────────────────────────┘  │                  │
│  │                                              │                  │
│  └──────────────────────────────────────────────┘                  │
└──────────────────────────────────────────────────────────────────────┘
          │
┌─────────┼──────────────────────────────────────────────────────────┐
│         │       DATA LAYER                                          │
│  ┌──────▼──────────┐  ┌──────────────┐  ┌────────────────┐       │
│  │  PostgreSQL     │  │  MongoDB     │  │  Redis Cache   │       │
│  │  ────────────   │  │  ──────────  │  │  ──────────    │       │
│  │  - Customers    │  │  - Messages  │  │  - Sessions    │       │
│  │  - Leads        │  │  - Events    │  │  - Task Queue  │       │
│  │  - Tasks        │  │  - Analytics │  │  - Locks       │       │
│  │  - Bookings     │  │              │  │                │       │
│  │  - Follow-ups   │  │              │  │                │       │
│  └─────────────────┘  └──────────────┘  └────────────────┘       │
└──────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│        EXTERNAL INTEGRATIONS                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  OpenAI API  │  │  Twilio SMS  │  │  SendGrid Email      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  Salesforce  │  │  Google Cal  │  │  Stripe/Calendly     │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  Slack       │  │  Zapier      │  │  Custom Webhooks     │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Message Reception & Processing

```
Customer Message
    ↓
Message Handler (SMS/Email/Chat/Form)
    ↓
Save to Database
    ↓
AI Service (Process & Understand)
    ↓
Generate Response
    ↓
Send to Customer
    ↓
Save Conversation History
```

### 2. Lead Qualification Flow

```
Customer Profile + Messages
    ↓
AI Qualification Analysis
    ↓
Calculate Quality Score
    ↓
Determine Priority
    ↓
Update Lead Status
    ↓
Generate Recommendations
    ↓
Trigger Notifications (if high-priority)
```

### 3. Task Routing Flow

```
Message Content
    ↓
Analyze Content
    ↓
Determine Task Type (Sales/Support/Technical)
    ↓
Create Task Record
    ↓
Route to Appropriate Team
    ↓
Send Team Notification
    ↓
Track Task Status
```

### 4. Follow-up Automation

```
Lead Enters Follow-up Condition
    ↓
Schedule Follow-up Sequence
    ↓
Queue Messages
    ↓
Scheduled Time Arrives
    ↓
Generate Personalized Message (AI)
    ↓
Send via Preferred Channel
    ↓
Track Delivery & Response
    ↓
Update Lead Status
```

## Service Architecture

### AI Service
**Responsibilities:**
- Process incoming messages
- Understand customer intent
- Generate contextual responses
- Qualify leads based on conversation
- Generate personalized follow-ups

**Key Methods:**
```python
- process_message()
- qualify_lead()
- generate_follow_up()
```

### Lead Qualification Service
**Responsibilities:**
- Analyze customer fit
- Calculate quality scores
- Determine lead priority
- Provide recommendations
- Track qualification history

**Key Methods:**
```python
- qualify_lead()
- _calculate_quality_score()
- _determine_priority()
- _get_recommendations()
```

### CRM Service
**Responsibilities:**
- Manage customer data
- Store interaction history
- Update lead status
- Sync with external CRMs
- Maintain data consistency

**Key Methods:**
```python
- save_customer_interaction()
- update_lead_in_crm()
- get_customer_history()
- sync_with_salesforce()
```

### Booking Service
**Responsibilities:**
- Manage appointment scheduling
- Check calendar availability
- Generate meeting links
- Send confirmations
- Handle cancellations

**Key Methods:**
```python
- create_booking()
- check_availability()
- update_booking()
- cancel_booking()
```

### Task Routing Service
**Responsibilities:**
- Analyze message content
- Route to appropriate team
- Create task records
- Track task status
- Send notifications

**Key Methods:**
```python
- route_task()
- _analyze_content()
- assign_task()
- update_task_status()
```

### Follow-up Service
**Responsibilities:**
- Schedule follow-ups
- Create automation sequences
- Send pending follow-ups
- Generate personalized messages
- Track engagement

**Key Methods:**
```python
- schedule_follow_up()
- create_follow_up_sequence()
- send_pending_follow_ups()
- _generate_follow_up_message()
```

## Database Schema

### Core Entities

**Customer**
- id (UUID)
- name, email, phone
- company, business_type
- location, created_at, updated_at

**Lead**
- id (UUID)
- customer_id (FK)
- status (new, contacted, qualified, won, lost)
- quality_score (0-100)
- priority (high, medium, low)
- requirements, timeline, budget
- assigned_to, created_at, updated_at

**Message**
- id (UUID)
- customer_id (FK)
- channel (sms, email, chat, form)
- direction (inbound, outbound)
- content, ai_response
- processed, created_at

**Task**
- id (UUID)
- lead_id (FK)
- title, description
- type (sales, support, technical)
- status, priority
- assigned_to, due_date, created_at, updated_at

**Booking**
- id (UUID)
- lead_id (FK), customer_id (FK)
- scheduled_time, duration_minutes
- meeting_type, meeting_link
- status, notes, created_at

**FollowUp**
- id (UUID)
- lead_id (FK)
- message_type, scheduled_time
- message_content, sent, sent_at
- created_at

## API Structure

```
/api
├── /messages
│   ├── POST /receive
│   ├── GET /
│   ├── GET /{id}
│   └── POST /send/{channel}
├── /leads
│   ├── POST /
│   ├── GET /
│   ├── GET /{id}
│   ├── PUT /{id}
│   ├── POST /{id}/qualify
│   └── POST /{id}/assign
├── /crm
│   ├── /customers (CRUD)
│   ├── GET /customers/{id}/history
│   └── POST /sync/salesforce
├── /bookings
│   ├── POST /
│   ├── GET /
│   ├── PUT /{id}
│   └── GET /availability/check
├── /tasks
│   ├── POST /
│   ├── GET /
│   ├── POST /{lead_id}/route
│   └── POST /{id}/assign
└── /follow-ups
    ├── POST /
    ├── GET /
    ├── POST /{lead_id}/sequence/{type}
    └── POST /send/pending
```

## Technology Stack

**Backend:**
- FastAPI - Web framework
- SQLAlchemy - ORM
- Pydantic - Data validation
- OpenAI - AI/ML
- Twilio - SMS
- SendGrid - Email
- Redis - Caching
- PostgreSQL - Primary DB
- MongoDB - Document DB

**Frontend:**
- React 18 - UI framework
- React Router - Navigation
- Axios/Fetch - HTTP client
- CSS3 - Styling

**Infrastructure:**
- Docker - Containerization
- Docker Compose - Multi-container
- Kubernetes - Orchestration (optional)
- Git - Version control

## Scalability Considerations

### Horizontal Scaling
- Multiple API instances behind load balancer
- Database read replicas
- Redis cluster for caching
- Message queue (Celery) for async tasks

### Vertical Scaling
- Optimize database queries
- Implement caching strategies
- Use connection pooling
- Async/await for I/O operations

### Performance Optimization
- Cache frequently accessed data
- Implement pagination
- Use database indexes
- Optimize AI API calls
- Batch process follow-ups

## Security Architecture

- JWT authentication
- API key management
- Rate limiting
- Input validation (Pydantic)
- CORS configuration
- HTTPS/TLS encryption
- Database encryption
- Secure credential storage

## Monitoring & Logging

- Application logging (Python logging)
- API monitoring
- Database query logging
- Error tracking (Sentry)
- Performance monitoring
- User activity tracking
- System health checks

---

This architecture is designed to be:
- **Scalable** - Handle growing user and data volume
- **Maintainable** - Clear separation of concerns
- **Extensible** - Easy to add new features
- **Reliable** - Error handling and resilience
- **Performant** - Optimized for speed

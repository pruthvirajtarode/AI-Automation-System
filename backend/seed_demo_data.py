"""
Seed script - populate the database with demo data for client presentation
Run: python seed_demo_data.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Force SQLite for local seeding (no PostgreSQL needed)
os.environ.setdefault("DATABASE_URL", "sqlite:///./local_dev.db")

from app.core.database import SessionLocal, init_db
from app.models import Customer, Lead, Task, Booking
from datetime import datetime, timedelta
import uuid

def seed():
    init_db()
    db = SessionLocal()

    # Check if data already exists
    if db.query(Customer).count() > 1:
        print("Demo data already seeded. Skipping.")
        db.close()
        return

    print("Seeding demo data...")

    # Create Customers
    customers = [
        Customer(
            id=str(uuid.uuid4()), name="Rahul Sharma", email="rahul@techventures.in",
            phone="+919876543001", company="Tech Ventures India", business_type="Technology",
            location="Mumbai", status="active", tier="premium"
        ),
        Customer(
            id=str(uuid.uuid4()), name="Priya Patel", email="priya@greenleaf.co",
            phone="+919876543002", company="GreenLeaf Solutions", business_type="Sustainability",
            location="Delhi", status="active", tier="enterprise"
        ),
        Customer(
            id=str(uuid.uuid4()), name="Amit Kumar", email="amit@cloudcore.io",
            phone="+919876543003", company="CloudCore Systems", business_type="Cloud Services",
            location="Bangalore", status="active", tier="standard"
        ),
        Customer(
            id=str(uuid.uuid4()), name="Sneha Reddy", email="sneha@mediapulse.in",
            phone="+919876543004", company="MediaPulse Digital", business_type="Marketing",
            location="Hyderabad", status="active", tier="premium"
        ),
        Customer(
            id=str(uuid.uuid4()), name="Vikram Singh", email="vikram@buildfast.co",
            phone="+919876543005", company="BuildFast Construction", business_type="Construction",
            location="Pune", status="inactive", tier="standard"
        ),
    ]

    for c in customers:
        db.add(c)
    db.flush()

    # Create Leads
    now = datetime.utcnow()
    leads = [
        Lead(
            id=str(uuid.uuid4()), customer_id=customers[0].id,
            status="qualified", quality_score=8.5,
            requirements="AI chatbot integration for customer support",
            timeline="2 weeks", budget="$5,000", priority="high", assigned_to="Agent Dada"
        ),
        Lead(
            id=str(uuid.uuid4()), customer_id=customers[1].id,
            status="new", quality_score=6.0,
            requirements="CRM automation setup",
            timeline="1 month", budget="$3,000", priority="medium", assigned_to=None
        ),
        Lead(
            id=str(uuid.uuid4()), customer_id=customers[2].id,
            status="contacted", quality_score=7.2,
            requirements="Cloud migration and monitoring dashboard",
            timeline="3 weeks", budget="$8,000", priority="high", assigned_to="Agent Dada"
        ),
        Lead(
            id=str(uuid.uuid4()), customer_id=customers[3].id,
            status="in_negotiation", quality_score=9.1,
            requirements="Social media automation + analytics",
            timeline="1 week", budget="$4,500", priority="urgent", assigned_to="Agent Dada"
        ),
    ]

    for l in leads:
        db.add(l)
    db.flush()

    # Create Tasks (requires lead_id)
    tasks = [
        Task(
            id=str(uuid.uuid4()), lead_id=leads[0].id,
            title="Follow up with Rahul - AI Chatbot",
            description="Send proposal for AI chatbot integration",
            task_type="follow_up", priority="high", status="open",
            assigned_to="Agent Dada", due_date=now + timedelta(days=2)
        ),
        Task(
            id=str(uuid.uuid4()), lead_id=leads[3].id,
            title="Prepare demo for MediaPulse",
            description="Create social media automation demo",
            task_type="demo", priority="urgent", status="in_progress",
            assigned_to="Agent Dada", due_date=now + timedelta(days=1)
        ),
        Task(
            id=str(uuid.uuid4()), lead_id=leads[1].id,
            title="Send CRM onboarding docs",
            description="Share GreenLeaf CRM setup documentation",
            task_type="documentation", priority="medium", status="open",
            assigned_to="Agent Dada", due_date=now + timedelta(days=5)
        ),
        Task(
            id=str(uuid.uuid4()), lead_id=leads[2].id,
            title="Review CloudCore proposal",
            description="Review and finalize cloud migration proposal",
            task_type="review", priority="high", status="completed",
            assigned_to="Agent Dada", due_date=now - timedelta(days=1)
        ),
    ]

    for t in tasks:
        db.add(t)
    db.flush()

    # Create Bookings (uses duration_minutes, meeting_type)
    bookings = [
        Booking(
            id=str(uuid.uuid4()), customer_id=customers[0].id, lead_id=leads[0].id,
            meeting_type="consultation",
            scheduled_time=now + timedelta(days=3, hours=10),
            duration_minutes=60, status="scheduled",
            meeting_link="https://meet.digitaldada.com/rahul-session",
            notes="AI Chatbot Strategy Session - Discuss requirements and timeline"
        ),
        Booking(
            id=str(uuid.uuid4()), customer_id=customers[3].id, lead_id=leads[3].id,
            meeting_type="demo",
            scheduled_time=now + timedelta(days=1, hours=14),
            duration_minutes=45, status="scheduled",
            meeting_link="https://meet.digitaldada.com/mediapulse-demo",
            notes="Social Media Automation Demo - Live demo of automation features"
        ),
        Booking(
            id=str(uuid.uuid4()), customer_id=customers[2].id, lead_id=leads[2].id,
            meeting_type="follow_up",
            scheduled_time=now - timedelta(days=2, hours=11),
            duration_minutes=30, status="completed",
            meeting_link="https://meet.digitaldada.com/cloudcore",
            notes="CloudCore Progress Check - Reviewed migration plan, approved"
        ),
    ]

    for b in bookings:
        db.add(b)

    db.commit()
    db.close()
    print(f"Seeded: {len(customers)} customers, {len(leads)} leads, {len(tasks)} tasks, {len(bookings)} bookings")
    print("Demo data ready!")


if __name__ == "__main__":
    seed()

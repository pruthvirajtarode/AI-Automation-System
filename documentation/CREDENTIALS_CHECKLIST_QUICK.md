# ✅ CREDENTIALS CHECKLIST - Quick Reference

## What to Ask Your Client For

### 🔴 REQUIRED (System won't work without these):

```
1. OPENAI_API_KEY
   Source: https://platform.openai.com/api-keys
   Example: sk-proj-xxxxxxxxxxxxx

2. TWILIO_ACCOUNT_SID
   Source: https://www.twilio.com/console
   Example: ACxxxxxxxxxxxxxxxxxxxxx

3. TWILIO_AUTH_TOKEN
   Source: https://www.twilio.com/console
   Example: xxxxxxxxxxxxxxxxxxxxx

4. TWILIO_PHONE_NUMBER
   Source: https://www.twilio.com/console
   Example: +14155552671

5. SENDGRID_API_KEY
   Source: https://app.sendgrid.com/settings/api_keys
   Example: SG.xxxxxxxxxxxxxxxxxxxxx

6. GMAIL_ADDRESS
   Source: Gmail account
   Example: admin@gmail.com

7. GMAIL_APP_PASSWORD
   Source: https://myaccount.google.com/apppasswords
   Example: abcd efgh ijkl mnop

8. DATABASE_URL (PostgreSQL)
   Source: Your database provider
   Example: postgresql://user:pass@localhost:5432/db

9. REDIS_URL
   Source: Redis server
   Example: redis://localhost:6379

10. SECRET_KEY
    Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"
    Example: xxxxxxxxxxxxxxxxxxxxx
```

### 🟠 OPTIONAL (For enhanced features):

```
- SALESFORCE_CLIENT_ID
- SALESFORCE_CLIENT_SECRET
- SALESFORCE_INSTANCE_URL
- Salesforce Org: https://login.salesforce.com/

- GOOGLE_CALENDAR_API_KEY
- Google Cloud: https://console.cloud.google.com

- CALENDLY_API_TOKEN
- Calendly: https://calendly.com/integrations/api

- STRIPE_API_KEY
- Stripe: https://dashboard.stripe.com/apikeys

- SLACK_WEBHOOK_URL
- Slack: https://api.slack.com/messaging/webhooks

- MONGODB_URL (for analytics)
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas

- AWS_ACCESS_KEY_ID (if using AWS)
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_S3_BUCKET
- AWS: https://console.aws.amazon.com/iam/
```

---

## 📋 CLIENT REQUEST EMAIL Template

Subject: **Required Credentials for AI Automation System Setup**

---

Hi [Client Name],

To set up your AI-Powered Lead Automation System, we'll need you to provide credentials from several external services. Below is a complete list:

### **MUST HAVE (Core Services)** - 10 items
1. **OpenAI API Key** - For AI message generation
2. **Twilio Account SID** - For SMS receiving/sending
3. **Twilio Auth Token** - For SMS authentication
4. **Twilio Phone Number** - Your assigned SMS number
5. **SendGrid API Key** - For email delivery
6. **Gmail Address** - For email server
7. **Gmail App Password** - For email authentication (NOT your regular Gmail password)
8. **PostgreSQL Database URL** - For data storage
9. **Redis URL** - For caching
10. **Secret Key** - For session encryption (we can generate this)

### **NICE TO HAVE (Optional Features)** - 8 items
- Salesforce credentials (if you use Salesforce CRM)
- Google Calendar API Key (for calendar sync)
- Calendly API Token (for booking management)
- Stripe API Key (for payments)
- Slack Webhook URL (for team notifications)
- MongoDB URL (for analytics)
- AWS credentials (if you want cloud hosting)

### **Timeline**
Please provide these credentials by [DATE] so we can complete the setup.

### **Security**
- All credentials will be stored securely in an encrypted environment file
- Never shared via email in future communications
- Stored locally and not committed to version control

Please reply with the attached spreadsheet filled out with these values.

Thanks,
[Your Name]

---

## 🎯 For Zoho & Other CRM Integration

If your client uses **Zoho CRM** instead of Salesforce:

```
ZOHO_CLIENT_ID
ZOHO_CLIENT_SECRET
ZOHO_REFRESH_TOKEN
ZOHO_API_URL = https://www.zohoapis.com

Source: https://accounts.zoho.com/developerconsole
```

---

## 💾 How to Store These in .env File

Create a file named `.env` in the backend root directory:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+14155552671

# SendGrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx

# Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=admin@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_automation
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/db
REDIS_URL=redis://localhost:6379

# Application
SECRET_KEY=your-generated-secret-key-here
APP_NAME=AI Lead Automation System
DEPLOYMENT_ENV=production

# AWS (if using)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxx
AWS_REGION=us-east-1
AWS_S3_BUCKET=ai-automation-agent-data

# Salesforce (Optional)
SALESFORCE_CLIENT_ID=
SALESFORCE_CLIENT_SECRET=
SALESFORCE_INSTANCE_URL=

# Google Calendar (Optional)
GOOGLE_CALENDAR_API_KEY=

# Calendly (Optional)
CALENDLY_API_TOKEN=

# Stripe (Optional)
STRIPE_API_KEY=

# Slack (Optional)
SLACK_WEBHOOK_URL=
```

---

## ⚠️ IMPORTANT REMINDERS

1. **NEVER** commit `.env` file to GitHub
2. **NEVER** share credentials via Slack or email
3. **NEVER** use test/demo credentials in production
4. **ALWAYS** use App Passwords for Gmail (not your login password)
5. **ALWAYS** enable 2FA on accounts with API access
6. **ALWAYS** rotate credentials periodically
7. **ALWAYS** use different credentials for dev/staging/production

---

## 🔗 Quick Links Reference

| Service | Website | API Console | Docs |
|---------|---------|-------------|------|
| **OpenAI** | openai.com | platform.openai.com/api-keys | platform.openai.com/docs |
| **Twilio** | twilio.com | console.twilio.com | twilio.com/docs |
| **SendGrid** | sendgrid.com | app.sendgrid.com/settings/api_keys | sendgrid.com/docs |
| **Gmail** | gmail.com | myaccount.google.com/apppasswords | google.com/support/accounts |
| **Salesforce** | salesforce.com | login.salesforce.com | developer.salesforce.com |
| **Zoho** | zoho.com | accounts.zoho.com/developerconsole | zoho.com/docs |
| **AWS** | aws.amazon.com | console.aws.amazon.com | docs.aws.amazon.com |
| **Google Cloud** | cloud.google.com | console.cloud.google.com | cloud.google.com/docs |
| **Stripe** | stripe.com | dashboard.stripe.com | stripe.com/docs |
| **Slack** | slack.com | api.slack.com | slack.com/help/categories |
| **PostgreSQL** | postgresql.org | (depends on host) | postgresql.org/docs |
| **MongoDB** | mongodb.com | cloud.mongodb.com | docs.mongodb.com |
| **Redis** | redis.io | (depends on host) | redis.io/documentation |

---

## 📊 Cost Estimation (Monthly)

| Service | Free Tier | Entry Plan | Notes |
|---------|-----------|-----------|-------|
| OpenAI | $0 ($5 trial) | Pay-as-you-go | $10-50/month typical |
| Twilio | Free with trial | $0.0075/SMS | $50-200/month typical |
| SendGrid | 100 emails/day | $9.95/month | Good for small volume |
| Gmail | Free | Free | Only costs Google account |
| PostgreSQL | Free (self-hosted) | $12-300/month | Depends on provider |
| Redis | Free (self-hosted) | $5-50/month | Depends on provider |
| AWS | Free tier (limited) | $20-200/month | Scalable pricing |
| Salesforce | Sandbox only | $75-300/month | CRM licensing |
| Stripe | Free to connect | 2.9% + $0.30 | Only on transactions |
| Google Calendar | Free | Free | Limited free tier |
| Slack | Free tier | $8/user/month | Team communication |
| **TOTAL MINIMUM** | ~$10 | $60-100/month | For basic operation |

---

## ✅ Pre-Launch Verification Checklist

Before going live, verify:

- [ ] All API keys are working
- [ ] SMS can send and receive via Twilio
- [ ] Emails can send via SendGrid
- [ ] Database connection is stable
- [ ] Redis cache is working
- [ ] OpenAI API is accessible and has credits
- [ ] AWS S3 bucket exists (if using)
- [ ] All optional integrations are configured (if selected)
- [ ] Error logging is enabled
- [ ] Monitoring dashboards are setup
- [ ] Backup credentials are stored safely
- [ ] Team members know how to rotate keys

---

**Document Created:** February 7, 2026
**Last Updated:** February 7, 2026
**Status:** Ready to Share with Clients

# 🔐 Complete List of Required Credentials & API Keys

## Overview
This document lists **ALL external services, API keys, and credentials** required to run the AI-Powered Lead Automation System. Use this checklist when requesting credentials from your client.

---

## 📋 CREDENTIALS CHECKLIST

### 1. **OpenAI (AI Engine)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `OPENAI_API_KEY` | ✅ YES | API key for GPT-4 language model | [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| AI Model Selection | ✅ YES | Usually `gpt-4` or `gpt-3.5-turbo` | Set in environment |

**What it does:** Powers AI message generation, lead qualification, and automated responses

**API Limit Guide:**
- Usage-based pricing
- Recommended: Monitor monthly costs
- Starting budget: $10-20/month for testing

---

### 2. **Twilio (SMS Communication)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `TWILIO_ACCOUNT_SID` | ✅ YES | Account identifier from Twilio | [https://www.twilio.com/console](https://www.twilio.com/console) |
| `TWILIO_AUTH_TOKEN` | ✅ YES | Authentication token (keep SECRET) | [https://www.twilio.com/console](https://www.twilio.com/console) |
| `TWILIO_PHONE_NUMBER` | ✅ YES | Your Twilio phone number (e.g., +1234567890) | [https://www.twilio.com/console/phone-numbers](https://www.twilio.com/console/phone-numbers) |

**What it does:** Sends SMS messages to customers, receives SMS replies

**Setup Steps:**
1. Create free Twilio account
2. Verify your personal phone
3. Get trial phone number (+1 US number)
4. Add credits for production (starts with $15 trial credit)
5. Copy Account SID, Auth Token, and Phone Number

**API Limit Guide:**
- Free trial: Limited to verified numbers only
- Paid: Pay-as-you-go ($0.0075 per SMS)
- Monthly estimate: $50-200 depending on volume

---

### 3. **SendGrid (Email Delivery)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `SENDGRID_API_KEY` | ✅ YES | API key for sending emails | [https://app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys) |

**What it does:** Sends email notifications, follow-ups, and confirmations

**Setup Steps:**
1. Create account at [sendgrid.com](https://sendgrid.com)
2. Verify your sender email address
3. Create API key in Settings → API Keys
4. Use key for authenticated requests

**API Limit Guide:**
- Free tier: 100 emails/day
- Paid tier: Up to 500K emails/month ($9.95/month)
- Recommended: Use paid tier for production

---

### 4. **Google Calendar (Appointment Sync)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `GOOGLE_CALENDAR_API_KEY` | ⚠️ OPTIONAL | API key for Google Calendar integration | [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) |

**What it does:** Syncs booked appointments to Google Calendar

**Setup Steps:**
1. Create a Google Cloud project
2. Enable Google Calendar API
3. Create API key (or Service Account)
4. Copy the API key

---

### 5. **Calendly (Booking Management)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `CALENDLY_API_TOKEN` | ⚠️ OPTIONAL | API token for Calendly integration | [https://calendly.com/integrations/api](https://calendly.com/integrations/api) |

**What it does:** Manages appointment bookings via Calendly

**Setup Steps:**
1. Create Calendly account
2. Go to Settings → API & Webhooks
3. Generate Personal Access Token
4. Store securely

---

### 6. **Stripe (Payment Processing)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `STRIPE_API_KEY` | ⚠️ OPTIONAL | Publishable and Secret API keys | [https://dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys) |

**What it does:** Processes payments from customers

**Setup Steps:**
1. Create Stripe account at [stripe.com](https://stripe.com)
2. Go to Developers → API Keys
3. Copy both Publishable and Secret keys
4. Use Secret key in backend only

---

### 7. **Salesforce (CRM Integration)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `SALESFORCE_CLIENT_ID` | ⚠️ OPTIONAL | OAuth 2.0 Client ID | [https://login.salesforce.com/](https://login.salesforce.com/) → Setup → Apps → Connected Apps |
| `SALESFORCE_CLIENT_SECRET` | ⚠️ OPTIONAL | OAuth 2.0 Client Secret | Same as above |
| `SALESFORCE_INSTANCE_URL` | ⚠️ OPTIONAL | Your Salesforce instance URL (e.g., https://your-instance.salesforce.com) | Your Salesforce admin console |

**What it does:** Syncs leads and customer data to Salesforce CRM

**Setup Steps:**
1. Create Salesforce Developer account
2. Create a new Connected App
3. Enable OAuth 2.0 in Connected App
4. Generate Client ID and Secret
5. Copy your instance URL (e.g., https://na1.salesforce.com)

---

### 8. **Slack (Team Notifications)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `SLACK_WEBHOOK_URL` | ⚠️ OPTIONAL | Incoming Webhook URL for notifications | [https://api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks) |

**What it does:** Sends team notifications for new leads, high-priority tasks

**Setup Steps:**
1. Create Slack workspace or use existing
2. Go to api.slack.com → Create New App
3. Enable Incoming Webhooks
4. Add New Webhook to Workspace
5. Copy the Webhook URL

**Example Webhook URL:**
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

---

### 9. **Gmail (Email Configuration)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `SMTP_HOST` | ✅ YES | SMTP host (usually `smtp.gmail.com`) | Default for Gmail |
| `SMTP_PORT` | ✅ YES | SMTP port (587 for TLS) | Default: `587` |
| `SMTP_USER` | ✅ YES | Your Gmail address (e.g., admin@gmail.com) | Your Gmail account |
| `SMTP_PASSWORD` | ✅ YES | Gmail App Password (NOT your regular password) | [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |

**What it does:** Sends email notifications via Gmail SMTP

**Setup Steps:**
1. Enable 2-Factor Authentication on your Gmail account
2. Go to myaccount.google.com → Security
3. Create an "App Password" (select Mail + Windows Computer)
4. Google generates a 16-character password
5. Use this password in SMTP_PASSWORD (NOT your Gmail password)

---

### 10. **AWS (Cloud Infrastructure)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | ✅ YES (if using AWS) | AWS access key ID | [https://console.aws.amazon.com/iam/home#/users](https://console.aws.amazon.com/iam/home#/users) |
| `AWS_SECRET_ACCESS_KEY` | ✅ YES (if using AWS) | AWS secret access key (keep SECRET) | Same as above |
| `AWS_REGION` | ✅ YES | AWS region (e.g., `us-east-1`) | Choose your region |
| `AWS_S3_BUCKET` | ✅ YES | S3 bucket name for file storage | Create in AWS S3 console |

**What it does:** Hosts the application, stores files, runs containers

**Setup Steps:**
1. Create AWS account at [aws.amazon.com](https://aws.amazon.com)
2. Go to IAM → Users → Create User
3. Generate Access Key ID and Secret Access Key
4. Store keys securely
5. Create S3 bucket: `ai-automation-agent-data`
6. Choose region (default: us-east-1)

---

### 11. **Database Credentials**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `DATABASE_URL` | ✅ YES | PostgreSQL connection string | Create PostgreSQL database |
| `MONGODB_URL` | ⚠️ OPTIONAL | MongoDB connection string | Create MongoDB database (Atlas recommended) |
| `REDIS_URL` | ✅ YES | Redis cache connection string | Create Redis instance |

**What it does:** Stores customer data, leads, messages, tasks, bookings

**Setup Steps:**
1. **PostgreSQL**: Use local or cloud provider (Heroku, AWS RDS, Railway)
2. **MongoDB**: Create free cluster on MongoDB Atlas
3. **Redis**: Use ElastiCache (AWS) or local Redis

**Example Connection Strings:**
```
PostgreSQL: postgresql://user:password@localhost:5432/ai_automation
MongoDB: mongodb+srv://user:password@cluster.mongodb.net/ai_automation
Redis: redis://localhost:6379
```

---

### 12. **Application Secrets**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| `SECRET_KEY` | ✅ YES | Secret key for session encryption | Generate random string |
| `APP_NAME` | ✅ YES | Application name | Set to: `AI Lead Automation System` |
| `CORS_ORIGINS` | ✅ YES | Allowed frontend URLs | Set to: `http://localhost:3000,http://localhost:8080` |

**Setup Steps:**
1. Generate SECRET_KEY: Use Python to generate a secure random string
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
2. For CORS_ORIGINS, list all domains that can access the API

---

### 13. **OpenClaw Agent (AI Automation)**
| Item | Required | Description | Where to Get |
|------|----------|-------------|---------------|
| OpenClaw Integration | ✅ YES (if using Openclaw) | Agent framework for advanced automation | Part of system architecture |

**What it does:** Advanced AI agent for complex lead scoring and automation

**No credentials needed** - uses existing OpenAI API key

---

## 📊 SUMMARY TABLE - WHAT'S REQUIRED vs OPTIONAL

| Service | Type | Required | For What |
|---------|------|----------|----------|
| OpenAI | API Key | ✅ YES | AI message generation |
| Twilio | API Key | ✅ YES | SMS communication |
| SendGrid | API Key | ✅ YES | Email delivery |
| Google Calendar | API Key | ⚠️ OPTIONAL | Calendar sync |
| Calendly | Token | ⚠️ OPTIONAL | Booking management |
| Stripe | API Key | ⚠️ OPTIONAL | Payment processing |
| Salesforce | OAuth | ⚠️ OPTIONAL | CRM sync |
| Slack | Webhook | ⚠️ OPTIONAL | Team notifications |
| Gmail | SMTP | ✅ YES | Email server |
| AWS | Keys | ✅ YES (if cloud) | Infrastructure |
| PostgreSQL | URL | ✅ YES | Main database |
| MongoDB | URL | ⚠️ OPTIONAL | Analytics |
| Redis | URL | ✅ YES | Cache |
| **TOTAL REQUIRED** | - | **8-9 services** | Core functionality |

---

## 🎯 QUICK REQUEST TEMPLATE

Send this to your client to request all credentials:

```
Hello [Client Name],

To set up the AI-Powered Lead Automation System, we need the following credentials:

✅ ESSENTIAL (Must Have):
1. OpenAI API Key (for AI engine)
2. Twilio Account SID, Auth Token, and Phone Number (for SMS)
3. SendGrid API Key (for emails)
4. Gmail Credentials (SMTP settings)
5. AWS Access Key ID and Secret (if cloud hosting)
6. Database connection strings (PostgreSQL, Redis)

⚠️ OPTIONAL (Nice to Have):
7. Salesforce OAuth credentials (for CRM sync)
8. Google Calendar API Key
9. Calendly API Token
10. Stripe API Key (for payments)
11. Slack Webhook (for notifications)
12. MongoDB URL (for analytics)

Timeline: Please provide these within 2-3 business days.
Storage: We'll keep all credentials encrypted in our secure .env file.

Please reply with the credentials in the format shown in the attached spreadsheet.
```

---

## 🔒 SECURITY BEST PRACTICES

### ✅ DO:
- Store all credentials in `.env` file (never in code)
- Use `git ignore` to exclude `.env` from version control
- Rotate API keys regularly
- Use strong, unique values for SECRET_KEY
- Enable 2FA on all accounts
- Use service accounts for production (not personal accounts)
- Store credentials in secure password manager

### ❌ DON'T:
- Commit `.env` file to GitHub
- Share credentials via email/Slack
- Use same credentials across environments
- Use default/weak SECRET_KEY values
- Log or print credentials
- Share AWS keys with multiple people

---

## 📝 IMPLEMENTATION CHECKLIST

- [ ] OpenAI API Key obtained and verified
- [ ] Twilio account setup (Account SID, Auth Token, Phone Number)
- [ ] SendGrid API Key created and tested
- [ ] Gmail SMTP credentials configured
- [ ] AWS account setup (if cloud deployment)
- [ ] PostgreSQL database created and running
- [ ] Redis instance created and running
- [ ] All credentials placed in `.env` file
- [ ] `.env` added to `.gitignore`
- [ ] Application tested with all services
- [ ] Monitoring setup (CloudWatch, SendGrid, Twilio dashboards)
- [ ] Backup credentials stored securely

---

## 🆘 TROUBLESHOOTING CONNECTION ISSUES

### OpenAI not working?
- Check API key is correct
- Verify account has credits
- Check rate limits: `https://platform.openai.com/account/rate-limits`

### Twilio SMS not sending?
- Verify Account SID and Auth Token
- Check phone number format (include country code)
- Confirm account has credits
- Check Twilio console for failed messages

### SendGrid emails failing?
- Verify API key is correct
- Check sender email is verified
- Ensure domain authentication is complete
- Check spam folder

### Database connection timeouts?
- Verify connection string is correct
- Check database is running
- Test connection: `psql -c "select 1"` (PostgreSQL)
- Check firewall/security group rules (AWS)

### AWS S3 errors?
- Verify bucket name is correct
- Check IAM permissions on access key
- Ensure region matches bucket region
- Verify bucket exists

---

## 📞 SUPPORT CONTACTS

| Service | Support | Documentation |
|---------|---------|---------------|
| OpenAI | [support.openai.com](https://support.openai.com) | [platform.openai.com/docs](https://platform.openai.com/docs) |
| Twilio | [twilio.com/help](https://www.twilio.com/help) | [twilio.com/docs](https://www.twilio.com/en-us/docs) |
| SendGrid | [sendgrid.com/support](https://support.sendgrid.com) | [sendgrid.com/docs](https://docs.sendgrid.com) |
| AWS | [aws.amazon.com/support](https://aws.amazon.com/support) | [docs.aws.amazon.com](https://docs.aws.amazon.com) |
| Salesforce | [salesforce.com/help](https://help.salesforce.com) | [developer.salesforce.com](https://developer.salesforce.com) |

---

**Last Updated:** February 7, 2026
**Document Version:** 1.0
**Status:** Complete & Ready to Share

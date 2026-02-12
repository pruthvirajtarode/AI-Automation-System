# 🎴 QUICK REFERENCE CARD - Print This!

## All Credentials at a Glance (One Page Reference)

---

## ✅ REQUIRED - 9 Items (System WILL NOT work without)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. OPENAI API KEY                                              │
│    Where: https://platform.openai.com/api-keys                │
│    Format: sk-proj-xxxxxxxxxxxxx                              │
│    Cost: $10-50/mo                                             │
│    Setup: 5 min                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 2. TWILIO ACCOUNT SID                                          │
│    Where: https://www.twilio.com/console                      │
│    Format: ACxxxxxxxxxxxxxxxxxxxxx                             │
│    Cost: Included with $50/mo credit                           │
│    Setup: 10 min                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 3. TWILIO AUTH TOKEN                                           │
│    Where: https://www.twilio.com/console                      │
│    Format: xxxxxxxxxxxxxxxxxxxxx                              │
│    Cost: Included                                              │
│    Setup: 5 min                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 4. TWILIO PHONE NUMBER                                         │
│    Where: https://www.twilio.com/console                      │
│    Format: +14155552671                                        │
│    Cost: Included                                              │
│    Setup: 10 min                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 5. SENDGRID API KEY                                            │
│    Where: https://app.sendgrid.com/settings/api_keys           │
│    Format: SG.xxxxxxxxxxxxxxxxxxxxx                            │
│    Cost: FREE (100 emails/day) or $9.95/mo                     │
│    Setup: 5 min                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 6. GMAIL ADDRESS                                               │
│    Source: Your Gmail account                                 │
│    Format: admin@gmail.com                                     │
│    Cost: FREE                                                  │
│    Setup: Already have it                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 7. GMAIL APP PASSWORD (NOT your Gmail password!)               │
│    Where: https://myaccount.google.com/apppasswords            │
│    Format: abcd efgh ijkl mnop (16 characters)                 │
│    Cost: FREE                                                  │
│    Setup: 10 min (with 2FA enabled)                            │
│    ⚠️  IMPORTANT: This is NOT your Gmail password!             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 8. POSTGRESQL DATABASE URL                                     │
│    Format: postgresql://user:password@host:5432/database       │
│    Cost: $5-100/mo (depends on provider)                       │
│    Providers: Railway, Heroku, AWS RDS, Neon                  │
│    Setup: 15 min                                               │
│    Example: postgresql://admin:pass@db.railway.app:5432/ai_db │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 9. REDIS CACHE URL                                             │
│    Format: redis://host:6379                                   │
│    Cost: $5-30/mo (depends on provider)                        │
│    Providers: Railway, AWS ElastiCache, Upstash                │
│    Setup: 10 min                                               │
│    Example: redis://default:token@redis.railway.app:6379      │
└─────────────────────────────────────────────────────────────────┘
```

**TOTAL REQUIRED TIME: 1.5 - 2 hours**
**TOTAL MINIMUM COST: ~$65-100/month**

---

## ⚠️ OPTIONAL - Choose At Least 1 CRM (4 items total)

```
PICK ONE CRM:

┌─────────────────────────────────────────────────────────────────┐
│ OPTION A: ZOHO CRM ⭐ RECOMMENDED (Easiest)                    │
│ Where: https://www.zoho.com/crm/                              │
│ Get All From: https://accounts.zoho.com/developerconsole       │
│ Cost: FREE or $15-65/user/month                                │
│ Setup Time: 30-45 min                                          │
│                                                                 │
│ Items Needed:                                                   │
│ ├─ ZOHO_CLIENT_ID         1000.xxxxx                           │
│ ├─ ZOHO_CLIENT_SECRET     xxxxxxxxxxxxxxxxxxxxx               │
│ ├─ ZOHO_REFRESH_TOKEN     1000.xxxxx                           │
│ └─ ZOHO_API_URL           https://www.zohoapis.com            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ OPTION B: SALESFORCE (Enterprise)                              │
│ Where: https://developer.salesforce.com/                      │
│ Get All From: Setup → Apps → App Manager                      │
│ Cost: $75-300/user/month                                       │
│ Setup Time: 1-2 hours                                          │
│                                                                 │
│ Items Needed:                                                   │
│ ├─ SALESFORCE_CLIENT_ID          3MVG9.xxxxx                  │
│ ├─ SALESFORCE_CLIENT_SECRET      xxxxxxxxxxxxxxxxxxxxx         │
│ └─ SALESFORCE_INSTANCE_URL       https://na1.salesforce.com   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ OPTION C: HUBSPOT (Marketing-focused)                          │
│ Where: https://www.hubspot.com/                               │
│ Get All From: Settings → Integrations → Private apps           │
│ Cost: FREE or $50-1200/month                                   │
│ Setup Time: 20-30 min                                          │
│                                                                 │
│ Items Needed:                                                   │
│ ├─ HUBSPOT_PRIVATE_APP_TOKEN     pat-na1-xxxxx               │
│ └─ HUBSPOT_PORTAL_ID             12345678                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ OPTION D: PIPEDRIVE (Sales-focused)                            │
│ Where: https://www.pipedrive.com/                             │
│ Get All From: Settings → API                                  │
│ Cost: $12-99/user/month                                        │
│ Setup Time: 15-20 min                                          │
│                                                                 │
│ Items Needed:                                                   │
│ ├─ PIPEDRIVE_API_TOKEN       xxxxxxxxxxxxxxxxxxxxxxxx          │
│ └─ PIPEDRIVE_COMPANY_DOMAIN  your-company                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 EXTRA OPTIONAL FEATURES

```
┌──────────────────────────────────────────────────────┐
│ Google Calendar (Meeting sync)                      │
│ Where: https://console.cloud.google.com/apis        │
│ What: GOOGLE_CALENDAR_API_KEY                       │
│ Cost: FREE                                           │
│ Setup: 15 min                                        │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ Slack (Team notifications)                          │
│ Where: https://api.slack.com/messaging/webhooks     │
│ What: SLACK_WEBHOOK_URL                             │
│ Cost: FREE                                           │
│ Setup: 10 min                                        │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ Stripe (Payment processing)                         │
│ Where: https://dashboard.stripe.com/apikeys         │
│ What: STRIPE_API_KEY (Publishable + Secret)        │
│ Cost: 2.9% + $0.30 per transaction                 │
│ Setup: 15 min                                        │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ AWS (Cloud hosting)                                 │
│ Where: https://console.aws.amazon.com/iam/          │
│ What: AWS_ACCESS_KEY_ID                             │
│       AWS_SECRET_ACCESS_KEY                         │
│       AWS_REGION (e.g., us-east-1)                 │
│       AWS_S3_BUCKET                                 │
│ Cost: $20-200/month (pay-as-you-go)                │
│ Setup: 30 min                                        │
└──────────────────────────────────────────────────────┘
```

---

## 📋 CHECKLIST - PRINT AND COMPLETE

```
TIER 1 - REQUIRED (Must complete)
────────────────────────────────────────
[ ] OpenAI API Key             _______________
[ ] Twilio Account SID         _______________
[ ] Twilio Auth Token          _______________
[ ] Twilio Phone Number        _______________
[ ] SendGrid API Key           _______________
[ ] Gmail Address              _______________
[ ] Gmail App Password         _______________
[ ] PostgreSQL URL             _______________
[ ] Redis URL                  _______________

TIER 2 - CRM (Choose ONE)
────────────────────────────────────────
[ ] CRM Type Selected: __________

If Zoho:
  [ ] Client ID                 _______________
  [ ] Client Secret             _______________
  [ ] Refresh Token             _______________
  [ ] API URL                   _______________

If Salesforce:
  [ ] Client ID                 _______________
  [ ] Client Secret             _______________
  [ ] Instance URL              _______________

If HubSpot:
  [ ] Private App Token         _______________
  [ ] Portal ID                 _______________

If Pipedrive:
  [ ] API Token                 _______________
  [ ] Company Domain            _______________

TIER 3 - OPTIONAL
────────────────────────────────────────
[ ] Google Calendar API        _______________
[ ] Slack Webhook              _______________
[ ] Stripe API Key             _______________
[ ] AWS Access Key             _______________
[ ] AWS Secret Key             _______________
[ ] AWS S3 Bucket              _______________

COMPLETION
────────────────────────────────────────
Date Started: ________________
Date Completed: ________________
Ready for Deployment: [ ] YES [ ] NO
```

---

## ⚡ QUICK START (30-Second Version)

1. **OpenAI:** Get API key at platform.openai.com/api-keys
2. **Twilio:** Get SID, Token, Phone at twilio.com/console
3. **SendGrid:** Get API key at sendgrid.com/settings/api_keys
4. **Gmail:** Enable 2FA, get app password at myaccount.google.com/apppasswords
5. **Database:** Create PostgreSQL at railway.app
6. **Cache:** Create Redis at railway.app
7. **CRM:** Choose Zoho/SF/HubSpot/Pipedrive

**Total Cost:** $70-150/month
**Total Time:** 2-3 hours
**Status:** Ready to deploy!

---

## 🚨 DON'T FORGET!

```
✅ DO THIS:
  ✓ Use strong passwords
  ✓ Enable 2FA on accounts with API access
  ✓ Keep credentials in .env file
  ✓ Add .env to .gitignore
  ✓ Test each credential
  ✓ Rotate keys every 90 days
  ✓ Backup credentials securely

❌ DON'T DO THIS:
  ✗ Share credentials via email
  ✗ Commit .env to GitHub
  ✗ Use Gmail password for SMTP (use App Password!)
  ✗ Hardcode credentials in code
  ✗ Use same credentials for dev & production
  ✗ Log or print credentials
  ✗ Ignore API rate limits
```

---

## 📞 CRITICAL SUPPORT

| Problem | Solution |
|---------|----------|
| **SMS not sending** | Check Twilio balance & phone number format |
| **Email not sending** | Check SendGrid API key & sender verification |
| **Can't create app password** | Enable 2FA on Gmail first |
| **Database won't connect** | Verify connection string & network access |
| **API rate limited** | Wait or upgrade plan (see service docs) |
| **CRM sync failing** | Check OAuth token hasn't expired |
| **Lost a credential?** | Regenerate from service dashboard |

---

## 💰 COST SUMMARY TABLE

```
┌────────────────────┬──────────────┬──────────────┬──────────────┐
│ Service            │ Free Tier    │ Paid Tier    │ Monthly Cost │
├────────────────────┼──────────────┼──────────────┼──────────────┤
│ OpenAI             │ $5 trial     │ Pay-as-go    │ $20-50       │
│ Twilio             │ Trial credit │ $0.0075/SMS  │ $50-200      │
│ SendGrid           │ 100/day      │ $9.95/mo     │ $0-10        │
│ Gmail SMTP         │ FREE         │ FREE         │ FREE         │
│ PostgreSQL         │ Self-hosted  │ Cloud        │ $5-100       │
│ Redis              │ Self-hosted  │ Cloud        │ $5-30        │
│ Zoho CRM           │ FREE account │ $15/user/mo  │ $0-65        │
│ Salesforce         │ Sandbox free │ $75/user/mo  │ $75-300      │
│ HubSpot            │ FREE CRM     │ $50/month    │ $0-1200      │
├────────────────────┼──────────────┼──────────────┼──────────────┤
│ **MINIMUM TOTAL**  │              │              │ **$65-150**  │
└────────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 🎯 NEXT STEP

Read: [CREDENTIALS_DOCUMENTATION_INDEX.md](CREDENTIALS_DOCUMENTATION_INDEX.md)

It has links to all detailed guides.

---

**Print This Page!** 📄

Keep this card handy while setting up credentials.

---

**Card Created:** February 7, 2026
**Status:** Ready to Print & Use ✅

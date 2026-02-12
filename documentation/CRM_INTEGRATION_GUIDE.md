# 🔗 CRM Integration Guide - Zoho, Salesforce, HubSpot & Others

## Compare Different CRM Options

Your system can integrate with multiple CRM platforms. Here's what each requires:

---

## 📊 CRM Comparison Table

| Feature | **Zoho CRM** | **Salesforce** | **HubSpot** | **Pipedrive** | **Microsoft Dynamics** |
|---------|------------|----------------|-----------|---------------|----------------------|
| **Setup Difficulty** | Easy ⭐⭐ | Hard ⭐⭐⭐⭐ | Medium ⭐⭐⭐ | Easy ⭐⭐ | Hard ⭐⭐⭐⭐ |
| **Cost** | $15-65/user | $75-300/user | Free-1200 | $12-99/user | $50-250/user |
| **Best For** | Small-medium | Enterprise | Inbound marketing | Sales teams | Large enterprises |
| **API Access** | Easy | Complex | Easy | Medium | Complex |
| **Setup Time** | 1-2 hours | 1-2 days | 2-4 hours | 1-2 hours | 2-3 days |

---

## 🔌 1. ZOHO CRM Integration

### Best For:
- Small to medium businesses
- Affordable pricing
- Easy API integration
- Fully customizable

### Required Credentials:

```
ZOHO_CLIENT_ID
ZOHO_CLIENT_SECRET
ZOHO_REFRESH_TOKEN
ZOHO_API_URL = https://www.zohoapis.com
ZOHO_ORG_ID (optional)
ZOHO_CUSTOM_FIELDS (optional, for field mapping)
```

### Setup Steps:

1. **Create Zoho Account**
   - Go to [zoho.com/crm](https://www.zoho.com/crm/)
   - Sign up for free or paid plan

2. **Register Your Application**
   - Go to [accounts.zoho.com/developerconsole](https://accounts.zoho.com/developerconsole)
   - Click "Create API Key"
   - Choose: OAuth 2.0
   - Enter Application Name: "AI Lead Automation"

3. **Get Credentials**
   - Copy: `Client ID`
   - Copy: `Client Secret`
   - Set Redirect URI: `http://localhost:8000/callback`

4. **Generate Refresh Token**
   - Use Zoho's OAuth token generator
   - Or make authorization request and capture token

5. **Find Your API URL**
   - US: https://www.zohoapis.com
   - EU: https://www.zohoapis.eu
   - CN: https://www.zohoapis.cn

### Environment Variables:

```env
# Zoho CRM
ZOHO_CLIENT_ID=1000.xxxxx
ZOHO_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxx
ZOHO_REFRESH_TOKEN=1000.xxxxx
ZOHO_API_URL=https://www.zohoapis.com
ZOHO_ORG_ID=12345678901 (optional)
```

### What Zoho Can Do:
- ✅ Sync leads automatically
- ✅ Create/update contacts
- ✅ Log activities
- ✅ Update deal stages
- ✅ Send follow-up tasks
- ✅ Track interactions

### Cost:
- **Free Plan**: Up to 2 users, basic features
- **Pro Plan**: $15/user/month, API access
- **Enterprise**: $65/user/month, unlimited API

### Documentation:
- [Zoho CRM API Docs](https://www.zoho.com/crm/developer/docs/api/overview.html)
- [OAuth Setup Guide](https://www.zoho.com/crm/developer/docs/api/extend/oauth.html)

---

## 🔌 2. SALESFORCE CRM Integration

### Best For:
- Large enterprises
- Complex workflows
- Advanced customization
- High-volume operations

### Required Credentials:

```
SALESFORCE_CLIENT_ID
SALESFORCE_CLIENT_SECRET
SALESFORCE_INSTANCE_URL
SALESFORCE_USERNAME (optional)
SALESFORCE_PASSWORD (optional)
SALESFORCE_SECURITY_TOKEN (optional)
```

### Setup Steps:

1. **Create Salesforce Account**
   - Go to [developer.salesforce.com](https://developer.salesforce.com/)
   - Sign up for free Developer org

2. **Create a Connected App**
   - Go to Setup → Apps → App Manager
   - Click "New Connected App"
   - Fill in:
     - App Name: "AI Lead Automation"
     - API Name: "AI_Lead_Automation"
     - Description: "Automate leads from SMS/Email"
     - Contact Email: your-email@company.com

3. **Enable OAuth**
   - Check "Enable OAuth Settings"
   - Set Callback URL: `http://localhost:8000/callback`
   - Select Scopes:
     - Full access (full)
     - Perform requests at any time (refresh_token)
     - Manage user data via APIs (api)

4. **Get Credentials**
   - Click "Reveal" for Consumer Key (Client ID)
   - Click "Reveal" for Consumer Secret (Client Secret)
   - Copy Consumer Key and Secret

5. **Find Your Instance URL**
   - Your SF org URL: https://na1.salesforce.com (varies by region)

### Environment Variables:

```env
# Salesforce
SALESFORCE_CLIENT_ID=3MVG9.WzOfHON8eHZu_xxxxxxxxxxxxx
SALESFORCE_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SALESFORCE_INSTANCE_URL=https://na1.salesforce.com (or your region)
SALESFORCE_USERNAME=admin@company.com.sandbox (optional)
SALESFORCE_PASSWORD=xxxxx (optional)
SALESFORCE_SECURITY_TOKEN=xxxxxxxxxxxxx (optional)
```

### What Salesforce Can Do:
- ✅ Sync leads to Salesforce
- ✅ Create opportunities
- ✅ Update accounts & contacts
- ✅ Log activities & calls
- ✅ Trigger workflows
- ✅ Custom object sync

### Cost:
- **Sandbox**: Free (for development)
- **Developer Edition**: Free (for testing)
- **Essentials**: $75/user/month
- **Professional**: $150/user/month
- **Enterprise**: $300/user/month

### Documentation:
- [Salesforce OAuth Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_understanding_oauth.htm)
- [REST API Docs](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_list.htm)

---

## 🔌 3. HUBSPOT CRM Integration

### Best For:
- Inbound marketing focus
- Lead scoring & nurturing
- Easy implementation
- Mid-market companies

### Required Credentials:

```
HUBSPOT_API_KEY
HUBSPOT_PORTAL_ID
HUBSPOT_PRIVATE_APP_TOKEN (preferred)
```

### Setup Steps:

1. **Create HubSpot Account**
   - Go to [hubspot.com](https://www.hubspot.com/)
   - Sign up for free CRM

2. **Generate Private App Token** (Recommended)
   - Go to Settings → Integrations → Private apps
   - Click "Create private app"
   - Name: "AI Lead Automation"
   - Select Scopes (minimal):
     - `crm.objects.contacts.read`
     - `crm.objects.contacts.write`
     - `crm.objects.deals.read`
     - `crm.objects.deals.write`

3. **Get Token**
   - Copy "Private App Token" (keep it secret!)

4. **Get Portal ID**
   - Go to Settings → Account defaults
   - Copy "Portal ID" (8-10 digit number)

### Environment Variables:

```env
# HubSpot
HUBSPOT_PRIVATE_APP_TOKEN=pat-na1-xxxxxxxxxxxxxxxxxxxxx
HUBSPOT_PORTAL_ID=12345678

# OR (Legacy)
HUBSPOT_API_KEY=xxxxxxxxxxxxxxxxxxxxx
```

### What HubSpot Can Do:
- ✅ Create/update contacts
- ✅ Create deals (opportunities)
- ✅ Add notes & activities
- ✅ Score leads automatically
- ✅ Trigger workflows
- ✅ List all contacts

### Cost:
- **Free CRM**: Forever free, basic features
- **Starter**: $50/month
- **Professional**: $300/month
- **Enterprise**: $1,200/month

### Documentation:
- [HubSpot API Docs](https://developers.hubspot.com/)
- [Private Apps Setup](https://developers.hubspot.com/docs/api/private-apps)

---

## 🔌 4. PIPEDRIVE CRM Integration

### Best For:
- Sales teams
- Deal-focused workflows
- Affordable pricing
- Quick setup

### Required Credentials:

```
PIPEDRIVE_API_TOKEN
PIPEDRIVE_COMPANY_DOMAIN
```

### Setup Steps:

1. **Create Pipedrive Account**
   - Go to [pipedrive.com](https://www.pipedrive.com/)
   - Start free trial

2. **Generate API Token**
   - Go to Settings → API
   - Click "Create new API token"
   - Name: "AI Lead Automation"
   - Copy the token

3. **Get Company Domain**
   - Your Pipedrive URL: `https://your-company.pipedrive.com`
   - Domain = `your-company`

### Environment Variables:

```env
# Pipedrive
PIPEDRIVE_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
PIPEDRIVE_COMPANY_DOMAIN=your-company
```

### What Pipedrive Can Do:
- ✅ Add/update persons (contacts)
- ✅ Create deals (sales opportunities)
- ✅ Add activities (calls, meetings)
- ✅ Manage pipelines
- ✅ Add notes & comments

### Cost:
- **Essential**: $12/user/month
- **Advanced**: $24/user/month
- **Professional**: $49/user/month
- **Power**: $99/user/month

### Documentation:
- [Pipedrive API Docs](https://developers.pipedrive.com/docs/api/v1)

---

## 🔌 5. HUBSPOT vs SALESFORCE vs ZOHO Comparison

### Which CRM to Choose?

**Choose ZOHO if:**
- Budget is tight ($15-65/user/month)
- Small to medium business
- Want easy API access
- Prefer quick implementation
- Need customization

**Choose SALESFORCE if:**
- You're enterprise-level
- Need advanced automation
- Have complex workflows
- Don't mind 1-2 day setup
- Want industry-leading platform

**Choose HUBSPOT if:**
- Focus is marketing/inbound sales
- Want free tier to start
- Need user-friendly interface
- Prefer simplicity
- Like built-in marketing tools

**Choose PIPEDRIVE if:**
- Team is sales-focused
- Budget is moderate ($12-99/user)
- Want visual pipeline management
- Need quick implementation
- Focus is on closing deals

---

## 📝 Environment Variables Template

```env
# Choose ONE CRM integration

# ===== ZOHO CRM =====
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_REFRESH_TOKEN=
ZOHO_API_URL=https://www.zohoapis.com
ZOHO_ORG_ID=

# ===== SALESFORCE =====
SALESFORCE_CLIENT_ID=
SALESFORCE_CLIENT_SECRET=
SALESFORCE_INSTANCE_URL=https://na1.salesforce.com
SALESFORCE_USERNAME=
SALESFORCE_PASSWORD=

# ===== HUBSPOT =====
HUBSPOT_PRIVATE_APP_TOKEN=
HUBSPOT_PORTAL_ID=

# ===== PIPEDRIVE =====
PIPEDRIVE_API_TOKEN=
PIPEDRIVE_COMPANY_DOMAIN=
```

---

## 🔄 Migration Between CRMs

If your client wants to switch CRMs later:

1. **Export data** from current CRM
2. **Map fields** between systems
3. **Batch import** to new CRM
4. **Test data sync** thoroughly
5. **Switch API credentials** in .env
6. **Monitor integration** for 1 week
7. **Keep old system for reference** (30 days)

---

## ⚠️ CRM Integration Tips

### Security:
- ✅ Never share API tokens via email
- ✅ Rotate tokens every 90 days
- ✅ Use separate accounts for dev/prod
- ✅ Store tokens in .env only
- ✅ Use webhook signing for Zoho/Pipedrive

### Performance:
- ✅ Batch API calls (max 100 per call)
- ✅ Use rate limiting (most CRMs: 100 requests/minute)
- ✅ Cache frequently accessed data
- ✅ Schedule syncs during off-hours
- ✅ Monitor API usage dashboards

### Troubleshooting:
- ✅ Check API logs in CRM dashboard
- ✅ Verify field mappings match
- ✅ Test with 1 lead first
- ✅ Monitor error messages
- ✅ Keep audit trail of syncs

---

## 📞 CRM Support Resources

| CRM | Support | Status Page | Community |
|-----|---------|------------|-----------|
| Zoho | [support.zoho.com](https://support.zoho.com) | [status.zoho.com](https://status.zoho.com) | [forums.zoho.com](https://forums.zoho.com) |
| Salesforce | [developer.salesforce.com/support](https://developer.salesforce.com/support) | [trust.salesforce.com](https://trust.salesforce.com) | [salesforce.stackexchange.com](https://salesforce.stackexchange.com) |
| HubSpot | [support.hubspot.com](https://support.hubspot.com) | [status.hubspot.com](https://status.hubspot.com) | [community.hubspot.com](https://community.hubspot.com) |
| Pipedrive | [support.pipedrive.com](https://support.pipedrive.com) | [status.pipedrive.com](https://status.pipedrive.com) | [community.pipedrive.com](https://community.pipedrive.com) |

---

**Created:** February 7, 2026
**Document Version:** 1.0
**Status:** Ready for Client Distribution

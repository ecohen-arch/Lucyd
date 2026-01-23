# Gorgias Setup Guide - Step by Step

## What's Already Done ✅

- [x] **26 Macros Created** (via API)
- [x] **7 Auto-routing Rules** (enable in UI)

## What Needs Manual Setup

Gorgias Flows and Help Center don't have API access. Use this guide for manual setup.

---

## Step 1: Verify Rules Are Enabled

1. Go to: **Settings → Rules**
2. Ensure all 7 rules show "Active":
   - [Auto assign] Order Support
   - [Auto assign] Warranty & Returns
   - [Auto assign] Prescription Services
   - [Auto assign] Sales & Product
   - [Auto assign] Social & Chat
   - [Auto Tag] Identify intents and sentiments
   - [Auto Tag] Identify social questions and leads

---

## Step 2: Create Chat Flows

Go to: **Automate → Flows → Create Flow**

### Flow 1: Order Tracking

**Name:** Order Tracking Self-Service
**Trigger:** Chat message contains: track, tracking, order, shipping, where is, delivery

**Build:**
1. Add Message: "I can help you track your order! 📦 Please provide your order number or email."
2. Add: Wait for customer reply
3. Add: Shopify order lookup action
4. Add: Condition (order found?)
   - Yes → Show tracking info
   - No → Offer agent handoff
5. Add: Quick replies for next steps

### Flow 2: Technical Support

**Name:** Technical Support Self-Service
**Trigger:** Chat message contains: bluetooth, pairing, audio, sound, charging, app, reset, not working

**Build:**
1. Add Message with Quick Replies:
   - "What issue are you experiencing?"
   - Buttons: Bluetooth | Audio | Charging | App | Reset | Other
2. For each button, create branch with troubleshooting steps
3. End each branch with: "Did this help?" → Yes (end) / No (agent)

### Flow 3: Prescription Help

**Name:** Prescription Help Self-Service
**Trigger:** Chat message contains: prescription, Rx, PD, lens, vision

**Build:**
1. Add Message with Quick Replies:
   - Buttons: Submit Rx | Measure PD | Processing Time | Vision Issue | Rx Limits
2. Create content branch for each option
3. Include escalation paths

### Flow 4: Returns & Exchanges

**Name:** Returns & Exchanges Self-Service
**Trigger:** Chat message contains: return, exchange, refund, damaged, wrong item

**Build:**
1. Add Message with Quick Replies:
   - Buttons: Damaged Item | Exchange | Return | Check Status | Policy
2. For damaged/wrong: Collect info → create ticket (high priority)
3. For return/exchange: Check eligibility → process or explain policy

### Flow 5: Welcome Flow (Optional)

**Name:** Welcome & Route
**Trigger:** Chat opened

**Build:**
1. Add Message: "Hi! Welcome to Lucyd. How can I help?"
2. Add Quick Replies:
   - Track Order | Tech Support | Prescription | Returns | Product Questions | Talk to Agent
3. Route each button to appropriate flow or agent

---

## Step 3: Set Up Contact Form Pre-Qualification

Go to: **Settings → Contact Form** or **Help Center → Contact**

**Option A: Use Gorgias Forms**
1. Create custom form with category dropdown
2. Add conditional fields based on category
3. Set auto-tag and routing rules

**Option B: Website Integration**
1. Add pre-qualification popup before form
2. Offer self-service links first
3. Show form only if not resolved

---

## Step 4: Create Help Center

Go to: **Help Center → Settings**

### Create Categories:
1. 🚀 Getting Started
2. 🔧 Troubleshooting
3. 📦 Orders & Shipping
4. 👓 Prescriptions
5. ↩️ Returns & Exchanges
6. 🛡️ Warranty
7. 🛒 Product Info

### Create Articles:
Use content from `gorgias_help_articles.md` file (created below)

---

## Step 5: Configure Chat Widget

Go to: **Settings → Chat**

1. Enable chat widget
2. Set business hours
3. Configure welcome message
4. Enable flow triggers
5. Set up offline message collection

---

## Step 6: Test Everything

1. Open chat widget on website
2. Test each keyword trigger
3. Verify flows route correctly
4. Test form submissions
5. Check ticket tags and team assignment

---

## File Reference

| File | Contents |
|------|----------|
| `gorgias_macros.py` | Script to create/update macros |
| `gorgias_flows_plan.md` | Detailed flow specifications |
| `gorgias_flows_master.md` | Complete summary document |
| `gorgias_help_articles.md` | All 32 article contents |
| `gorgias_setup_guide.md` | This file |

---

## Quick Access URLs

- Dashboard: https://lucyd.gorgias.com
- Flows: https://lucyd.gorgias.com/app/automate/flows
- Macros: https://lucyd.gorgias.com/app/settings/macros
- Rules: https://lucyd.gorgias.com/app/settings/rules
- Chat Settings: https://lucyd.gorgias.com/app/settings/chat
- Help Center: https://lucyd.gorgias.com/app/help-center

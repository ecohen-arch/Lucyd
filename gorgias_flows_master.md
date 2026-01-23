# Lucyd Gorgias Flows - Master Summary

## Overview

This document contains all automated flows for Lucyd customer support across Chat, Help Center, and Contact Form channels.

**Total Implementation:**
- 6 Flows
- 32 Help Center Articles
- 26 Macros (already created)
- 7 Auto-routing Rules (already enabled)

---

## Quick Reference

### Flow Summary

| # | Flow | Channel | Purpose | Expected Deflection |
|---|------|---------|---------|---------------------|
| 1 | Order Tracking | Chat | Self-service order lookup | 40-50% |
| 2 | Technical Support | Chat | Troubleshooting guides | 30-40% |
| 3 | Prescription Help | Chat | Rx submission & support | 25-35% |
| 4 | Returns & Exchanges | Chat | Return/exchange process | 20-30% |
| 5 | Contact Form Pre-Qual | Form | Deflect & smart routing | 30-40% |
| 6 | Help Center | Help Center | Self-service articles | 40-50% |

### Team Routing

| Topic | Team | Tags |
|-------|------|------|
| Orders & Shipping | Order Support | ORDER-STATUS |
| Technical Issues | Order Support | TECH-SUPPORT |
| Prescriptions | Prescription Services | PRESCRIPTION |
| Returns/Exchanges | Warranty & Returns | RETURN/EXCHANGE |
| Warranty Claims | Warranty & Returns | WARRANTY |
| Product Questions | Sales & Product | SALES |
| Social Media | Social & Chat | social-lead |

---

## Flow 1: Order Tracking

### Trigger
- Keywords: track, tracking, order, shipping, where is, delivery, shipped, package
- Button: "📦 Track My Order"

### Flow Diagram
```
[Customer asks about order]
         │
         ▼
[Ask for order # or email]
         │
         ▼
[Shopify Lookup]
         │
    ┌────┴────┐
    │         │
 Found     Not Found
    │         │
    ▼         ▼
[Status?]  [Retry or Agent]
    │
┌───┴───┐
│       │
Shipped Processing
│       │
▼       ▼
[Show   [Show
Track]  Timeline]
```

### Key Messages

**Order Found - Shipped:**
```
Great news! Your order has shipped! 🚚

Order: {{order.name}}
Status: Shipped on {{order.fulfilled_at}}
Tracking: {{order.tracking_url}}

Click the tracking link for real-time updates.
```

**Order Found - Processing:**
```
Your order is being prepared! ⏳

Order: {{order.name}}
Status: Processing

Expected timelines:
• Non-prescription: Ships in 1-3 business days
• Prescription orders: 10-15 business days total

We'll email you tracking info as soon as it ships!
```

**Order Not Found:**
```
I couldn't find an order matching that information. 🔍

Please double-check:
• Order number (check confirmation email)
• Email address used at checkout

Want to try again or speak with our team?
```

### Escalation
- Create ticket with tag: `ORDER-STATUS`, `chat-escalation`
- Assign to: Order Support team

---

## Flow 2: Technical Support

### Trigger
- Keywords: bluetooth, pairing, connect, audio, sound, speaker, charging, charge, battery, app, reset, not working, broken, problem, help, issue
- Button: "🔧 Technical Support"

### Flow Diagram
```
[What issue?]
      │
┌─────┼─────┬─────┬─────┬─────┐
▼     ▼     ▼     ▼     ▼     ▼
BT  Audio Charge App  Reset Other
│     │     │     │     │     │
▼     ▼     ▼     ▼     ▼     │
[Steps][One/ [LED [Setup][Hold │
      Both] Chk]       Btns]  │
│     │     │     │     │     │
▼     ▼     ▼     ▼     ▼     │
[More][HW?] [Clean][Pair][Re- │
Steps      /Try]       pair]  │
│     │     │     │     │     │
└─────┴─────┴─────┴─────┴─────┘
              │
      ┌───────┴───────┐
   Resolved        Not Fixed
      │                │
      ▼                ▼
  [Success!]     [Create Ticket]
```

### Key Troubleshooting Messages

**Bluetooth:**
```
Let's get your glasses connected! 📱

1️⃣ Make sure Bluetooth is ON on your phone
2️⃣ Hold glasses button for 5 seconds → "pairing mode"
3️⃣ Select "Lucyd" in phone Bluetooth settings
4️⃣ You should hear "connected"

Still stuck? Try forgetting "Lucyd" and pairing again.
```

**Audio - Both Sides:**
```
Quick audio checks:

1️⃣ Phone media volume turned up
2️⃣ Tap RIGHT temple to increase glasses volume
3️⃣ Verify "Lucyd" is selected audio output
4️⃣ Try factory reset: hold BOTH buttons 10 sec
```

**Audio - One Side:**
```
Audio on one side may indicate hardware issue.

First try: Factory reset (hold BOTH buttons 10 sec)

If still one-sided after reset, this is likely covered under warranty. Let me connect you with our team.
```

**Charging:**
```
Charging troubleshooting:

1️⃣ Check magnetic connection snaps firmly
2️⃣ Clean contacts with dry cloth
3️⃣ Try different USB port/adapter
4️⃣ LED should light when connected

No LED = connection issue. LED on = receiving power.
```

**Factory Reset:**
```
Factory Reset Instructions:

1️⃣ Make sure glasses are ON and charged
2️⃣ Hold BOTH temple buttons for 10 seconds
3️⃣ Wait for confirmation tone
4️⃣ Re-pair with phone after reset

This fixes 70% of connectivity and audio issues!
```

### Escalation
- Create ticket with tags: `TECH-SUPPORT`, `{{issue_type}}`
- Hardware issues add: `WARRANTY`
- Assign to: Order Support team

---

## Flow 3: Prescription Help

### Trigger
- Keywords: prescription, Rx, PD, pupillary, lens, vision, eye doctor, progressive, bifocal
- Button: "💊 Prescription Help"

### Flow Diagram
```
[What Rx help?]
      │
┌─────┼─────┬─────┬─────┬─────┐
▼     ▼     ▼     ▼     ▼     ▼
Submit Measure Process Vision Limits Other
Rx     PD    Time  Issue       │
│      │      │      │     │   │
▼      ▼      ▼      ▼     ▼   │
[3    [App/  [Time-[How  [Show │
Ways] Mirror]line] Long?]Range]│
│      │      │      │     │   │
▼      ▼      ▼      ▼     ▼   │
[Req.][Steps][Check][Adj/ [Lens│
             Status]Escal]Opts]│
└──────┴──────┴──────┴─────┴───┘
              │
      ┌───────┴───────┐
   Resolved        Needs Help
      │                │
      ▼                ▼
  [Shop Link]    [Rx Team Ticket]
```

### Key Messages

**Submit Prescription:**
```
3 ways to submit your prescription:

1️⃣ Upload during checkout (photo or enter values)
2️⃣ Email to info@lucyd.co with your order number
3️⃣ We contact your doctor (share their info)

Requirements:
• Dated within 2 years
• Include SPH, CYL, Axis, PD
```

**PD Measurement:**
```
Measure PD with the Lucyd app:

1️⃣ Download Lucyd app
2️⃣ Open "Measure PD" feature
3️⃣ Hold credit card to forehead (for scale)
4️⃣ Look at camera → auto-calculates!

Manual method: Mirror + mm ruler at 8 inches, measure between pupils.
```

**Processing Timeline:**
```
Prescription order timeline:

📋 Rx Verification: 1-2 business days
🔬 Lens Crafting: 5-7 business days
✅ Quality Check: 1 business day
📦 Shipping: 3-5 business days

Total: 10-15 business days
```

**Vision Issues:**
```
Adjustment period (1-2 weeks) is normal:
• Mild headaches, eye strain
• Slight edge distortion
• Progressives: finding sweet spots

NOT normal (contact us):
• Severe headaches, double vision
• Significant blur that doesn't improve
• Dizziness or nausea
```

**Prescription Limits:**
```
We can fill:

Single Vision: SPH ±8.00, CYL ±4.00
Progressive: SPH ±6.00, CYL ±3.00, ADD +3.00

Lens options: Clear, Blue Light, Photochromic, Polarized
```

### Escalation
- Create ticket with tags: `PRESCRIPTION`, `{{specific_issue}}`
- Vision issues add: `vision-issue`, `remake-review`
- Assign to: Prescription Services team

---

## Flow 4: Returns & Exchanges

### Trigger
- Keywords: return, exchange, refund, send back, damaged, broken, wrong item, doesn't fit
- Button: "↩️ Returns & Exchanges"

### Flow Diagram
```
[What do you need?]
        │
┌───────┼───────┬───────┬───────┐
▼       ▼       ▼       ▼       ▼
Damaged Exchange Return Status Policy
│       │       │       │       │
▼       ▼       ▼       ▼       ▼
[Photo][Size/  [30    [Track][Full
Collect]Style] Days?] Pkg]  Info]
│       │       │       │       │
▼       ▼       ▼       │       │
[Agent][Details][Rx?]   │       │
              │         │       │
              ▼         │       │
        [Eligible?]     │       │
              │         │       │
      ┌───────┴───────┐ │       │
   Yes, Process    No, Policy  │
      │                │        │
      └────────────────┴────────┘
                  │
          [Create Ticket]
```

### Key Messages

**Return Policy:**
```
Return Policy:

Non-Prescription:
✅ 30 days from delivery
✅ Full refund, free return shipping
✅ Must be unworn, tags attached

Prescription:
⚠️ Lenses non-refundable (custom-made)
✅ Frame exchanges available
✅ Vision issues → free remake
✅ Defects → full replacement
```

**Damaged Item:**
```
Sorry your item arrived damaged! 😔

To process replacement:
1. Order number
2. Photos of damage
3. Description of issue

We'll ship replacement immediately!
```

**Exchange Process:**
```
Free exchanges within 30 days!

How it works:
1. Tell us what you want to exchange for
2. We send prepaid return label
3. Ship back current pair
4. We ship new selection

Turnaround: 5-7 business days
```

**Refund Timeline:**
```
After we receive your return:

• Processing: 1-2 business days
• Refund issued: 3-5 business days
• Appears in account: 3-5 more days

Total: 7-12 business days
```

### Escalation
- Create ticket with tags: `RETURN/EXCHANGE`, `{{request_type}}`
- Damaged/wrong item: Priority HIGH
- Assign to: Warranty & Returns team

---

## Flow 5: Contact Form Pre-Qualification

### Trigger
- Contact page visited
- "Contact Us" clicked

### Flow Diagram
```
[Before you submit...]
         │
         ▼
[What do you need help with?]
         │
┌────────┼────────┬────────┬────────┬────────┬────────┐
▼        ▼        ▼        ▼        ▼        ▼        ▼
Order   Tech     Rx     Return Warranty Sales  Other
│        │        │        │        │        │        │
▼        ▼        ▼        ▼        ▼        ▼        │
[Quick  [Quick   [Quick  [Quick  [Quick  [Quick      │
 Solve?] Fix?]   Ans?]   Check]  Check]  Ans?]      │
│        │        │        │        │        │        │
▼        ▼        ▼        ▼        ▼        ▼        │
Resolved OR ─────────────────────────────────────────┘
         │
         ▼
[SMART CONTACT FORM]
(Dynamic fields by category)
         │
         ▼
[Auto-tag & Route]
         │
         ▼
[Confirmation]
```

### Self-Service Deflection Points

| Category | Quick Solution Offered |
|----------|----------------------|
| Order | Track order lookup |
| Tech | Reset instructions, quick fixes |
| Rx | Submission info, PD guide |
| Return | Policy check, eligibility |
| Warranty | Coverage check, troubleshoot first |
| Sales | FSA info, sizing guide, compatibility |

### Dynamic Form Fields

**Order Issues:**
- Email (required)
- Order Number (required)
- Issue Type: Status / Change / Cancel / Delivery
- Description

**Technical Issues:**
- Email (required)
- Order Number
- Issue Type: Bluetooth / Audio / Charging / App
- Tried Reset? Yes/No
- Description

**Prescription:**
- Email (required)
- Order Number (required)
- Issue Type: Submit Rx / PD / Processing / Vision
- Prescription Upload (optional)
- Description

**Returns:**
- Email (required)
- Order Number (required)
- Request Type: Return / Exchange / Damaged
- Reason dropdown
- Photos (optional)

**Warranty:**
- Email (required)
- Order Number (required)
- Purchase Date
- Issue Description
- Photos (required)

**Sales:**
- Email (required)
- Question Type: Pricing / Features / Sizing / FSA
- Question text

### Auto-Routing

| Category | Team | Priority |
|----------|------|----------|
| Order | Order Support | Normal |
| Order (urgent) | Order Support | High |
| Tech | Order Support | Normal |
| Rx | Prescription Services | Normal |
| Rx (vision) | Prescription Services | High |
| Return | Warranty & Returns | Normal |
| Return (damaged) | Warranty & Returns | High |
| Warranty | Warranty & Returns | Normal |
| Sales | Sales & Product | Normal |
| Other | Order Support | Normal |

---

## Flow 6: Help Center Articles

### Article Structure

**32 Total Articles across 7 Categories:**

#### 🚀 Getting Started (4)
1. First-Time Setup Guide
2. Bluetooth Pairing Guide
3. Lucyd App Setup
4. Touch Controls Guide

#### 🔧 Troubleshooting (6)
1. Bluetooth Won't Connect
2. No Audio / Sound Issues
3. Charging Problems
4. One Speaker Not Working
5. App Issues
6. Factory Reset Guide

#### 📦 Orders & Shipping (5)
1. Track My Order
2. Shipping Times
3. International Shipping
4. Change or Cancel Order
5. Order Not Received

#### 👓 Prescriptions (5)
1. How to Submit Prescription
2. PD Measurement Guide
3. Prescription Requirements
4. Rx Processing Time
5. Vision Problems with New Glasses

#### ↩️ Returns & Exchanges (4)
1. Return Policy
2. Start a Return
3. Start an Exchange
4. Refund Timeline

#### 🛡️ Warranty (3)
1. Warranty Coverage
2. File Warranty Claim
3. Out of Warranty Options

#### 🛒 Product Info (5)
1. FSA/HSA Eligibility
2. Sizing Guide
3. Phone Compatibility
4. Battery & Charging
5. Water Resistance

### Article Features
- Reading time indicator
- "Was this helpful?" feedback
- Related articles suggestions
- Easy escalation to chat/email
- Search functionality

---

## Implementation Checklist

### Phase 1: Foundation ✅
- [x] Create 26 macros
- [x] Enable 7 auto-routing rules
- [ ] Set up Help Center articles

### Phase 2: Chat Flows
- [ ] Order Tracking flow
- [ ] Technical Support flow
- [ ] Prescription Help flow
- [ ] Returns & Exchanges flow

### Phase 3: Forms & Help Center
- [ ] Contact Form Pre-Qualification
- [ ] Help Center article organization
- [ ] Search configuration
- [ ] Feedback collection

### Phase 4: Testing & Optimization
- [ ] Test all flow branches
- [ ] Verify auto-routing
- [ ] Monitor deflection rates
- [ ] Gather feedback and iterate

---

## Metrics Dashboard

### Key Performance Indicators

| Metric | Target | Measure |
|--------|--------|---------|
| Self-service rate | 35%+ | Resolved without agent |
| Flow completion | 70%+ | Users finish vs abandon |
| First response time | <5 min | Auto-responses count |
| CSAT | 4.0+ | Post-interaction survey |
| Ticket volume reduction | -25% | Month-over-month |

### Tracking by Flow

| Flow | Deflection Target | KPI |
|------|-------------------|-----|
| Order Tracking | 40-50% | Orders tracked without ticket |
| Technical Support | 30-40% | Issues resolved via reset |
| Prescription Help | 25-35% | Questions answered |
| Returns | 20-30% | Policy understood |
| Contact Form | 30-40% | Deflected before submit |
| Help Center | 40-50% | Article → no ticket |

---

## Quick Links

- Gorgias Dashboard: https://lucyd.gorgias.com
- Rules Settings: https://lucyd.gorgias.com/app/settings/rules
- Macros: https://lucyd.gorgias.com/app/settings/macros
- Flows: https://lucyd.gorgias.com/app/automate/flows
- Help Center: https://lucyd.gorgias.com/app/settings/help-center

---

## Support Contacts

**Escalation Path:**
1. Self-service (flows/articles)
2. Chat with agent
3. Email ticket
4. Phone callback (if offered)

**Internal Teams:**
- Order Support: Orders, shipping, general tech
- Prescription Services: Rx submission, vision issues
- Warranty & Returns: Returns, exchanges, warranty claims
- Sales & Product: Pre-sale questions, product info
- Social & Chat: Instagram, Facebook, live chat

---

*Document created: January 2026*
*Last updated: January 2026*
*Version: 1.0*

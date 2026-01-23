# Gorgias Flows Plan for Lucyd

## Overview

Flows automate customer interactions on Chat, Help Center, and Contact Forms. Based on your ticket data:
- **Top intents**: Order Status, Product Quality Issues, Returns, Warranty Claims
- **Channels**: Email 78%, Facebook 16%, Instagram 6%

---

## Recommended Flows by Channel

### 1. Chat Widget Flows

#### Flow 1.1: Welcome & Intent Detection
**Trigger**: Chat opened
**Purpose**: Greet and route customers to self-service or agent

```
[Welcome Message]
"Hi! 👋 Welcome to Lucyd. How can I help you today?"

[Quick Reply Buttons]
├── 🚚 Track My Order
├── 🔧 Technical Support
├── 💊 Prescription Help
├── ↩️ Returns & Exchanges
├── 🛒 Product Questions
└── 💬 Talk to Agent
```

---

#### Flow 1.2: Order Tracking (Self-Service)
**Trigger**: "Track My Order" button OR keywords: track, order, shipping, where is

```
[Ask for Order Info]
"I can help you track your order! Please provide your order number or the email used for purchase."

[Customer provides info]
   │
   ├── [Order Found - Shipped]
   │   "Great news! Your order #{{order_number}} shipped on {{ship_date}}.
   │    Tracking: {{tracking_link}}
   │    Estimated delivery: {{delivery_date}}"
   │   [Buttons: "Track Package" | "Something Else" | "Talk to Agent"]
   │
   ├── [Order Found - Processing]
   │   "Your order #{{order_number}} is being prepared.
   │    Prescription orders: 10-15 business days
   │    Non-Rx orders: 3-5 business days
   │    We'll email you when it ships!"
   │   [Buttons: "OK, Thanks" | "I Need It Faster" | "Talk to Agent"]
   │
   └── [Order Not Found]
       "I couldn't find an order with that information.
        Please double-check the order number or email.
        Or I can connect you with our team."
       [Buttons: "Try Again" | "Talk to Agent"]
```

---

#### Flow 1.3: Technical Support
**Trigger**: "Technical Support" button OR keywords: bluetooth, connect, pairing, audio, charging, app

```
[Ask Issue Type]
"What issue are you experiencing with your Lucyd glasses?"

[Quick Reply Buttons]
├── 📱 Bluetooth/Pairing Issues
├── 🔊 Audio Problems
├── 🔋 Charging Issues
├── 📲 App Setup Help
└── 🔄 Need to Reset

[Based on Selection]
   │
   ├── [Bluetooth/Pairing]
   │   "Let's get your glasses connected! Try these steps:
   │    1. Enable Bluetooth on your phone
   │    2. Hold the glasses button for 5 seconds until you hear 'pairing mode'
   │    3. Select 'Lucyd' in your phone's Bluetooth settings
   │
   │    Still having trouble? Try forgetting 'Lucyd' from your
   │    Bluetooth list and pairing again."
   │   [Buttons: "That Worked!" | "Still Not Working" | "Talk to Agent"]
   │
   ├── [Audio Problems]
   │   "Sorry to hear about the audio issue! Quick checks:
   │    1. Ensure glasses are charged (20%+ recommended)
   │    2. Check phone media volume isn't muted
   │    3. Tap right temple to increase volume
   │
   │    Is sound missing from one side or both?"
   │   [Buttons: "One Side" | "Both Sides" | "Fixed It!"]
   │       │
   │       ├── [One Side] → "This may be a hardware issue. Let me
   │       │                  connect you with our warranty team."
   │       │                 [Create ticket, assign to Warranty team]
   │       │
   │       └── [Both Sides] → "Try a factory reset: Hold BOTH temple
   │                           buttons for 10 seconds. Then re-pair."
   │                          [Buttons: "That Worked!" | "Talk to Agent"]
   │
   ├── [Charging Issues]
   │   "Let's troubleshoot charging:
   │    1. Check magnetic pins align with charging contacts
   │    2. Try a different USB port/adapter
   │    3. Clean contacts with dry cloth
   │    4. Look for LED light when connected
   │
   │    Is the LED lighting up when you connect the charger?"
   │   [Buttons: "Yes, LED On" | "No LED" | "Talk to Agent"]
   │
   ├── [App Setup]
   │   "Here's how to set up the Lucyd app:
   │    1. Download from App Store or Google Play
   │    2. Create account or sign in
   │    3. Ensure glasses are on and charged
   │    4. Tap 'Add Device' and follow prompts
   │
   │    Download: [App Store Link] | [Google Play Link]"
   │   [Buttons: "All Set!" | "Having Issues" | "Talk to Agent"]
   │
   └── [Reset]
       "To factory reset your Lucyd glasses:
        1. Make sure glasses are on and charged
        2. Hold BOTH temple buttons for 10 seconds
        3. You'll hear a confirmation tone
        4. Re-pair with your phone after reset

        This fixes most connectivity and audio glitches!"
       [Buttons: "That Helped!" | "Still Having Issues"]
```

---

#### Flow 1.4: Prescription Help
**Trigger**: "Prescription Help" button OR keywords: prescription, Rx, PD, lens, vision

```
[Ask Rx Question Type]
"How can I help with your prescription order?"

[Quick Reply Buttons]
├── 📤 Submit My Prescription
├── 📏 Measure My PD
├── ⏱️ Check Processing Time
├── 👓 Vision Seems Off
└── ❓ Rx Limits/Questions

[Based on Selection]
   │
   ├── [Submit Prescription]
   │   "You can submit your prescription 3 ways:
   │
   │    1. Upload during checkout (photo or enter values)
   │    2. Email to info@lucyd.co with your order number
   │    3. Share your eye doctor's info and we'll request it
   │
   │    Your Rx must be less than 2 years old and include
   │    SPH, CYL, Axis, and PD values."
   │   [Buttons: "Got It!" | "What's PD?" | "Talk to Agent"]
   │
   ├── [Measure PD]
   │   "PD (Pupillary Distance) measures the space between your pupils.
   │
   │    Easiest method - Use our app:
   │    1. Open Lucyd app → 'Measure PD'
   │    2. Follow camera instructions
   │    3. App calculates automatically!
   │
   │    Or check your prescription - PD is often included."
   │   [Buttons: "Thanks!" | "Need Manual Method" | "Talk to Agent"]
   │       │
   │       └── [Manual Method]
   │           "Manual PD measurement:
   │            1. Stand 8 inches from mirror
   │            2. Hold ruler against your brow
   │            3. Close right eye, align 0 with left pupil
   │            4. Close left eye, open right
   │            5. Read measurement at right pupil (usually 57-72mm)"
   │
   ├── [Processing Time]
   │   "Prescription order timeline:
   │
   │    • Rx verification: 1-2 business days
   │    • Lens crafting: 5-7 business days
   │    • Quality check: 1 business day
   │    • Shipping: 3-5 days (standard)
   │
   │    Total: 10-15 business days
   │
   │    You'll get email updates at each stage!"
   │   [Buttons: "OK, Thanks" | "Need It Faster" | "Talk to Agent"]
   │
   ├── [Vision Seems Off]
   │   "Sorry your vision isn't right! A few questions:
   │
   │    • How long have you been wearing them?
   │      (1-2 week adjustment period is normal)
   │    • Is it blurry at certain distances?
   │    • Do you have headaches or eye strain?
   │
   │    Let me connect you with our Rx team to help."
   │   [Create ticket, assign to Prescription Services team]
   │
   └── [Rx Limits]
       "Our prescription capabilities:

        Single Vision: SPH ±8.00, CYL ±4.00
        Progressive: SPH ±6.00, CYL ±3.00
        Reading ADD: up to +3.00

        Lens options: Clear, Blue Light, Photochromic, Polarized

        Outside these ranges? Send your Rx and we'll check!"
       [Buttons: "Start Order" | "Send My Rx" | "Talk to Agent"]
```

---

#### Flow 1.5: Returns & Exchanges
**Trigger**: "Returns & Exchanges" button OR keywords: return, exchange, refund, damaged

```
[Ask Return Type]
"I can help with returns and exchanges. What's your situation?"

[Quick Reply Buttons]
├── 📦 Item Arrived Damaged
├── 🔄 Want to Exchange
├── ↩️ Want to Return
└── 🕐 Check Return Status

[Based on Selection]
   │
   ├── [Damaged Item]
   │   "I'm sorry your item arrived damaged!
   │
   │    Please provide:
   │    1. Your order number
   │    2. Photos of the damage
   │
   │    We'll get a replacement sent right away."
   │   [Collect info → Create ticket for Warranty team]
   │
   ├── [Exchange]
   │   "We're happy to help with an exchange!
   │
   │    Within 30 days of delivery:
   │    • Different style/color: Free exchange
   │    • Different size: Free exchange
   │
   │    Please share your order number and what
   │    you'd like to exchange for."
   │   [Collect info → Create ticket]
   │
   ├── [Return]
   │   "Our return policy:
   │
   │    • 30 days from delivery
   │    • Items must be unworn with tags
   │    • Prescription lenses: Non-refundable (custom made)
   │    • Non-Rx frames: Full refund
   │
   │    Ready to start a return?"
   │   [Buttons: "Yes, Start Return" | "Questions First"]
   │
   └── [Return Status]
       "To check your return status, please provide
        your order number or return tracking number."
       [Collect info → Look up status]
```

---

#### Flow 1.6: Product Questions (Pre-Sale)
**Trigger**: "Product Questions" button OR keywords: FSA, HSA, size, battery, waterproof, compatible

```
[Ask Product Question]
"What would you like to know about Lucyd glasses?"

[Quick Reply Buttons]
├── 💰 FSA/HSA Eligible?
├── 📐 Sizing Help
├── 🔋 Battery Life
├── 💧 Water Resistant?
├── 📱 Phone Compatibility
└── 🕶️ Lens Options

[Based on Selection - serve content from macros]
   │
   ├── [FSA/HSA] → Display Product: FSA/HSA Eligibility content
   ├── [Sizing] → Display Product: Frame Sizing Guide content
   ├── [Battery] → Display Product: Battery Life Info content
   ├── [Water] → Display Product: Water Resistance content
   ├── [Compatibility] → Display Product: Compatibility Check content
   └── [Lenses] → Display Product: Lens Options content

[End each with]
[Buttons: "Shop Now" | "Another Question" | "Talk to Agent"]
```

---

### 2. Help Center Flows

#### Flow 2.1: Article Suggestions
**Trigger**: Customer lands on Help Center

```
[Search Bar + Popular Topics]
"Search for answers or browse popular topics:"

[Topic Cards]
├── Getting Started
│   ├── Bluetooth Pairing Guide
│   ├── App Setup Tutorial
│   └── First-Time User Tips
│
├── Troubleshooting
│   ├── Audio Not Working
│   ├── Charging Problems
│   └── Factory Reset Guide
│
├── Orders & Shipping
│   ├── Track My Order
│   ├── Shipping Times
│   └── International Delivery
│
├── Prescriptions
│   ├── How to Submit Rx
│   ├── PD Measurement Guide
│   └── Rx Processing Time
│
└── Returns & Warranty
    ├── Return Policy
    ├── Start a Return
    └── Warranty Coverage
```

---

#### Flow 2.2: Contact Form Pre-Qualification
**Trigger**: Customer clicks "Contact Us" or "Submit Request"

```
[Before Form]
"Before submitting, can we help you faster?"

[Quick Solutions]
├── Track Order → [Order lookup tool]
├── Technical Issue → [Troubleshooting flow]
├── Return Request → [Return initiation flow]
└── Something Else → [Show contact form]

[If Contact Form Shown]
Required fields:
• Email
• Order Number (optional but helpful)
• Category [Dropdown]:
  - Order Status
  - Technical Support
  - Prescription Help
  - Returns/Exchanges
  - Warranty Claim
  - Product Question
  - Other
• Description

[Auto-actions on submit]
- Auto-tag based on category
- Auto-assign to appropriate team
- Send confirmation email with ticket number
```

---

### 3. Contact Form Flows

#### Flow 3.1: Smart Contact Form
**Trigger**: Contact form accessed

```
[Step 1: Category Selection]
"What can we help you with?"
○ Order & Shipping
○ Technical Support
○ Prescription Services
○ Returns & Exchanges
○ Warranty Claim
○ Product Questions
○ Other

[Step 2: Dynamic Fields Based on Category]

If "Order & Shipping":
  • Order Number (required)
  • Issue Type: [Status | Change Address | Cancel | Other]

If "Technical Support":
  • Order Number
  • Issue Type: [Bluetooth | Audio | Charging | App | Other]
  • Already tried reset? [Yes | No]

If "Prescription Services":
  • Order Number
  • Issue Type: [Submit Rx | PD Help | Vision Issue | Other]
  • Attach prescription (optional)

If "Returns & Exchanges":
  • Order Number (required)
  • Request Type: [Return | Exchange | Damaged Item]
  • Reason: [Dropdown]

If "Warranty Claim":
  • Order Number (required)
  • Purchase Date
  • Issue Description
  • Photos (required)

If "Product Questions":
  • Question Type: [Sizing | Features | Compatibility | Pricing]
  • [Show relevant FAQ first]

[Step 3: Final Submission]
• Email (required)
• Additional Details
• [Submit Button]

[Post-Submit]
• Auto-assign to correct team
• Auto-tag with category
• Send confirmation with expected response time
```

---

## Implementation Priority

### Phase 1: High Impact (Week 1)
| Flow | Channel | Expected Deflection |
|------|---------|---------------------|
| Order Tracking | Chat | 30-40% of order inquiries |
| Technical Support | Chat | 20-30% of tech issues |
| Contact Form Pre-Qual | Form | 15-20% of submissions |

### Phase 2: Medium Impact (Week 2)
| Flow | Channel | Expected Deflection |
|------|---------|---------------------|
| Prescription Help | Chat | 25-35% of Rx questions |
| Returns Flow | Chat | 20-30% of return requests |
| Help Center Topics | Help Center | Ongoing self-service |

### Phase 3: Optimization (Week 3+)
| Flow | Channel | Purpose |
|------|---------|---------|
| Product Questions | Chat | Pre-sale conversion |
| Welcome Flow | Chat | Better routing |
| Form Optimization | Form | Faster resolution |

---

## Setup Instructions

### Creating a Flow in Gorgias

1. Go to **Automate → Flows**
2. Click **Create Flow**
3. Choose trigger:
   - Chat opened
   - Keyword detected
   - Button clicked
4. Add steps:
   - **Message**: Text to display
   - **Quick Replies**: Button options
   - **Condition**: Branch based on response
   - **Action**: Create ticket, assign team, add tags
5. Test the flow
6. Publish

### Connecting Flows to Macros

When a flow ends with "Talk to Agent":
1. Create ticket automatically
2. Apply relevant tags (from macro tag list)
3. Assign to appropriate team
4. Pre-populate ticket with flow conversation context

### Recommended Settings

- **Business Hours**: Show "Talk to Agent" only during business hours
- **Fallback**: After 2 failed intent matches → offer agent
- **Handoff**: Always offer human option within 3 clicks
- **Context**: Pass all flow data to agent when escalating

---

## Metrics to Track

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Self-service rate | 30%+ | Resolved without agent |
| Flow completion | 70%+ | Users finish flow vs abandon |
| CSAT for flow users | 4.0+ | Post-interaction survey |
| Avg handle time | -20% | Time savings on escalated tickets |
| First response time | <5 min | Auto-responses count |

---

## Quick Reference: Flow → Team Mapping

| Flow Topic | Assign To | Tags |
|------------|-----------|------|
| Order Tracking | Order Support | ORDER-STATUS |
| Technical Issues | Order Support | TECH-SUPPORT |
| Prescription | Prescription Services | PRESCRIPTION |
| Returns/Exchanges | Warranty & Returns | RETURN/EXCHANGE |
| Warranty Claims | Warranty & Returns | WARRANTY |
| Product Questions | Sales & Product | SALES |
| Social Inquiries | Social & Chat | social-lead |

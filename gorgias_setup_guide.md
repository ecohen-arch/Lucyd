# Gorgias Manual Setup Guide
## Remaining Configuration Steps

---

## What's Already Done

- [x] 34 macros created via API (26 original + 8 new)
- [x] 11 auto-routing rules created via API (7 original + 4 new)
- [x] All 6 documentation files updated and pushed to GitHub
- [x] Paste-ready articles file created (`gorgias_articles_paste_ready.md`)

---

## Step 1: Paste 10 New Articles into Help Center

**Path:** Settings → Help Center → click the "lucyd" row → Open Help Center

For each article in `gorgias_articles_paste_ready.md`:

1. Click **"New Article"** (or "Create Article")
2. Enter the **Title** exactly as listed
3. Assign to the correct **Category** (create category if it doesn't exist)
4. Paste the body content from below the `--- PASTE BELOW THIS LINE ---` marker
5. Add **Tags** as listed
6. Click **Publish**

### Article Order (do critical ones first):

| Priority | # | Title | Category |
|----------|---|-------|----------|
| CRITICAL | 1 | My Frames Are Broken -- What Are My Options? | Warranty & Protection |
| CRITICAL | 2 | How to Photograph Damage for a Warranty Claim | Warranty & Protection |
| CRITICAL | 3 | Warranty vs Accidental Damage: What's Covered? | Warranty & Protection |
| CRITICAL | 4 | Frame Damage Assessment Guide | Warranty & Protection |
| CRITICAL | 5 | Broken Frames FAQ: Hinges, Temples, Nose Bridge | Warranty & Protection |
| P1 | 6 | Current Promotions & How to Apply Discount Codes | Product Info |
| P1 | 7 | Amazon Orders: How to Get Support | Orders & Shipping |
| P1 | 8 | Wholesale & Partnership Inquiries | Product Info |
| P1 | 9 | Lucyd Pro Insurance: Is It Worth It? | Warranty & Protection |
| P1 | 10 | Common Frame Issues & When to Contact Us | Warranty & Protection |

---

## Step 2: Update 4 Existing Articles

**Path:** Settings → Help Center → Open Help Center → find each article → Edit

### 2a: Warranty Coverage (Article 6.1)
- **Find** the "COVERED" and "NOT COVERED" sections
- **Add** to COVERED list:
  - Hinge/frame defects (not from drops)
  - Frame stress cracks from normal use
  - Joint separation during normal handling
  - Screw holes that strip or fail
- **Add** to NOT COVERED list:
  - Accidental frame breakage (drops, bending, crushing)
  - Heat damage (left in hot car, near heat source)
- **Add new section** "FRAME DAMAGE CLASSIFICATION" at the bottom:
  - Hinge breaks during normal use → Covered (warranty)
  - Frame cracks at stress point, no impact → Covered (warranty)
  - Temple snaps from a drop → Not covered (accidental)
  - Sat on glasses → Not covered (accidental)
  - Nose bridge cracks, no impact → Covered (manufacturing flaw)
  - Link to "Warranty vs Accidental Damage" article

### 2b: Out of Warranty Options (Article 6.3)
- **Find** the "Physical Damage" section (or add at bottom)
- **Replace/add** with options:
  - Lucyd Pro Insurance: file an insurance claim (deductible applies)
  - Discounted replacement frames: loyal customer pricing
  - Paid repair: some frame damage can be repaired for a fee
  - Rx lens transfer: prescription lenses may transfer to new frame of same model
  - Upgrade trade-in: ask about trade-in programs
  - Link to "My Frames Are Broken" article

### 2c: How to File a Warranty Claim (Article 6.2)
- **Find** the "What You'll Need" section
- **Add** after existing items:
  - FOR BROKEN FRAME CLAIMS SPECIFICALLY:
  - 2-3 photos from different angles (link to photo guide article)
  - Description of how the damage happened (normal use vs. drop/impact)
  - Whether you have Lucyd Pro insurance

### 2d: Return Policy (Article 5.1)
- **Find** the "Damaged/Defective Items" section
- **Add** subsection "DAMAGED IN TRANSIT VS. CUSTOMER-DAMAGED":
  - Arrived damaged from shipping → Full replacement, no return needed
  - Frame broke from a drop/accident → Not covered by warranty
  - Manufacturing defect after use → Warranty replacement
- **Add** to "NOT ELIGIBLE" list:
  - Accidental damage (see warranty/insurance options instead)

> Full paste-ready text for all 4 updates is at the bottom of `gorgias_articles_paste_ready.md` under "UPDATED ARTICLES (4)"

---

## Step 3: Update Chat Widget Quick-Reply Buttons

**Path:** Settings → Chat → select your chat widget → Campaigns or Welcome Message

Reorder buttons so "My Frames Are Broken/Damaged" is **first**:

| Position | Button Text |
|----------|-------------|
| **1 (NEW)** | **My Frames Are Broken/Damaged** |
| 2 | Track My Order |
| 3 | Technical Support |
| 4 | Prescription Help |
| 5 | Returns & Exchanges |
| 6 | Talk to Someone |

### Steps:
1. Go to **Settings → Chat**
2. Click your active chat widget
3. Find **Welcome Message** or **Quick Replies** section
4. Add "My Frames Are Broken/Damaged" as the first button
5. Reorder remaining buttons as shown above
6. Save

---

## Step 4: Build Broken Frames Triage Flow

**Path:** Settings → Flows → Create Flow

### Flow Name: "Broken Frames Triage"
### Trigger: Customer selects "My Frames Are Broken/Damaged" OR message matches broken frame keywords

### Step 4a: Initial Message
```
We're sorry to hear about your damaged frames! Let's get this sorted out quickly.

To help you, I need a few things:
1. Your order number
2. 2-3 photos of the damage from different angles
3. A brief description of how the damage happened

Could you start by sharing your order number?
```

### Step 4b: Collect Order Number
- Wait for customer response
- Store as variable: `{order_number}`

### Step 4c: Ask About Damage Cause
```
Thanks! Now, could you describe how the damage happened?
```
Quick reply buttons:
- "Broke during normal use"
- "Dropped / impact"
- "Other accident"

### Step 4d: Branch on Damage Cause

**If "Broke during normal use" →**
```
This may be covered under your 1-year warranty. To verify, please send us 2-3 photos:
- One overall photo of the glasses
- One close-up of the damaged area
- One showing the break point

Our warranty team will review and get back to you within 1 business day.
```
- Auto-tag: `WARRANTY`, `broken-frame`, `potential-defect`
- Assign to: Warranty & Returns team (ID: 4140)

**If "Dropped / impact" or "Other accident" →**
```
I understand — accidents happen! Unfortunately, accidental damage isn't covered by the standard warranty, but you still have options.

Do you have Lucyd Pro insurance on this pair?
```
Quick reply: "Yes, I have Lucyd Pro" / "No" / "Not sure"

### Step 4e: Accidental Damage Sub-Branch

**If "Yes, I have Lucyd Pro" →**
```
Great news! Lucyd Pro covers accidental damage. Please send us:
- 2-3 photos of the damage
- Your order number (if not already provided)

We'll start your insurance claim right away. A small deductible applies.
```
- Auto-tag: `WARRANTY`, `broken-frame`, `insurance-claim`
- Assign to: Warranty & Returns team

**If "No" or "Not sure" →**
```
Here are your options:

• Discounted Replacement — Special pricing for existing customers
• Paid Repair — Some damage can be repaired (we'll quote after seeing photos)
• Upgrade Trade-In — Trade your damaged pair toward new glasses

Please send 2-3 photos of the damage, and we'll recommend the best option for you.
```
- Auto-tag: `WARRANTY`, `broken-frame`, `out-of-warranty`
- Assign to: Warranty & Returns team

### Step 4f: Handoff (all paths end here)
```
Thank you! I've created a case for our warranty team. They'll review your photos and get back to you within 1 business day with your best options.

Is there anything else I can help with?
```
- Create ticket with all collected info
- Priority: HIGH

---

## Step 5: Update Welcome Flow

**Path:** Settings → Flows → find Welcome/Greeting flow → Edit

1. Add "My Frames Are Broken/Damaged" as the **first** quick-reply button
2. Connect it to the Broken Frames Triage flow (Step 4)
3. Verify all other buttons still route correctly
4. Save

---

## Step 6: Configure AI Agent Persona

**Path:** AI Agent → Settings / Configuration

### Persona:
- **Name:** Lucyd Support (or preferred name)
- **Tone:** Friendly, concise, empathetic, solution-oriented
- **Language:** English only
- **Response length:** Short to medium

### Greeting Message:
```
Hi! I'm here to help with your Lucyd smart eyewear. What can I help you with today?
```

---

## Step 7: Set AI Agent Guardrails

**Path:** AI Agent → Settings → Instructions / Guardrails

Paste the following into the AI Agent instructions:

```
CRITICAL RULES — NEVER VIOLATE:

1. NEVER promise warranty coverage before human review
2. NEVER process refunds, cancellations, or any money movement
3. NEVER create or promise discount codes
4. NEVER make medical or vision recommendations
5. ALWAYS collect order number before discussing specific orders
6. ALWAYS ask for photos before classifying frame damage
7. ALWAYS offer human handoff if customer expresses frustration
8. Maximum 4 back-and-forth messages before offering a live agent
9. After 2 failed intent matches, offer to connect with an agent
10. For broken frames: collect order#, photos, damage description, and insurance status before creating ticket

TOPIC RESTRICTIONS:
- Only discuss Lucyd products, orders, and support
- Do not discuss competitors
- Do not speculate about future products or features
- Do not discuss company financials or stock

ESCALATION TRIGGERS (immediately route to human):
- Customer mentions lawyer, legal action, or lawsuit
- Customer mentions chargeback or disputing charge
- Customer mentions safety concern (sharp edges, broken lens near eyes)
- Customer asks for a manager or supervisor
- Customer uses profanity or expresses extreme anger
```

---

## Step 8: Set AI Agent Intent Classification

**Path:** AI Agent → Intents / Automation settings

### Full Self-Service (AI resolves, no ticket unless asked):
| Intent | AI Action |
|--------|-----------|
| Order status / tracking | Shopify lookup → show status |
| Product questions | KB article → answer |
| Size & fit inquiry | KB article → sizing guide |
| Tutorial / how-to | KB article → step-by-step |

### Guided Triage (AI collects info, creates enriched ticket):
| Intent | AI Action |
|--------|-----------|
| Broken frames | Collect order#, photos, cause, insurance → Warranty team |
| Prescription info | Answer from KB, route complex Qs to Rx team |
| Return eligibility | Check policy, collect order# → Returns team |
| Tech troubleshooting | Walk through reset/fix steps → Tech team if unresolved |
| Audio/connectivity | Troubleshooting tree → Tech team if unresolved |
| Discount inquiry | Share current promos (NEVER create codes) |

### Human-Gated (AI collects basics, creates priority ticket):
| Intent | AI Action | Priority |
|--------|-----------|----------|
| Order cancellation | Collect order# urgently → Order team | HIGH |
| Missing delivery | Collect order#, tracking → Order team | NORMAL |
| Wrong item received | Collect order#, photos → Order team | HIGH |
| Wholesale inquiry | Collect business details → Sales team | NORMAL |
| Lens defect | Collect order#, photos → Rx team | HIGH |

### Immediate Human (minimal AI, direct routing):
| Intent | AI Response |
|--------|-------------|
| Legal threats | "I understand your concern. Let me connect you with a team member right away." |
| Chargeback mention | Same — immediate routing |
| Safety concern | Same — immediate routing + flag as urgent |
| Manager request | "Let me connect you with a team member who can help." |

---

## Step 9: Test with 50 Real Customer Messages

After steps 1-8, test the AI Agent with these messages. Verify correct intent detection, flow routing, tags, and team assignment for each.

### Broken Frames (13 — reflects 25% volume):
1. "My frames broke"
2. "The hinge snapped on my glasses"
3. "The arm fell off"
4. "My frames cracked near the nose bridge"
5. "I sat on my glasses and they snapped"
6. "The frame broke after 2 months"
7. "One side is cracked"
8. "The temple broke when I adjusted them"
9. "The frame split at the joint"
10. "My glasses are broken, what can I do?"
11. "Are broken frames covered under warranty?"
12. "I need a replacement, my frames broke"
13. "The glasses snapped in half"

### Order Status (10):
14. "Where is my order?"
15. "Can I get a tracking number?"
16. "When will my order ship?"
17. "My order hasn't arrived"
18. "Tracking says in transit for 10 days"
19. "Has my order shipped?"
20. "I placed an order last week"
21. "When will I get my glasses?"
22. "What's the status of order #12345?"
23. "My tracking number doesn't work"

### Prescription (7):
24. "How do I upload my prescription?"
25. "What's my PD?"
26. "Can you fill a progressive?"
27. "How long will my Rx order take?"
28. "Do you offer blue light Rx lenses?"
29. "My prescription is -9.50, can you make it?"
30. "I need to update my prescription"

### Returns (5):
31. "I want to return my glasses"
32. "Can I exchange for a different size?"
33. "How do I get a refund?"
34. "Are prescription lenses refundable?"
35. "What's the return window?"

### Tech Support (5):
36. "My Bluetooth won't connect"
37. "Sound only from one side"
38. "My glasses keep disconnecting"
39. "How do I factory reset?"
40. "Touch controls not responding"

### Pre-Sale (4):
41. "Are these FSA/HSA eligible?"
42. "What size should I get?"
43. "How long does battery last?"
44. "Are they waterproof?"

### Other (6):
45. "Do you have any discounts?"
46. "I need to cancel my order"
47. "My order says delivered but I never got it"
48. "I want to talk to a manager"
49. "I'm interested in wholesale"
50. "What about your crypto token?"

### Expected Results:

| Messages | Expected Intent | Expected Team | Expected Tags |
|----------|----------------|---------------|---------------|
| 1-13 | broken_frames | Warranty & Returns | WARRANTY, broken-frame |
| 14-23 | order_status | Order Support | ORDER, wismo |
| 24-30 | prescription | Prescription Services | PRESCRIPTION |
| 31-35 | return_exchange | Warranty & Returns | RETURN |
| 36-40 | tech_support | Order Support | TECHNICAL |
| 41-44 | pre_sale | Sales & Product | PRE-SALE |
| 45 | discount_inquiry | Sales & Product | PRE-SALE, pricing |
| 46 | cancellation | Order Support (HIGH) | ORDER, cancel |
| 47 | missing_delivery | Order Support | ORDER, missing-item |
| 48 | escalation | Immediate human | escalated |
| 49 | wholesale | Sales & Product | PRE-SALE, wholesale |
| 50 | investor_token | Sales & Product | PRE-SALE |

---

## Step 10: Launch Checklist

### Week 1 (Foundation):
- [ ] All 10 new articles published
- [ ] All 4 existing articles updated
- [ ] Chat widget buttons reordered (broken frames = #1)
- [ ] Broken Frames Triage flow built
- [ ] Welcome flow updated
- [ ] AI Agent persona configured
- [ ] AI Agent guardrails set
- [ ] Intent classification configured

### Week 2 (Soft Launch):
- [ ] Enable AI Agent in **"suggest" mode** (AI suggests, agent confirms)
- [ ] Review 100% of AI-handled tickets daily
- [ ] Fix any misclassifications
- [ ] Run full 50-question test set
- [ ] Adjust flows based on test results

### Week 3-4 (Expand):
- [ ] Switch high-confidence modules to auto-response (Order Status, Pre-Sale)
- [ ] Enable remaining modules
- [ ] Sample 20% of AI-handled tickets weekly
- [ ] Monitor deflection rates

### Week 5+ (Optimize):
- [ ] Analyze deflection rates by module
- [ ] A/B test welcome messages
- [ ] Implement CSAT surveys
- [ ] Monthly content audit
- [ ] Feed broken frames data to product team

---

## Quick Access URLs

| Page | URL |
|------|-----|
| Dashboard | https://lucyd.gorgias.com/app/home |
| Help Center | https://lucyd.gorgias.com/app/settings/help-center |
| Flows | https://lucyd.gorgias.com/app/settings/flows |
| Macros | https://lucyd.gorgias.com/app/settings/macros |
| Rules | https://lucyd.gorgias.com/app/settings/rules |
| Chat Settings | https://lucyd.gorgias.com/app/settings/channels/gorgias_chat |
| AI Agent | https://lucyd.gorgias.com/app/ai-agent |
| Tags | https://lucyd.gorgias.com/app/settings/manage-tags |
| Teams | https://lucyd.gorgias.com/app/settings/teams |

---

## File Reference

| File | Contents |
|------|----------|
| `gorgias_macros.py` | Macro creation script (34 macros) |
| `gorgias_automation_rules.md` | Rule configurations (11 rules) |
| `gorgias_help_articles.md` | All 82 article contents |
| `gorgias_articles_paste_ready.md` | Copy-paste formatted articles (10 new + 4 updates) |
| `gorgias_flows_master.md` | All flow implementations (7 flows) |
| `gorgias_flows_plan.md` | Flow specifications and configs |
| `help_center_architecture.md` | Category structure and article inventory |
| `gorgias_tag_taxonomy.md` | Tag naming conventions |
| `gorgias_setup_guide.md` | This file |

---

*Document Version: 2.0*
*Last Updated: February 23, 2026*

# Gorgias Automation Rules for Lucyd

## Overview

This document defines the automation rules that should be configured in Gorgias to:
- Auto-tag tickets based on content
- Route tickets to appropriate teams
- Trigger auto-responses for common issues
- Escalate urgent tickets

---

## Rule 1: WISMO Auto-Response

**Purpose:** Automatically handle "Where Is My Order?" inquiries

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | WISMO Auto-Tagger |
| Status | Active |
| Trigger | Ticket created |

**Conditions (ANY):**
```
Body contains: "where is my order"
Body contains: "track my order"
Body contains: "order status"
Body contains: "when will my order"
Body contains: "shipping status"
Body contains: "tracking number"
Body contains: "has my order shipped"
```

**Actions:**
1. Add tags: `ORDER`, `wismo`
2. Set status: Open
3. Apply macro: `ORDER-WISMO-Auto` (if available)
4. Assign to: Order Support team

**Auto-Response (Optional):**
```
Hi {{ticket.customer.firstname | default: 'there'}},

Thanks for reaching out! I can help you track your order.

To look up your order status, I'll need:
- Your order number (starts with "LU" or "#"), OR
- The email address used for the order

In the meantime, you can track your order at: https://lucyd.co/apps/tracking

If your order included prescription lenses, please note they take 10-15 business days to process before shipping.

We'll get back to you shortly!
```

---

## Rule 2: Bluetooth Auto-Help

**Purpose:** Provide immediate troubleshooting for Bluetooth issues

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | Bluetooth Troubleshooting |
| Status | Active |
| Trigger | Ticket created |

**Conditions (ANY):**
```
Body contains: "bluetooth"
Body contains: "pairing"
Body contains: "won't connect"
Body contains: "can't connect"
Body contains: "not connecting"
Body contains: "disconnect"
Body contains: "connection problem"
```

**Actions:**
1. Add tags: `TECHNICAL`, `bluetooth`
2. Set status: Open
3. Send Help Center article: "Bluetooth Pairing Troubleshooting Guide"
4. Assign to: Order Support team

**Auto-Response:**
```
Hi {{ticket.customer.firstname | default: 'there'}},

I see you're having Bluetooth connection issues. Let's get your Lucyd glasses connected!

Try these steps:
1. Make sure Bluetooth is ON on your phone
2. Hold the glasses button for 5 seconds until you hear "pairing mode"
3. Select "Lucyd" in your phone's Bluetooth settings

If that doesn't work:
- Go to Bluetooth settings and "Forget" Lucyd
- Factory reset: Hold BOTH buttons for 10 seconds
- Try pairing again

For detailed steps: [Link to Help Center Article]

Let us know if you need more help!
```

---

## Rule 3: Prescription Upload Help

**Purpose:** Assist with prescription upload issues

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | Rx Upload Assistance |
| Status | Active |
| Trigger | Ticket created |

**Conditions (ANY):**
```
Body contains: "can't upload"
Body contains: "upload failed"
Body contains: "prescription error"
Body contains: "won't let me upload"
Body contains: "upload my prescription"
Body contains: "submit prescription"
```

**Actions:**
1. Add tags: `PRESCRIPTION`, `upload-issue`
2. Set status: Open
3. Apply macro: `RX-Upload-Help`
4. Assign to: Prescription Services team

**Auto-Response:**
```
Hi {{ticket.customer.firstname | default: 'there'}},

I'm sorry you're having trouble uploading your prescription!

Quick fixes to try:
- Accepted formats: JPG, PNG, PDF (under 5MB)
- Make sure the image is clear and all text is readable
- Try a different browser or clear your cache
- If on mobile, try desktop or vice versa

Can't get it to work? No problem! You can:
- Reply to this email with your prescription attached
- Email it to info@lucyd.co with your order number

We'll process it manually for you!
```

---

## Rule 4: Urgent Escalation

**Purpose:** Flag and escalate tickets with angry or legally concerning language

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | Urgent Escalation |
| Status | Active |
| Trigger | Ticket created OR updated |

**Conditions (ANY):**
```
Body contains: "lawyer"
Body contains: "attorney"
Body contains: "BBB"
Body contains: "Better Business Bureau"
Body contains: "chargeback"
Body contains: "dispute"
Body contains: "sue"
Body contains: "legal action"
Body contains: "fraud"
Body contains: "scam"
Sentiment: Angry (if sentiment analysis enabled)
```

**Actions:**
1. Add tags: `escalated`, `urgent`, `legal-risk`
2. Set priority: Urgent
3. Assign to: Manager/Lead queue
4. Send internal notification to team lead

**Internal Note (Auto-Added):**
```
[URGENT ESCALATION]
This ticket contains language indicating potential legal concerns or extreme dissatisfaction.
Please prioritize and handle with care.
Keywords detected: [matched keywords]
```

---

## Rule 5: Return Request Tagger

**Purpose:** Identify and route return requests

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | Return Request Tagger |
| Status | Active |
| Trigger | Ticket created |

**Conditions (ANY):**
```
Body contains: "return"
Body contains: "refund"
Body contains: "send back"
Body contains: "money back"
Body contains: "exchange"
Body contains: "doesn't fit"
Body contains: "wrong size"
```

**Actions:**
1. Add tags: `RETURN`
2. If body contains "refund" or "money back": Add tag `refund-status`
3. If body contains "exchange": Add tag `exchange`
4. Assign to: Warranty & Returns team

---

## Rule 6: Warranty Claim Identifier

**Purpose:** Route warranty-related tickets

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | Warranty Claim Router |
| Status | Active |
| Trigger | Ticket created |

**Conditions (ANY):**
```
Body contains: "warranty"
Body contains: "defect"
Body contains: "broken"
Body contains: "stopped working"
Body contains: "manufacturing"
Body contains: "faulty"
```

**Actions:**
1. Add tags: `WARRANTY`
2. If body contains "defect" or "faulty": Add tag `defect`
3. If body contains "claim": Add tag `claim`
4. Assign to: Warranty & Returns team

---

## Rule 7: Social Media Lead Capture

**Purpose:** Tag and prioritize potential sales from social media

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | Social Lead Capture |
| Status | Active |
| Trigger | Ticket created |

**Conditions:**
```
Channel: Instagram OR Facebook
Body contains: "where can I buy"
Body contains: "how much"
Body contains: "price"
Body contains: "want to order"
Body contains: "interested in"
```

**Actions:**
1. Add tags: `PRE-SALE`, `social-lead`
2. Assign to: Social & Chat team
3. Set priority: High (sales opportunity)

---

## Rule 8: After-Hours Auto-Response

**Purpose:** Set expectations when tickets arrive outside business hours

**Configuration:**

| Setting | Value |
|---------|-------|
| Rule Name | After Hours Response |
| Status | Active |
| Trigger | Ticket created |

**Conditions:**
```
Time: Outside business hours (M-F 9am-5pm EST)
```

**Actions:**
1. Send auto-response (below)
2. Do NOT change status (keeps as new)

**Auto-Response:**
```
Hi {{ticket.customer.firstname | default: 'there'}},

Thanks for reaching out to Lucyd! We received your message.

Our support team is available Monday-Friday, 9am-5pm EST. We'll get back to you on the next business day.

In the meantime, you might find answers in our Help Center:
https://lucyd.gorgias.com/help-center

Common topics:
- Track your order: [link]
- Bluetooth troubleshooting: [link]
- Return policy: [link]

Talk soon!
```

---

## Rule Priority Order

Rules are evaluated in this order (first match wins for conflicting actions):

1. **Urgent Escalation** (highest priority - safety net)
2. **WISMO Auto-Response**
3. **Bluetooth Auto-Help**
4. **Prescription Upload Help**
5. **Return Request Tagger**
6. **Warranty Claim Identifier**
7. **Social Media Lead Capture**
8. **After-Hours Auto-Response** (lowest priority)

---

## Implementation Checklist

- [ ] Create Rule 1: WISMO Auto-Response
- [ ] Create Rule 2: Bluetooth Auto-Help
- [ ] Create Rule 3: Prescription Upload Help
- [ ] Create Rule 4: Urgent Escalation
- [ ] Create Rule 5: Return Request Tagger
- [ ] Create Rule 6: Warranty Claim Identifier
- [ ] Create Rule 7: Social Media Lead Capture
- [ ] Create Rule 8: After-Hours Auto-Response
- [ ] Test each rule with sample tickets
- [ ] Monitor for false positives/negatives

---

## Testing Rules

### Test Scenarios

| Scenario | Expected Tags | Expected Team |
|----------|---------------|---------------|
| "Where is my order #LU12345?" | `ORDER`, `wismo` | Order Support |
| "My glasses won't connect to bluetooth" | `TECHNICAL`, `bluetooth` | Order Support |
| "I can't upload my prescription" | `PRESCRIPTION`, `upload-issue` | Prescription Services |
| "I want to return my glasses" | `RETURN` | Warranty & Returns |
| "The speaker is broken, is this under warranty?" | `WARRANTY`, `defect` | Warranty & Returns |
| "I'm contacting my lawyer about this" | `escalated`, `urgent`, `legal-risk` | Manager |

---

## Gorgias Settings Location

To create/edit rules:
1. Go to: https://lucyd.gorgias.com/app/settings/rules
2. Click "Create Rule"
3. Configure trigger, conditions, and actions
4. Test with "Run Test" feature
5. Enable rule

---

*Document Version: 1.0*
*Last Updated: January 2026*

# Gorgias Tag Taxonomy for Lucyd

## Overview

This document defines the complete tag structure for organizing and routing tickets in Gorgias.

---

## Primary Tags (Required - One Per Ticket)

These are the main category tags. Every ticket should have exactly one primary tag.

| Tag | Category | Color | Description |
|-----|----------|-------|-------------|
| `ORDER` | Orders & Shipping | Blue | Order status, tracking, delivery issues |
| `TECHNICAL` | Technical Support | Orange | Bluetooth, audio, charging, connectivity |
| `PRESCRIPTION` | Prescription Lenses | Purple | Rx orders, PD, lens processing |
| `RETURN` | Returns & Exchanges | Red | Return requests, refunds, exchanges |
| `WARRANTY` | Warranty & Protection | Green | Coverage questions, claims, insurance |
| `PRE-SALE` | Pre-purchase Questions | Yellow | Product questions before buying |

---

## Secondary Tags (Specificity)

Secondary tags provide more detail about the specific issue. Use in combination with primary tags.

### ORDER Secondary Tags

| Tag | Use When | Auto-Apply Keywords |
|-----|----------|---------------------|
| `wismo` | Customer asking where their order is | "where is", "track", "when will" |
| `tracking` | Tracking number or link requests | "tracking number", "tracking link" |
| `delay` | Order delayed beyond expected time | "late", "delayed", "still waiting" |
| `damaged` | Product arrived damaged | "damaged", "broken", "crushed" |
| `cancel` | Customer wants to cancel order | "cancel", "don't want", "stop order" |
| `international` | International shipping questions | "international", "outside US", country names |
| `address-change` | Shipping address modification | "change address", "wrong address" |

### TECHNICAL Secondary Tags

| Tag | Use When | Auto-Apply Keywords |
|-----|----------|---------------------|
| `bluetooth` | Pairing or connection issues | "bluetooth", "pairing", "connect" |
| `audio-quality` | Sound quality problems | "tinny", "quiet", "bass", "crackling" |
| `one-side` | Audio on one side only | "one side", "left speaker", "right speaker" |
| `battery` | Battery life concerns | "battery", "dies fast", "won't hold charge" |
| `charging` | Charging problems | "won't charge", "charging cable", "LED" |
| `app-issue` | Lucyd app problems | "app", "firmware", "update" |
| `reset` | Factory reset needed/performed | "reset", "restart" |

### PRESCRIPTION Secondary Tags

| Tag | Use When | Auto-Apply Keywords |
|-----|----------|---------------------|
| `upload-issue` | Can't upload prescription | "can't upload", "upload failed", "error" |
| `pd-missing` | PD measurement needed | "PD", "pupillary distance" |
| `processing-time` | Questions about Rx processing | "how long", "when ready", "processing" |
| `lens-fit` | Lenses don't fit correctly | "loose", "tight", "don't fit" |
| `vision-issue` | Vision problems with lenses | "blurry", "headache", "can't see" |
| `remake-review` | Potential lens remake needed | "wrong prescription", "remake" |

### RETURN Secondary Tags

| Tag | Use When | Auto-Apply Keywords |
|-----|----------|---------------------|
| `eligibility` | Asking if item can be returned | "can I return", "eligible", "returnable" |
| `refund-status` | Checking on refund progress | "where's my refund", "refund status" |
| `exchange` | Wants to exchange for different item | "exchange", "swap", "different size" |
| `restocking-fee` | Questions about $15 fee | "restocking", "fee", "$15" |
| `rx-return` | Trying to return Rx lenses | "return prescription", "refund lenses" |

### WARRANTY Secondary Tags

| Tag | Use When | Auto-Apply Keywords |
|-----|----------|---------------------|
| `claim` | Filing a warranty claim | "warranty claim", "file claim" |
| `coverage-question` | Asking what's covered | "covered", "warranty include" |
| `insurance` | Lucyd Pro insurance questions | "insurance", "Lucyd Pro", "2 year" |
| `defect` | Manufacturing defect reported | "defect", "manufacturing", "faulty" |
| `out-of-warranty` | Product past warranty period | "expired", "out of warranty", "over a year" |

### PRE-SALE Secondary Tags

| Tag | Use When | Auto-Apply Keywords |
|-----|----------|---------------------|
| `sizing` | Frame size questions | "size", "fit", "face width" |
| `compatibility` | Phone/device compatibility | "work with", "compatible", "iPhone", "Android" |
| `features` | Product feature questions | "can it", "does it", "feature" |
| `fsa-hsa` | FSA/HSA payment questions | "FSA", "HSA", "insurance", "eligible" |
| `pricing` | Price or discount questions | "price", "cost", "discount", "coupon" |

---

## Resolution Tags

Apply one of these when closing a ticket.

| Tag | When to Apply |
|-----|---------------|
| `resolved-self-service` | Customer resolved via Help Center/flow without agent |
| `resolved-agent` | Agent resolved the issue |
| `resolved-auto` | Automation resolved (order lookup, etc.) |
| `escalated` | Required manager or special handling |
| `no-response` | Customer didn't respond to follow-up |

---

## Priority Tags

| Tag | When to Apply | SLA Impact |
|-----|---------------|------------|
| `urgent` | Angry customer, time-sensitive | Response within 1 hour |
| `vip` | High-value or repeat customer | Prioritized handling |
| `legal-risk` | Mentions lawyer, BBB, chargeback | Immediate escalation |

---

## Channel Tags (Auto-Applied)

| Tag | Applied When |
|-----|--------------|
| `email` | Ticket from email |
| `chat` | Ticket from chat widget |
| `instagram` | Ticket from Instagram DM |
| `facebook` | Ticket from Facebook |
| `contact-form` | Ticket from website form |

---

## Social Media Tags

| Tag | Use When |
|-----|----------|
| `social-lead` | Sales opportunity from social |
| `social-question` | Product question on social |
| `influencer` | Influencer or collab inquiry |
| `negative` | Negative sentiment/complaint |

---

## Tag Naming Conventions

1. **Lowercase with hyphens**: `upload-issue` not `Upload_Issue`
2. **Primary tags UPPERCASE**: `ORDER`, `TECHNICAL`, etc.
3. **Be specific**: `bluetooth` not `tech-issue`
4. **Max 3 tags per ticket**: 1 primary + 2 secondary max
5. **Don't duplicate**: If using `WARRANTY` + `defect`, don't also add `TECHNICAL`

---

## Team Assignment by Tag

| Primary Tag | Assign To |
|-------------|-----------|
| `ORDER` | Order Support |
| `TECHNICAL` | Order Support |
| `PRESCRIPTION` | Prescription Services |
| `RETURN` | Warranty & Returns |
| `WARRANTY` | Warranty & Returns |
| `PRE-SALE` | Sales & Product |

---

## Auto-Tagging Rules Summary

See `gorgias_automation_rules.md` for full rule configurations.

| Rule | Trigger Keywords | Tags Applied |
|------|------------------|--------------|
| WISMO Detection | "where is my order", "track" | `ORDER`, `wismo` |
| Bluetooth Issues | "bluetooth", "pairing", "connect" | `TECHNICAL`, `bluetooth` |
| Rx Upload Help | "can't upload", "prescription" | `PRESCRIPTION`, `upload-issue` |
| Refund Check | "refund", "money back" | `RETURN`, `refund-status` |
| Escalation | "lawyer", "BBB", "chargeback" | `urgent`, `legal-risk` |

---

*Document Version: 1.0*
*Last Updated: January 2026*

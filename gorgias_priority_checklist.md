# Gorgias Implementation Priority Checklist

## Priority Framework
- **Impact**: Based on ticket volume and deflection potential
- **Effort**: Time to build in Gorgias UI
- **ROI**: Impact ÷ Effort

---

## Phase 1: Quick Wins (Do First - 1 Hour Total)

### Flows (High Impact, Low Effort)

| Priority | Flow | Build Time | Expected Deflection | Why First |
|----------|------|------------|---------------------|-----------|
| 🥇 1 | **Order Tracking** | 10 min | 40-50% | #1 ticket driver, simple flow |
| 🥈 2 | **Returns Policy** | 10 min | 20-30% | High volume, simple info |

### Help Center Articles (Copy-Paste Ready)

| Priority | Article | Category | Why First |
|----------|---------|----------|-----------|
| 1 | Track My Order | Orders | Links from Order Tracking flow |
| 2 | Return Policy | Returns | Answers 80% of return questions |
| 3 | Shipping Times | Orders | Common pre-sale question |
| 4 | Bluetooth Pairing Guide | Getting Started | #1 tech support topic |
| 5 | Factory Reset Guide | Troubleshooting | Solves 70% of tech issues |

**Phase 1 Total: ~1 hour → Deflects 30% of tickets**

---

## Phase 2: Core Support (Day 1 - 2 Hours)

### Flows

| Priority | Flow | Build Time | Expected Deflection | Why |
|----------|------|------------|---------------------|-----|
| 🥉 3 | **Technical Support** | 20 min | 30-40% | High volume, saves agent time |
| 4 | **Prescription Help** | 20 min | 25-35% | Complex tickets, good deflection |

### Help Center Articles

| Priority | Article | Category | Why |
|----------|---------|----------|-----|
| 6 | How to Submit Prescription | Prescriptions | Required for Rx flow |
| 7 | PD Measurement Guide | Prescriptions | Common question |
| 8 | Charging Problems | Troubleshooting | Frequent tech issue |
| 9 | No Audio / Sound Issues | Troubleshooting | Frequent tech issue |
| 10 | Warranty Coverage | Warranty | Reduces claim confusion |

**Phase 2 Total: ~2 hours → Deflects additional 20% of tickets**

---

## Phase 3: Complete Coverage (Day 2 - 2 Hours)

### Flows

| Priority | Flow | Build Time | Why |
|----------|------|------------|-----|
| 5 | **Returns & Exchanges** | 15 min | Complete return self-service |
| 6 | **Contact Form Pre-Qual** | 20 min | Smart routing, better data |

### Help Center Articles

| Priority | Article | Category | Why |
|----------|---------|----------|-----|
| 11 | First-Time Setup Guide | Getting Started | New customer onboarding |
| 12 | Rx Processing Time | Prescriptions | Reduces "where's my order" |
| 13 | How to Start a Return | Returns | Enables self-service |
| 14 | How to File Warranty Claim | Warranty | Complete warranty flow |
| 15 | FSA/HSA Eligibility | Product Info | Common pre-sale question |

**Phase 3 Total: ~2 hours → Deflects additional 10% of tickets**

---

## Phase 4: Full Help Center (Day 3+ - 2 Hours)

### Remaining Articles by Category

**Getting Started (2 remaining)**
- [ ] Lucyd App Setup
- [ ] Touch Controls Guide

**Troubleshooting (3 remaining)**
- [ ] Bluetooth Won't Connect
- [ ] One Speaker Not Working
- [ ] App Issues

**Orders & Shipping (3 remaining)**
- [ ] International Shipping
- [ ] Change or Cancel Order
- [ ] Order Not Received

**Prescriptions (2 remaining)**
- [ ] Prescription Requirements
- [ ] Vision Problems with New Glasses

**Returns (2 remaining)**
- [ ] How to Start an Exchange
- [ ] Refund Timeline

**Warranty (1 remaining)**
- [ ] Out of Warranty Options

**Product Info (4 remaining)**
- [ ] Frame Sizing Guide
- [ ] Phone Compatibility
- [ ] Battery & Charging Specs
- [ ] Water Resistance

---

## Implementation Checklist

### Before Starting
- [ ] Open `gorgias_flows_master.md` in one tab
- [ ] Open `gorgias_help_articles.md` in another tab
- [ ] Open Gorgias dashboard

### Phase 1 Checklist (1 Hour)
- [ ] Create Order Tracking flow
- [ ] Create Returns Policy info flow
- [ ] Add article: Track My Order
- [ ] Add article: Return Policy
- [ ] Add article: Shipping Times
- [ ] Add article: Bluetooth Pairing Guide
- [ ] Add article: Factory Reset Guide
- [ ] **TEST**: Send test messages to trigger flows

### Phase 2 Checklist (2 Hours)
- [ ] Create Technical Support flow
- [ ] Create Prescription Help flow
- [ ] Add article: How to Submit Prescription
- [ ] Add article: PD Measurement Guide
- [ ] Add article: Charging Problems
- [ ] Add article: No Audio / Sound Issues
- [ ] Add article: Warranty Coverage
- [ ] **TEST**: Verify all branches work

### Phase 3 Checklist (2 Hours)
- [ ] Create Returns & Exchanges flow
- [ ] Create Contact Form Pre-Qualification
- [ ] Add articles 11-15
- [ ] **TEST**: Full end-to-end testing

### Phase 4 Checklist (2 Hours)
- [ ] Add remaining 17 articles
- [ ] Organize Help Center categories
- [ ] Enable search functionality
- [ ] Add feedback buttons to articles

---

## Quick Copy Commands

Open the content files for easy copy-paste:

```bash
# Open flows reference
open /Users/ecohen/Documents/GitHub/Lucyd/gorgias_flows_master.md

# Open articles content
open /Users/ecohen/Documents/GitHub/Lucyd/gorgias_help_articles.md
```

---

## Success Metrics (Check After 1 Week)

| Metric | Target | How to Check |
|--------|--------|--------------|
| Self-service rate | 30%+ | Gorgias Analytics → Automation |
| Flow completion | 70%+ | Flows → Analytics |
| Ticket volume | -20% | Compare to previous week |
| First response time | <5 min | Includes auto-responses |

---

## Gorgias Quick Links

- **Flows**: https://lucyd.gorgias.com/app/automate/flows
- **Help Center**: https://lucyd.gorgias.com/app/help-center
- **Rules** (verify enabled): https://lucyd.gorgias.com/app/settings/rules
- **Macros** (already created): https://lucyd.gorgias.com/app/settings/macros
- **Analytics**: https://lucyd.gorgias.com/app/statistics

---

*Total implementation time: ~7 hours for complete setup*
*Minimum viable setup (Phase 1): ~1 hour*

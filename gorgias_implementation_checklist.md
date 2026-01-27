# Gorgias Implementation Checklist
## 12-Week Rollout Plan

---

## Phase 1: MVP (Weeks 1-4)

### Week 1: Foundation

**Day 1-2: Setup & Configuration**
- [ ] Set up Gorgias Help Center (enable feature)
- [ ] Configure Shopify integration (order lookup)
- [ ] Set up team structure:
  - [ ] Order Support team
  - [ ] Prescription Services team
  - [ ] Warranty & Returns team
  - [ ] Sales & Product team
  - [ ] Social & Chat team

**Day 3-4: Tag & Rule Setup**
- [ ] Create tag taxonomy (see `gorgias_tag_taxonomy.md`)
  - [ ] Primary tags: ORDER, TECHNICAL, PRESCRIPTION, RETURN, WARRANTY, PRE-SALE
  - [ ] Secondary tags (by category)
  - [ ] Resolution tags
- [ ] Configure automation rules (see `gorgias_automation_rules.md`)
  - [ ] Rule 1: WISMO Auto-Response
  - [ ] Rule 2: Bluetooth Auto-Help
  - [ ] Rule 3: Prescription Upload Help
  - [ ] Rule 4: Urgent Escalation

**Day 5: Intercom Data Analysis**
- [ ] Export Intercom conversation transcripts (12 months)
- [ ] Export Intercom tags/categories
- [ ] Export saved replies/canned responses
- [ ] Analyze top ticket drivers by volume
- [ ] Identify deflection opportunities

---

### Week 2: Core Content (15 MVP Articles)

**Priority 1 Articles (Must Have)**
- [ ] How to track my order
- [ ] What does "preparing order" status mean?
- [ ] Bluetooth pairing troubleshooting guide
- [ ] How to pair with iPhone
- [ ] How to pair with Android
- [ ] How to factory reset your glasses
- [ ] What is Lucyd's return policy?
- [ ] How to start a return
- [ ] How to measure your PD at home
- [ ] How to upload my prescription

**Priority 2 Articles (High Value)**
- [ ] What does 1-year warranty cover?
- [ ] How to file a warranty claim
- [ ] How long do Rx orders take?
- [ ] No audio / sound issues troubleshooting
- [ ] Charging problems troubleshooting

---

### Week 3: Automation

**Macros (Verify/Create)**
- [ ] ORDER-WISMO-Shipped
- [ ] ORDER-WISMO-Processing
- [ ] ORDER-Delay-Apology
- [ ] RX-Upload-Help
- [ ] RX-PD-Missing
- [ ] RX-Processing-Time
- [ ] TECH-Bluetooth-Troubleshooting
- [ ] TECH-Audio-Quality
- [ ] TECH-Factory-Reset
- [ ] RETURN-Start-Return
- [ ] RETURN-Rx-Not-Returnable
- [ ] RETURN-Refund-Status
- [ ] WARRANTY-Coverage-Explanation
- [ ] WARRANTY-Defect-Claim

**Chat Flows**
- [ ] Flow 1: Order Tracking (WISMO)
- [ ] Flow 2: Technical Support (Basic)
- [ ] Quick Response Buttons:
  - [ ] Track My Order
  - [ ] Technical Support
  - [ ] Returns & Refunds
  - [ ] Prescription Help

**Testing**
- [ ] Test each automation rule with sample tickets
- [ ] Test order lookup via Shopify integration
- [ ] Test chat flows end-to-end
- [ ] Verify tag application is correct
- [ ] Verify team assignment is correct

---

### Week 4: Launch

**Pre-Launch**
- [ ] Final content review
- [ ] Publish Help Center
- [ ] Enable chat widget on lucyd.co
- [ ] Configure business hours
- [ ] Set up offline message collection

**Training**
- [ ] Train support team on new macros
- [ ] Train support team on tag usage
- [ ] Document escalation procedures
- [ ] Share Help Center URLs internally

**Go-Live**
- [ ] Enable all automation rules
- [ ] Monitor first 24 hours closely
- [ ] Address any issues immediately
- [ ] Collect team feedback

**Week 4 Success Metrics**
| Metric | Target |
|--------|--------|
| Help Center views | 500+/week |
| Self-service rate | 20%+ |
| WISMO reduction | 30%+ |
| Team satisfaction | Positive |

---

## Phase 2: Expansion (Weeks 5-8)

### Week 5-6: Additional Content (15+ Articles)

**Technical Support Expansion**
- [ ] Audio sounds tinny or lacks bass
- [ ] One side has no audio
- [ ] Volume too low at max
- [ ] Microphone not working on calls
- [ ] Battery draining too quickly
- [ ] My glasses won't charge

**Returns & Warranty Expansion**
- [ ] What items cannot be returned?
- [ ] When will I receive my refund?
- [ ] What is NOT covered under warranty?
- [ ] Out of warranty options

**Product Information**
- [ ] Frame styles and sizing guide
- [ ] What devices work with Lucyd?
- [ ] Can Lucyd glasses get wet?
- [ ] FSA/HSA eligibility

**Prescription Expansion**
- [ ] What prescription info do I need?
- [ ] Prescription range and limitations
- [ ] Vision problems with new glasses

---

### Week 7-8: Automation Enhancements

**New Rules**
- [ ] Rule 5: Return Request Tagger
- [ ] Rule 6: Warranty Claim Identifier
- [ ] Rule 7: Social Media Lead Capture
- [ ] Rule 8: After-Hours Auto-Response

**Advanced Flows**
- [ ] Flow 3: Prescription Help (expanded)
- [ ] Flow 4: Returns & Exchanges (expanded)
- [ ] Contact Form Pre-Qualification

**Proactive Chat Triggers**
- [ ] Trigger on cart abandonment
- [ ] Trigger on checkout hesitation
- [ ] Trigger on Help Center dead-end

**Phase 2 Success Metrics**
| Metric | Target |
|--------|--------|
| Self-service rate | 30-35% |
| Ticket reduction | 25%+ |
| CSAT | 4.0+ |
| Flow completion rate | 70%+ |

---

## Phase 3: Optimization (Weeks 9-12)

### Week 9-10: Analysis & Gaps

**Search Query Analysis**
- [ ] Review Help Center search queries
- [ ] Identify articles with high "not helpful" rates
- [ ] Identify missing content based on searches
- [ ] Create new articles for gaps

**A/B Testing**
- [ ] Test different article titles
- [ ] Test different flow welcome messages
- [ ] Test button labels on chat widget

**Content Improvements**
- [ ] Add video to top 10 articles
- [ ] Add step-by-step screenshots
- [ ] Create product-specific guides
- [ ] Update outdated content

---

### Week 11-12: Final Polish

**Advanced Features**
- [ ] Implement NPS surveys post-resolution
- [ ] Set up satisfaction tracking
- [ ] Configure advanced reporting
- [ ] Create management dashboard

**Documentation**
- [ ] Update all SOPs
- [ ] Create agent training guide
- [ ] Document all flows and rules
- [ ] Archive Intercom data

**Phase 3 Success Metrics**
| Metric | Target |
|--------|--------|
| Self-service rate | 40-50% |
| Ticket reduction | 40%+ |
| First contact resolution | 75%+ |
| Help Center satisfaction | 80%+ |

---

## Verification & Testing

### Pre-Launch Testing Checklist
- [ ] Test all Quick Response flows end-to-end
- [ ] Verify Shopify order data pulls correctly
- [ ] Test each automation rule with sample tickets
- [ ] Verify Help Center search returns relevant results
- [ ] Test on mobile devices
- [ ] Test on different browsers

### Post-Launch Monitoring
- [ ] Daily: Check automation success rate
- [ ] Daily: Review untagged tickets
- [ ] Weekly: Review Help Center analytics
- [ ] Weekly: Audit tickets tagged "needs-article"
- [ ] Monthly: Full content audit
- [ ] Monthly: Team feedback session

---

## Quick Links

| Resource | URL |
|----------|-----|
| Dashboard | https://lucyd.gorgias.com |
| Flows | https://lucyd.gorgias.com/app/automate/flows |
| Rules | https://lucyd.gorgias.com/app/settings/rules |
| Macros | https://lucyd.gorgias.com/app/settings/macros |
| Help Center | https://lucyd.gorgias.com/app/help-center |
| Analytics | https://lucyd.gorgias.com/app/statistics |

---

## File Reference

| File | Contents |
|------|----------|
| `help_center_architecture.md` | Master architecture document |
| `gorgias_tag_taxonomy.md` | Tag structure and naming |
| `gorgias_automation_rules.md` | Rule configurations |
| `gorgias_macros.py` | Macro creation script |
| `gorgias_help_articles.md` | Full article content |
| `gorgias_flows_master.md` | Flow specifications |

---

*Last Updated: January 2026*

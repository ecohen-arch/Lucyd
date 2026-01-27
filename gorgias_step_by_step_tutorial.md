# Gorgias Flows Step-by-Step Tutorial

## Getting Started

**Your Flows URL:** https://lucyd.gorgias.com/app/settings/flows/shopify/lucyd-dev

---

## Flow 1: Order Tracking (10 minutes)

### Step 1: Create New Flow
1. Click **"Create Flow"** or **"+ New"** button
2. Name it: `Order Tracking Self-Service`

### Step 2: Set Trigger
1. Select trigger type: **"Chat message received"** or **"Customer sends message"**
2. Add condition: **Message contains any of:**
   ```
   track, tracking, order, shipping, where is, delivery, shipped, package
   ```

### Step 3: Add First Message
1. Click **"+ Add step"** → Select **"Send message"**
2. Paste this message:
   ```
   I can help you track your order! 📦

   Please reply with your order number (starts with #) or the email address you used when ordering.
   ```

### Step 4: Wait for Customer Reply
1. Click **"+ Add step"** → Select **"Wait for reply"**
2. Save response as variable: `customer_input`

### Step 5: Add Shopify Order Lookup
1. Click **"+ Add step"** → Select **"Shopify lookup"** or **"Find order"**
2. Search by: Order number OR Customer email
3. Use variable: `{{customer_input}}`

### Step 6: Add Condition Branch
1. Click **"+ Add step"** → Select **"Condition"** or **"If/Then"**
2. Condition: **If order found**

### Step 7: Add "Order Found - Shipped" Response
1. Under the **"Yes/True"** branch, click **"+ Add step"** → **"Send message"**
2. Add another condition: **If fulfillment_status = fulfilled**
3. Paste this message:
   ```
   Great news! Your order has shipped! 🚚

   Order: {{order.name}}
   Status: Shipped on {{order.fulfilled_at}}
   Tracking: {{order.tracking_url}}

   Click the tracking link above for real-time updates.
   ```
4. Add **Quick Reply buttons:**
   - "Track Package" → Link to tracking
   - "Something Else" → Restart flow
   - "Talk to Agent" → Handoff

### Step 8: Add "Order Found - Processing" Response
1. Add another branch for: **If fulfillment_status = null/unfulfilled**
2. Paste this message:
   ```
   Your order is being prepared! ⏳

   Order: {{order.name}}
   Status: Processing

   Expected timelines:
   • Non-prescription: Ships in 1-3 business days
   • Prescription orders: 10-15 business days total

   We'll email you tracking info as soon as it ships!
   ```
3. Add **Quick Reply buttons:**
   - "OK, Thanks!" → End flow
   - "I Need It Faster" → Handoff to agent
   - "Talk to Agent" → Handoff

### Step 9: Add "Order Not Found" Response
1. Under the **"No/False"** branch (order not found), add message:
   ```
   I couldn't find an order matching that information. 🔍

   Please double-check:
   • Order number (check confirmation email)
   • Email address used at checkout

   Want to try again or speak with our team?
   ```
2. Add **Quick Reply buttons:**
   - "Try Again" → Go back to Step 3
   - "Talk to Agent" → Handoff

### Step 10: Add Agent Handoff
1. For "Talk to Agent" buttons, add step: **"Handoff to agent"** or **"Create ticket"**
2. Set:
   - Subject: `Order Tracking Help`
   - Tags: `ORDER-STATUS`, `chat-escalation`
   - Assign to: Order Support team

### Step 11: Save & Publish
1. Click **"Save"**
2. Click **"Publish"** or toggle **"Active"**
3. **Test it:** Open chat widget and type "where is my order"

---

## Flow 2: Technical Support (20 minutes)

### Step 1: Create New Flow
1. Click **"Create Flow"**
2. Name it: `Technical Support Self-Service`

### Step 2: Set Trigger
1. Trigger: **Chat message received**
2. Message contains any of:
   ```
   bluetooth, pairing, connect, audio, sound, speaker, charging, charge, battery, app, reset, not working, broken, help, issue
   ```

### Step 3: Add Issue Selection Message
1. Add **"Send message"** with **Quick Replies:**
   ```
   I'm here to help with your Lucyd glasses! 🔧

   What issue are you experiencing?
   ```
2. Add Quick Reply buttons:
   - 📱 Bluetooth/Pairing
   - 🔊 Audio Problems
   - 🔋 Charging Issues
   - 📲 App Setup
   - 🔄 Factory Reset
   - 💬 Other Issue

### Step 4: Create Bluetooth Branch
1. When customer clicks "Bluetooth/Pairing", send:
   ```
   Let's get your glasses connected! 📱

   Try these steps:

   1️⃣ Make sure Bluetooth is ON on your phone

   2️⃣ On your glasses, press and hold the button for 5 seconds until you hear "pairing mode"

   3️⃣ On your phone, go to Settings → Bluetooth and look for "Lucyd"

   4️⃣ Tap "Lucyd" to connect - you should hear "connected"

   Did that work?
   ```
2. Add Quick Replies:
   - "✅ Yes, connected!" → Success message → End
   - "❌ Still not working" → Advanced steps

### Step 5: Add Advanced Bluetooth Steps
1. For "Still not working", send:
   ```
   Let's try a few more things:

   1️⃣ On your phone, "Forget" or remove "Lucyd" from Bluetooth settings

   2️⃣ Restart your phone

   3️⃣ Make sure your glasses have at least 20% battery

   4️⃣ Try pairing mode again (hold button 5 seconds)

   Still having trouble?
   ```
2. Add Quick Replies:
   - "✅ Working now!" → Success → End
   - "❌ Still won't connect" → Factory reset or Agent

### Step 6: Create Audio Branch
1. When customer clicks "Audio Problems", send:
   ```
   Sorry about the audio issue! 🔊

   Is the sound missing from one side or both sides?
   ```
2. Add Quick Replies:
   - "One Side Only"
   - "Both Sides"
   - "Sound is Distorted"

### Step 7: Add One-Side Audio Response
1. For "One Side Only", send:
   ```
   Audio on one side may indicate a hardware issue.

   First, let's try a factory reset:
   Hold BOTH temple buttons for 10 seconds until you hear a tone.

   Then reconnect to your phone and test.

   Did the reset fix it?
   ```
2. Add Quick Replies:
   - "✅ Both sides working!" → Success → End
   - "❌ Still one side" → Warranty handoff

### Step 8: Add Both-Sides Audio Response
1. For "Both Sides", send:
   ```
   Let's troubleshoot:

   1️⃣ Check your phone's media volume (not just ringer)

   2️⃣ Tap the RIGHT temple to increase glasses volume

   3️⃣ Make sure audio output is set to "Lucyd" on your phone

   4️⃣ Try playing different audio (music, video, etc.)

   Any sound now?
   ```
2. Add Quick Replies:
   - "✅ Audio working!" → Success → End
   - "❌ Still silent" → Factory reset step

### Step 9: Create Charging Branch
1. When customer clicks "Charging Issues", send:
   ```
   Let's fix the charging issue! 🔋

   When you connect the charger, does the LED light turn on?
   ```
2. Add Quick Replies:
   - "Yes, LED is on"
   - "No LED light"
   - "LED blinks/flashes"

### Step 10: Add LED Responses
1. For "No LED light", send:
   ```
   No LED usually means a connection issue. Try this:

   1️⃣ Clean the charging contacts on the glasses with a dry cloth

   2️⃣ Clean the magnetic pins on the cable

   3️⃣ Make sure the magnets snap firmly into place

   4️⃣ Try a different USB port or power adapter

   Is the LED lighting up now?
   ```
2. Add Quick Replies:
   - "✅ LED is on now" → Charging tips → End
   - "❌ Still no LED" → Agent handoff

### Step 11: Create App Setup Branch
1. When customer clicks "App Setup", send:
   ```
   Let's get you set up with the Lucyd app! 📲

   1️⃣ Download the Lucyd app:
      • iPhone: App Store → Search "Lucyd"
      • Android: Google Play → Search "Lucyd"

   2️⃣ Open the app and create an account

   3️⃣ Make sure your glasses are ON and charged

   4️⃣ Tap "Add Device" and follow the prompts

   Are your glasses connected in the app?
   ```
2. Add Quick Replies:
   - "✅ Connected!" → Success → End
   - "❌ Won't connect" → Bluetooth troubleshooting
   - "Can't find app" → App store links

### Step 12: Create Factory Reset Branch
1. When customer clicks "Factory Reset", send:
   ```
   Here's how to factory reset your Lucyd glasses: 🔄

   1️⃣ Make sure glasses are turned ON

   2️⃣ Press and hold BOTH temple buttons at the same time

   3️⃣ Keep holding for 10 seconds

   4️⃣ You'll hear a tone confirming the reset

   5️⃣ Glasses will turn off and restart

   ⚠️ After reset, you'll need to re-pair with your phone.

   Ready to try?
   ```
2. Add Quick Replies:
   - "✅ Reset complete" → Re-pairing instructions
   - "No tone heard" → Troubleshooting or Agent

### Step 13: Create "Other Issue" Handoff
1. When customer clicks "Other Issue", send:
   ```
   I'll connect you with our tech support team! 👋

   Please describe your issue and include your order number if you have it.

   Someone will be with you shortly!
   ```
2. Add action: **Create ticket**
   - Tags: `TECH-SUPPORT`, `chat-escalation`
   - Assign to: Order Support team

### Step 14: Add Success Endings
1. Create a success message for resolved issues:
   ```
   Awesome! Glad that's working now! 🎉

   Anything else I can help with?
   ```
2. Add Quick Replies:
   - "Another Question" → Back to issue selection
   - "All Set, Thanks!" → End flow

### Step 15: Save & Publish
1. Click **"Save"**
2. Click **"Publish"**
3. **Test:** Type "my glasses won't connect" in chat

---

## Flow 3: Prescription Help (20 minutes)

### Step 1: Create New Flow
1. Click **"Create Flow"**
2. Name it: `Prescription Help Self-Service`

### Step 2: Set Trigger
1. Trigger: **Chat message received**
2. Message contains any of:
   ```
   prescription, Rx, PD, pupillary, lens, vision, glasses prescription, progressive, bifocal
   ```

### Step 3: Add Topic Selection
1. Send message with Quick Replies:
   ```
   I can help with your prescription order! 👓

   What do you need help with?
   ```
2. Add buttons:
   - 📤 Submit My Prescription
   - 📏 Measure My PD
   - ⏱️ Processing Time
   - 👁️ Vision Seems Off
   - ❓ What Rx Can You Do?
   - 💬 Other Question

### Step 4: Create Submit Rx Branch
1. For "Submit My Prescription", send:
   ```
   There are 3 easy ways to submit your prescription: 📋

   1️⃣ Upload during checkout
      Select "Prescription Lenses" → Upload photo or enter values

   2️⃣ Email your prescription
      Send to info@lucyd.co with your order number in subject

   3️⃣ We contact your doctor
      Provide their name and phone, we'll request it

   Your prescription must be:
   • Less than 2 years old
   • Include SPH, CYL, Axis, and PD values

   Does this help?
   ```
2. Add Quick Replies:
   - "Got It!" → End
   - "What's PD?" → PD branch
   - "Talk to Agent" → Handoff

### Step 5: Create PD Measurement Branch
1. For "Measure My PD", send:
   ```
   PD (Pupillary Distance) is the distance between your pupils. 📏

   Easiest method - Use the Lucyd App:
   1. Open the Lucyd app
   2. Go to "Measure PD"
   3. Hold a credit card to your forehead (for scale)
   4. Look at the camera
   5. App calculates automatically!

   Already have glasses? Your PD might be on your old prescription.

   Know your PD already?
   ```
2. Add Quick Replies:
   - "Yes, I Have It" → Success → End
   - "Need Manual Method" → Mirror method
   - "Need Help" → Agent

### Step 6: Add Manual PD Method
1. For "Need Manual Method", send:
   ```
   Manual PD measurement: 📏

   1️⃣ Stand 8 inches from a mirror

   2️⃣ Hold a mm ruler against your brow

   3️⃣ Close your RIGHT eye

   4️⃣ Align the 0mm mark with the center of your LEFT pupil

   5️⃣ Close your LEFT eye, open your RIGHT

   6️⃣ Read the measurement at your RIGHT pupil

   That number (usually 57-72mm) is your PD!

   Got your measurement?
   ```
2. Add Quick Replies:
   - "Yes, Got It!" → Success → End
   - "Not Sure I Did It Right" → Offer photo assistance or Agent

### Step 7: Create Processing Time Branch
1. For "Processing Time", send:
   ```
   Here's the timeline for prescription orders: ⏱️

   📋 Rx Verification: 1-2 business days
   🔬 Lens Crafting: 5-7 business days
   ✅ Quality Check: 1 business day
   📦 Shipping: 3-5 business days

   Total: 10-15 business days

   We'll email you at each stage!

   Have you already placed an order?
   ```
2. Add Quick Replies:
   - "Yes, Check My Order" → Order lookup
   - "No, Just Planning" → End
   - "Need It Faster" → Agent handoff

### Step 8: Create Vision Issue Branch
1. For "Vision Seems Off", send:
   ```
   Sorry your vision isn't right! 👁️

   First question: How long have you been wearing your new glasses?
   ```
2. Add Quick Replies:
   - "Less than 1 week"
   - "1-2 weeks"
   - "More than 2 weeks"

### Step 9: Add Vision Adjustment Response
1. For "Less than 1 week", send:
   ```
   It's normal to have an adjustment period! 🕐

   What to expect (first 1-2 weeks):
   • Mild headaches or eye strain
   • Slight distortion at edges
   • Progressives: Learning the sweet spots

   Tips:
   • Wear them consistently
   • Start with a few hours, increase daily

   NOT normal (contact us):
   • Severe headaches
   • Double vision
   • Significant blur that doesn't improve

   How would you describe your issue?
   ```
2. Add Quick Replies:
   - "Mild, I'll Adjust" → Encouragement → End
   - "Seems More Serious" → Agent handoff

### Step 10: Add 2+ Weeks Response
1. For "More than 2 weeks", send:
   ```
   After 2 weeks, you should be mostly adjusted.

   If still having issues, it could be:
   • Prescription needs verification
   • PD measurement was off
   • Rx may have changed

   Let me connect you with our Rx team to help!
   ```
2. Add action: **Create ticket**
   - Tags: `PRESCRIPTION`, `vision-issue`, `remake-review`
   - Assign to: Prescription Services team

### Step 11: Create Rx Limits Branch
1. For "What Rx Can You Do?", send:
   ```
   Here's what prescriptions we can fill: 👓

   Single Vision:
   • SPH: up to ±8.00
   • CYL: up to ±4.00

   Progressive/Bifocal:
   • SPH: up to ±6.00
   • CYL: up to ±3.00
   • ADD: up to +3.00

   Lens options: Clear, Blue Light, Photochromic, Polarized

   Does your prescription fit?
   ```
2. Add Quick Replies:
   - "Yes, I'm Good!" → Shop link → End
   - "Mine Is Higher" → Agent for custom options
   - "Not Sure" → Agent

### Step 12: Save & Publish
1. Click **"Save"**
2. Click **"Publish"**
3. **Test:** Type "how do I submit my prescription" in chat

---

## Flow 4: Returns & Exchanges (15 minutes)

### Step 1: Create New Flow
1. Click **"Create Flow"**
2. Name it: `Returns & Exchanges Self-Service`

### Step 2: Set Trigger
1. Trigger: **Chat message received**
2. Message contains any of:
   ```
   return, exchange, refund, send back, damaged, broken, wrong item, doesn't fit, too big, too small
   ```

### Step 3: Add Return Type Selection
1. Send message with Quick Replies:
   ```
   I can help with returns and exchanges! ↩️

   What would you like to do?
   ```
2. Add buttons:
   - 📦 Item Arrived Damaged
   - 🔄 Exchange for Different
   - ↩️ Return for Refund
   - 🔍 Check Return Status
   - ❓ Return Policy Question

### Step 4: Create Damaged Item Branch
1. For "Item Arrived Damaged", send:
   ```
   I'm so sorry your item arrived damaged! 😔

   We'll get a replacement sent right away.

   Please provide:
   1. Your order number
   2. Photos of the damage

   You can share them here or email to info@lucyd.co
   ```
2. Add action: **Create ticket**
   - Tags: `RETURN/EXCHANGE`, `damaged-item`, `replacement`
   - Priority: **High**
   - Assign to: Warranty & Returns team

### Step 5: Create Exchange Branch
1. For "Exchange for Different", send:
   ```
   Happy to help with an exchange! 🔄

   Within 30 days, you can exchange for:
   • Different size
   • Different color/style
   • Different lens type

   Free shipping both ways!

   What would you like to exchange for?
   ```
2. Add Quick Replies:
   - "Different Size" → Size guide
   - "Different Style" → Agent to process
   - "Different Lenses" → Agent to process

### Step 6: Add Size Exchange Info
1. For "Different Size", send:
   ```
   Our sizes:

   • Small: Narrow faces (130-135mm)
   • Medium: Average faces (136-142mm) ⭐ Most popular
   • Large: Wider faces (143-150mm)

   If your current pair feels:
   • Too tight → Go up a size
   • Too loose → Go down a size

   Which size do you need?
   ```
2. Add Quick Replies:
   - "Small" → Agent to process
   - "Medium" → Agent to process
   - "Large" → Agent to process
   - "Not Sure" → Agent for help

### Step 7: Create Return Branch
1. For "Return for Refund", send:
   ```
   I can help with a return! ↩️

   Quick questions first:

   When did you receive your order?
   ```
2. Add Quick Replies:
   - "Within last 30 days"
   - "More than 30 days ago"
   - "Not sure"

### Step 8: Add Return Eligibility Check
1. For "Within last 30 days", send:
   ```
   Great! And are your glasses:
   ```
2. Add Quick Replies:
   - "Non-Prescription" → Eligible response
   - "Prescription Lenses" → Rx policy

### Step 9: Add Eligible Return Response
1. For "Non-Prescription", send:
   ```
   Good news! Your return is eligible for a full refund. ✅

   Requirements:
   • Glasses must be unworn
   • Tags still attached
   • Original packaging (preferred)

   Refund processed within 5-7 business days of receiving return.

   Ready to start your return?
   ```
2. Add Quick Replies:
   - "Yes, Start Return" → Agent to send label
   - "Exchange Instead" → Exchange branch
   - "Have Questions" → Agent

### Step 10: Add Rx Return Policy
1. For "Prescription Lenses", send:
   ```
   Important info about prescription returns: ⚠️

   Prescription lenses are non-refundable because they're custom-made for your vision.

   However, we CAN help if:
   • Vision isn't right → Free remake
   • Frame doesn't fit → Exchange frame
   • Quality issue → Replacement

   What's the issue with your glasses?
   ```
2. Add Quick Replies:
   - "Vision Problems" → Rx team handoff
   - "Frame Fit Issue" → Exchange branch
   - "Quality/Defect" → Warranty handoff

### Step 11: Create Return Policy Branch
1. For "Return Policy Question", send:
   ```
   Here's our return policy: 📋

   Non-Prescription:
   ✅ 30 days from delivery
   ✅ Full refund to original payment
   ✅ Free return shipping

   Prescription:
   ⚠️ Lenses non-refundable (custom)
   ✅ Frame exchanges available
   ✅ Vision issues → Free remakes

   Exchanges:
   ✅ Free within 30 days
   ✅ Different size, color, or style

   Any questions?
   ```
2. Add Quick Replies:
   - "Start a Return" → Return branch
   - "Start an Exchange" → Exchange branch
   - "Talk to Agent" → Agent

### Step 12: Save & Publish
1. Click **"Save"**
2. Click **"Publish"**
3. **Test:** Type "I want to return my glasses" in chat

---

## After Creating All Flows: Testing Checklist

### Test Each Flow
Open your chat widget and test these phrases:

| Type This | Should Trigger |
|-----------|---------------|
| "where is my order" | Order Tracking |
| "track my package" | Order Tracking |
| "bluetooth not working" | Technical Support |
| "how do I reset" | Technical Support |
| "submit prescription" | Prescription Help |
| "what's my PD" | Prescription Help |
| "I want to return" | Returns & Exchanges |
| "exchange for different size" | Returns & Exchanges |

### Verify Handoffs
1. Go through each flow until you reach "Talk to Agent"
2. Check that tickets are created with correct:
   - Tags
   - Team assignment
   - Priority (high for damaged items)

---

## Help Center Articles Setup

### Navigate to Help Center
Go to: https://lucyd.gorgias.com/app/settings/help-center
(or look for "Help Center" in Settings)

### Create Categories
1. Click "Add Category" for each:
   - 🚀 Getting Started
   - 🔧 Troubleshooting
   - 📦 Orders & Shipping
   - 👓 Prescriptions
   - ↩️ Returns & Exchanges
   - 🛡️ Warranty
   - 🛒 Product Info

### Add Articles
1. Click into a category
2. Click "Add Article"
3. Copy title and content from `gorgias_help_articles.md`
4. Click "Publish"

### Priority Articles (Do These First)
1. Track My Order
2. Return Policy
3. Bluetooth Pairing Guide
4. Factory Reset Guide
5. How to Submit Prescription

---

## Final Verification

### Check Everything Works
- [ ] Order Tracking flow triggers and shows Shopify data
- [ ] Technical Support flow branches correctly
- [ ] Prescription Help flow provides accurate info
- [ ] Returns flow checks eligibility correctly
- [ ] All "Talk to Agent" buttons create tickets
- [ ] Tickets have correct tags and team assignments
- [ ] Help Center articles are visible
- [ ] Search works in Help Center

### Monitor for First Week
- Check Gorgias Analytics daily
- Review tickets that came through flows
- Note any questions flows don't handle
- Adjust flow messages based on feedback

---

*Tutorial complete! Total implementation time: ~2-3 hours*

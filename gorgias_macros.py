#!/usr/bin/env python3
"""
Gorgias Macro Bulk Creator for Lucyd
Creates 26 new macros across 5 categories:
- Technical Support (6)
- Prescription Services (5)
- Product Questions (6)
- Warranty & Replacements (5)
- Social Media (4)
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import time

# Gorgias API Configuration
GORGIAS_DOMAIN = "lucyd"
API_USERNAME = "ecohen@lucyd.co"
API_KEY = "fffc8e1b1b20e4625bc1a29396219cb79778a1a63f05d235eecd290ae3ac3921"

BASE_URL = f"https://{GORGIAS_DOMAIN}.gorgias.com/api"
AUTH = HTTPBasicAuth(API_USERNAME, API_KEY)

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# All 26 Macros organized by category
MACROS = [
    # ==================== TECHNICAL SUPPORT (6) ====================
    {
        "name": "Tech: Bluetooth Pairing Issue",
        "body": """Hi {{ticket.customer.firstname}},

Thank you for reaching out! I'd be happy to help you connect your Lucyd glasses to your phone.

Please try these steps:
1. Make sure Bluetooth is enabled on your phone
2. On your glasses, press and hold the button for 5 seconds until you hear "pairing mode"
3. Look for "Lucyd" in your phone's Bluetooth settings and tap to connect
4. You should hear "connected" when successful

If you're still having trouble:
- Forget "Lucyd" from your phone's Bluetooth list and try again
- Make sure your glasses are charged (at least 20%)
- Try restarting your phone

Let me know if this helps or if you need further assistance!""",
        "tags": ["TECH-SUPPORT", "bluetooth"]
    },
    {
        "name": "Tech: App Download & Setup",
        "body": """Hi {{ticket.customer.firstname}},

Great question! Here's how to get started with the Lucyd app:

1. Download the Lucyd app from the App Store (iPhone) or Google Play Store (Android)
2. Open the app and create an account or sign in
3. Make sure your glasses are charged and turned on
4. Tap "Add Device" and follow the on-screen instructions to pair your glasses

The app allows you to:
- Customize touch controls
- Update firmware
- Access voice assistant settings
- Adjust audio settings

If you run into any issues during setup, please let me know and I'll help you through it!""",
        "tags": ["TECH-SUPPORT", "app"]
    },
    {
        "name": "Tech: Audio Not Working",
        "body": """Hi {{ticket.customer.firstname}},

I'm sorry to hear you're having audio issues with your glasses. Let's troubleshoot this together.

Please try the following:
1. Make sure your glasses are fully charged
2. Check that the volume is turned up (tap the right temple to increase volume)
3. Verify your phone's media volume is not muted
4. Try disconnecting and reconnecting Bluetooth

If audio is working on only one side:
- This may indicate a hardware issue
- Please let me know your order number and when you purchased your glasses so we can check warranty options

If audio is completely silent on both sides:
- Try a factory reset: Hold both temple buttons for 10 seconds until you hear a tone
- Reconnect to your phone after the reset

Let me know how it goes!""",
        "tags": ["TECH-SUPPORT", "audio", "WARRANTY"]
    },
    {
        "name": "Tech: Charging Issues",
        "body": """Hi {{ticket.customer.firstname}},

I understand you're having trouble charging your Lucyd glasses. Let's get this sorted out.

Please check the following:
1. Make sure the charging cable is securely connected to the glasses
2. The magnetic pins should align with the charging contacts on the temples
3. Try using a different USB port or power adapter
4. Look for the LED indicator light - it should turn on when charging

If the LED doesn't light up:
- Clean the charging contacts gently with a dry cloth
- Make sure there's no debris on the magnetic pins

If your glasses still won't charge, please provide your order number and I can help with warranty options.

Let me know what you find!""",
        "tags": ["TECH-SUPPORT", "charging"]
    },
    {
        "name": "Tech: Firmware Update",
        "body": """Hi {{ticket.customer.firstname}},

Keeping your Lucyd glasses updated ensures the best performance! Here's how to update the firmware:

1. Download/open the Lucyd app on your phone
2. Make sure your glasses are connected via Bluetooth
3. Go to Settings > Device > Check for Updates
4. If an update is available, tap "Update Now"
5. Keep your glasses near your phone and charged during the update (this takes about 5-10 minutes)

Important: Don't turn off your glasses or disconnect during the update.

If you're not seeing the update option, make sure you have the latest version of the Lucyd app installed.

Let me know if you need any help!""",
        "tags": ["TECH-SUPPORT", "firmware"]
    },
    {
        "name": "Tech: Reset Instructions",
        "body": """Hi {{ticket.customer.firstname}},

Here's how to perform a factory reset on your Lucyd glasses:

1. Make sure your glasses are turned on and charged
2. Press and hold BOTH temple buttons simultaneously for 10 seconds
3. You'll hear a tone confirming the reset
4. Your glasses will turn off and restart

After the reset:
- You'll need to re-pair your glasses with your phone
- Open your phone's Bluetooth settings, forget "Lucyd" if it's still listed
- Put your glasses in pairing mode (hold button 5 seconds) and reconnect

This often resolves connectivity issues, audio glitches, and other minor problems.

Let me know if you need any further assistance!""",
        "tags": ["TECH-SUPPORT", "reset"]
    },

    # ==================== PRESCRIPTION SERVICES (5) ====================
    {
        "name": "Rx: How to Submit Prescription",
        "body": """Hi {{ticket.customer.firstname}},

Thank you for choosing Lucyd for your prescription eyewear! Here's how to submit your prescription:

Option 1: Upload during checkout
- Select your frame and choose "Prescription Lenses"
- Upload a photo of your prescription or enter the values manually

Option 2: Email your prescription
- Send a photo of your valid prescription to info@lucyd.co
- Include your order number in the subject line

Option 3: We contact your doctor
- Provide your eye doctor's name and phone number
- We'll request the prescription on your behalf

Your prescription must be:
- Less than 2 years old
- Include SPH, CYL, Axis, and PD values

Let me know if you have any questions!""",
        "tags": ["PRESCRIPTION", "new-order"]
    },
    {
        "name": "Rx: PD Measurement Instructions",
        "body": """Hi {{ticket.customer.firstname}},

Your PD (Pupillary Distance) is essential for prescription lenses. Here's how to measure it:

Using the Lucyd App:
1. Open the Lucyd app and go to "Measure PD"
2. Follow the on-screen instructions using your phone camera
3. The app will calculate your PD automatically

Manual Method:
1. Stand 8 inches from a mirror
2. Hold a ruler against your brow
3. Close your right eye and align the 0 with your left pupil's center
4. Close your left eye, open your right, and read the measurement at your right pupil
5. This number (usually 57-72mm) is your PD

If your prescription includes PD, you can use that value.

Need help? Send us a straight-on selfie and we can help estimate your PD!""",
        "tags": ["PRESCRIPTION", "PD"]
    },
    {
        "name": "Rx: Lens Processing Time",
        "body": """Hi {{ticket.customer.firstname}},

Thank you for your prescription order! Here's what to expect:

Processing Timeline:
- Prescription verification: 1-2 business days
- Lens crafting: 5-7 business days
- Quality inspection: 1 business day
- Shipping: 3-5 business days (standard) or 2-3 days (express)

Total estimated time: 10-15 business days from order confirmation

We'll send you email updates at each stage:
1. Prescription received and verified
2. Lenses in production
3. Order shipped with tracking number

If you need your glasses sooner, please let me know and I'll check if we can expedite your order.

Thank you for your patience!""",
        "tags": ["PRESCRIPTION", "processing"]
    },
    {
        "name": "Rx: Prescription Issue/Redo",
        "body": """Hi {{ticket.customer.firstname}},

I'm sorry to hear you're having issues with your prescription lenses. We want to make sure your vision is perfect.

Please describe the issue you're experiencing:
- Blurry vision at certain distances?
- Headaches or eye strain?
- Vision seems off compared to your other glasses?

To help resolve this, please provide:
1. Your order number
2. A copy of your current prescription (if different from what we have on file)
3. How long you've been wearing the glasses (there can be an adjustment period of 1-2 weeks)

If there's an error on our end, we'll remake your lenses at no charge. If your prescription has changed, we can discuss your options.

Let me know and we'll get this sorted out for you!""",
        "tags": ["PRESCRIPTION", "remake", "WARRANTY"]
    },
    {
        "name": "Rx: Prescription Limits",
        "body": """Hi {{ticket.customer.firstname}},

Great question! Here are our prescription lens capabilities:

We can accommodate:
- Single Vision: SPH up to +/- 8.00, CYL up to +/- 4.00
- Progressive/Bifocal: SPH up to +/- 6.00, CYL up to +/- 3.00
- Reading: ADD up to +3.00

Lens options available:
- Clear, Blue Light Filtering
- Photochromic (transition)
- Polarized Sun
- Non-polarized tinted

If your prescription is outside these ranges, please send it over and we'll let you know if we can accommodate it or suggest alternatives.

Would you like to proceed with an order?""",
        "tags": ["PRESCRIPTION", "pre-sale"]
    },

    # ==================== PRODUCT QUESTIONS (6) ====================
    {
        "name": "Product: FSA/HSA Eligibility",
        "body": """Hi {{ticket.customer.firstname}},

Great news! Lucyd prescription glasses ARE eligible for FSA (Flexible Spending Account) and HSA (Health Savings Account) funds.

How to use your FSA/HSA:
1. Simply use your FSA/HSA debit card at checkout
2. Or pay with a regular card and submit the receipt to your FSA/HSA provider for reimbursement

What's covered:
- Prescription lenses (required)
- Frames with prescription lenses

Note: Non-prescription (plano) glasses are typically NOT FSA/HSA eligible.

We provide itemized receipts upon request that you can submit for reimbursement. Just let me know if you need one!

Any other questions?""",
        "tags": ["SALES", "FSA-HSA"]
    },
    {
        "name": "Product: Frame Sizing Guide",
        "body": """Hi {{ticket.customer.firstname}},

Finding the right fit is important! Here's how to choose your Lucyd frame size:

Our frames come in these sizes:
- Small: Best for narrow faces (Frame width: 130-135mm)
- Medium: Most popular, fits average faces (Frame width: 136-142mm)
- Large: For wider faces (Frame width: 143-150mm)

How to measure:
1. Take a pair of glasses that fit you well
2. Look for numbers inside the temple (e.g., 52-18-140)
3. The first number is lens width, second is bridge width
4. Add these together with the lens width again: 52+18+52 = 122mm frame width

Not sure? Our Medium size fits most adults comfortably.

Want a specific recommendation? Let me know your face shape or send a selfie and I'll suggest the best option!""",
        "tags": ["SALES", "sizing"]
    },
    {
        "name": "Product: Lens Options",
        "body": """Hi {{ticket.customer.firstname}},

Here are the lens options available for Lucyd glasses:

**Non-Prescription:**
- Clear with Blue Light Filter - Great for screen time
- Polarized Sunglasses - Reduces glare for outdoor use
- Photochromic - Transitions from clear to dark automatically

**Prescription:**
- Clear - Standard everyday lenses
- Blue Light Filter - Reduces digital eye strain
- Polarized - Best for driving and outdoor activities
- Photochromic - Versatile indoor/outdoor lenses

**Add-ons (included):**
- Anti-reflective coating
- Scratch resistance
- UV protection

Most popular combo: Blue Light Filter for everyday use + Polarized for a second pair of sunglasses.

Would you like recommendations based on your lifestyle?""",
        "tags": ["SALES", "lenses"]
    },
    {
        "name": "Product: Battery Life Info",
        "body": """Hi {{ticket.customer.firstname}},

Great question about battery life! Here's what you can expect:

**Typical Usage:**
- Music/podcast playback: 6-8 hours
- Phone calls: 4-5 hours
- Standby time: Up to 2 weeks

**Factors that affect battery:**
- Volume level
- Call frequency
- Bluetooth range from phone

**Charging:**
- Full charge: About 1.5 hours
- Quick charge: 15 minutes = 2 hours of use

The glasses come with a magnetic charging cable. You can also purchase an extra cable or the travel charging case as accessories.

Let me know if you have any other questions!""",
        "tags": ["SALES", "battery"]
    },
    {
        "name": "Product: Water Resistance",
        "body": """Hi {{ticket.customer.firstname}},

Lucyd glasses have IPX4 water resistance rating. Here's what that means:

**Safe for:**
- Light rain
- Sweat during workouts
- Splashes

**Not recommended for:**
- Swimming or submerging in water
- Heavy rain exposure
- Showering

**Care tips:**
- Wipe dry if they get wet
- Don't charge while wet
- Avoid extreme humidity for extended periods

The electronics are protected, but the glasses aren't designed for water activities. For intense workouts, they handle sweat perfectly fine!

Any other questions?""",
        "tags": ["SALES", "features"]
    },
    {
        "name": "Product: Compatibility Check",
        "body": """Hi {{ticket.customer.firstname}},

Lucyd glasses work with both iPhone and Android! Here are the details:

**Compatible with:**
- iPhone: iOS 13 or later (iPhone 6s and newer)
- Android: Version 8.0 or later with Bluetooth 5.0

**Features by platform:**
- Both: Music, calls, podcasts, audiobooks
- iPhone: Siri voice assistant
- Android: Google Assistant

**The Lucyd App:**
- Available on App Store and Google Play
- Used for firmware updates and settings customization

To check your phone:
- iPhone: Settings > General > About
- Android: Settings > About Phone > Software Information

99% of smartphones from the last 5 years work perfectly with Lucyd glasses.

What phone do you have? I can confirm compatibility!""",
        "tags": ["SALES", "compatibility"]
    },

    # ==================== WARRANTY & REPLACEMENTS (5) ====================
    {
        "name": "Warranty: Claim Process",
        "body": """Hi {{ticket.customer.firstname}},

I'm happy to help you with a warranty claim. Here's the process:

**Lucyd Warranty Coverage:**
- 1 year from purchase date
- Covers manufacturing defects
- Includes: speaker failure, charging issues, electronic malfunctions

**To start your claim, please provide:**
1. Your order number
2. Description of the issue
3. Photos or video showing the problem (if applicable)
4. Date you first noticed the issue

**What happens next:**
1. We review your claim (1-2 business days)
2. If approved, we'll send a replacement or repair instructions
3. You may need to return the defective item

Please note: Physical damage from drops, water damage, and normal wear are not covered.

Send over the details and we'll take care of you!""",
        "tags": ["WARRANTY", "claim"]
    },
    {
        "name": "Warranty: Speaker Replacement",
        "body": """Hi {{ticket.customer.firstname}},

I'm sorry to hear about the speaker issue. This is covered under our warranty if your glasses are less than 1 year old.

**To proceed, I'll need:**
1. Your order number
2. Which speaker is affected (left, right, or both)
3. When did the issue start?

**Quick troubleshooting first:**
- Have you tried a factory reset? (Hold both buttons for 10 seconds)
- Is your firmware up to date via the Lucyd app?

If troubleshooting doesn't help:
- We'll ship you a replacement pair
- Return the defective pair using a prepaid label we provide

If your glasses are out of warranty, we offer discounted replacement options. Let me know your order details and I'll check your coverage!""",
        "tags": ["WARRANTY", "speaker", "claim"]
    },
    {
        "name": "Warranty: Frame Replacement",
        "body": """Hi {{ticket.customer.firstname}},

I'm sorry to hear about the damage to your frames. Let me help you with options.

**If under warranty (within 1 year):**
Manufacturing defects (hinge failure, stress cracks) are covered. Please send:
- Order number
- Photos of the damage
- Description of how it happened

**If accidental damage:**
Unfortunately, drops and physical damage aren't covered by warranty, but we have options:
- Discounted replacement frames (contact us for pricing)
- Replacement parts if available for your model

**For prescription orders:**
If just the frame broke, your lenses may be transferable to a new frame.

Please send photos of the damage and your order number, and I'll let you know the best path forward!""",
        "tags": ["WARRANTY", "frame", "claim"]
    },
    {
        "name": "Warranty: Out of Warranty Options",
        "body": """Hi {{ticket.customer.firstname}},

I understand your glasses are past the 1-year warranty period. While we can't provide a free replacement, here are your options:

**Repair Service:**
- We may be able to repair certain issues for a fee
- Send us details of the problem and we'll provide a quote

**Discounted Replacement:**
- Loyal customers get special pricing on new frames
- Contact us for current offers

**Upgrade:**
- Trade in your old pair when purchasing new Lucyd glasses
- Check lucyd.co for current promotions

**DIY Solutions:**
- For minor issues, we can send replacement parts (charging cables, nose pads) at low cost

What issue are you experiencing? I'd like to find the best solution for your situation.""",
        "tags": ["WARRANTY", "out-of-warranty"]
    },
    {
        "name": "Warranty: Proof of Purchase Needed",
        "body": """Hi {{ticket.customer.firstname}},

To process your warranty claim, I'll need to verify your purchase. Please provide ONE of the following:

1. **Order number** - Starts with "LU" followed by numbers
2. **Order confirmation email** - Forward it to us or send a screenshot
3. **Receipt** - If purchased from a retailer
4. **Email used for purchase** - We can look up your order

If you purchased from:
- Lucyd.co: Check your email for "Order Confirmation from Lucyd"
- Amazon: Go to Your Orders and find the Lucyd purchase
- Retail store: Contact the store for receipt copy

Can't find any of these? Let me know approximately when and where you purchased, and I'll try to locate your order.

Looking forward to helping you!""",
        "tags": ["WARRANTY", "verification"]
    },

    # ==================== SOCIAL MEDIA (4) ====================
    {
        "name": "Social: Product Inquiry Reply",
        "body": """Hey! Thanks for your interest in Lucyd!

These are Bluetooth audio glasses with built-in speakers and mic - perfect for music, calls, and podcasts without earbuds.

Available with or without prescription lenses! Check them out at lucyd.co

Any questions? Happy to help!""",
        "tags": ["social-lead", "SALES"]
    },
    {
        "name": "Social: Where to Buy",
        "body": """Thanks for asking! You can get Lucyd glasses at:

lucyd.co - Our official site (best selection + prescription options)
Amazon - Search "Lucyd glasses"
Select optical retailers

Use code SOCIAL10 for 10% off at lucyd.co!

Need help choosing a style? DM us!""",
        "tags": ["social-lead", "SALES"]
    },
    {
        "name": "Social: Influencer/Collab Inquiry",
        "body": """Hey! Thanks for reaching out about a collaboration!

Please email our partnerships team at marketing@lucyd.co with:
- Your social handles and follower count
- Type of content you create
- Your collaboration idea

We love working with creators and review all inquiries. Looking forward to hearing from you!""",
        "tags": ["social-question", "PARTNERSHIP"]
    },
    {
        "name": "Social: Complaint Acknowledgment",
        "body": """Hi, we're really sorry to hear about your experience. This isn't the standard we hold ourselves to.

Please DM us your order details so we can look into this right away and make it right.

We appreciate you bringing this to our attention and want to resolve it for you ASAP.""",
        "tags": ["social-question", "negative", "ESCALATE"]
    },
]


def text_to_html(text):
    """Convert plain text to simple HTML"""
    # Escape HTML entities
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert newlines to <br/> and wrap paragraphs
    paragraphs = text.split("\n\n")
    html_parts = []
    for p in paragraphs:
        lines = p.split("\n")
        html_parts.append("<div>" + "<br/>".join(lines) + "</div>")
    return "<br/>".join(html_parts)


def create_macro(macro_data):
    """Create a single macro in Gorgias"""
    url = f"{BASE_URL}/macros"

    body_text = macro_data["body"]
    body_html = text_to_html(body_text)
    tags_str = ", ".join(macro_data.get("tags", []))

    actions = [
        {
            "name": "setResponseText",
            "title": "Add response text",
            "type": "user",
            "arguments": {
                "body_html": body_html,
                "body_text": body_text
            }
        }
    ]

    if tags_str:
        actions.append({
            "name": "addTags",
            "title": "Add tags",
            "type": "user",
            "arguments": {
                "tags": tags_str
            }
        })

    payload = {
        "name": macro_data["name"],
        "actions": actions
    }

    response = requests.post(url, auth=AUTH, headers=HEADERS, json=payload)
    return response


def get_existing_macros():
    """Get list of existing macros to avoid duplicates"""
    url = f"{BASE_URL}/macros"
    params = {"limit": 100}
    response = requests.get(url, auth=AUTH, headers=HEADERS, params=params)
    if response.status_code == 200:
        return {m["name"] for m in response.json().get("data", [])}
    return set()


def main():
    print("=" * 60)
    print("Gorgias Macro Bulk Creator for Lucyd")
    print("=" * 60)

    # Test API connection
    print("\nTesting API connection...")
    test_url = f"{BASE_URL}/account"
    test_response = requests.get(test_url, auth=AUTH, headers=HEADERS)

    if test_response.status_code != 200:
        print(f"ERROR: Failed to connect to Gorgias API")
        print(f"Status: {test_response.status_code}")
        print(f"Response: {test_response.text}")
        return

    print(f"Connected to: {test_response.json().get('domain', 'unknown')}.gorgias.com")

    # Get existing macros
    print("\nChecking existing macros...")
    existing_macros = get_existing_macros()
    print(f"Found {len(existing_macros)} existing macros")

    # Create new macros
    print(f"\nCreating {len(MACROS)} new macros...")
    print("-" * 60)

    created = 0
    skipped = 0
    failed = 0

    for i, macro in enumerate(MACROS, 1):
        name = macro["name"]

        if name in existing_macros:
            print(f"[{i:02d}/{len(MACROS)}] SKIP: '{name}' (already exists)")
            skipped += 1
            continue

        response = create_macro(macro)

        if response.status_code in [200, 201]:
            print(f"[{i:02d}/{len(MACROS)}] OK: '{name}'")
            created += 1
        else:
            print(f"[{i:02d}/{len(MACROS)}] FAIL: '{name}' - {response.status_code}")
            print(f"         Error: {response.text[:100]}")
            failed += 1

        # Small delay to avoid rate limiting
        time.sleep(0.3)

    # Summary
    print("-" * 60)
    print(f"\nSummary:")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed:  {failed}")
    print(f"  Total:   {len(MACROS)}")
    print("\nDone!")


if __name__ == "__main__":
    main()

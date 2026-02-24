#!/usr/bin/env python3
"""
Gorgias Help Center Article Paste Automation v2
Uses AppleScript to control Chrome and paste articles into Gorgias Help Center.
"""

import subprocess
import time

HELP_CENTER_URL = "https://lucyd.gorgias.com/app/settings/help-center/120364/articles"

# Category IDs from Gorgias selects
CATEGORY_VALUES = {
    "Warranty & Protection": "category-377091",
    "Product Info": "category-377095",
    "Orders & Shipping": "category-377096",
}

ARTICLES = [
    {
        "title": "My Frames Are Broken -- What Are My Options?",
        "category": "Warranty & Protection",
        "content": '<p>We\'re sorry your Lucyd frames are damaged! Here are your options.</p><p>The path forward depends on two factors: when you bought them and how the damage happened.</p><h2>STEP 1: DETERMINE YOUR COVERAGE</h2><ul><li>Within 1 year + Manufacturing defect &rarr; Full warranty replacement</li><li>Within 1 year + Accidental damage &rarr; Not covered by warranty (see options below)</li><li>Within 2 years + Lucyd Pro Insurance &rarr; Insurance claim (deductible applies)</li><li>Over 1 year + No insurance &rarr; Out of warranty (see options below)</li></ul><h2>IF IT\'S A MANUFACTURING DEFECT (WARRANTY)</h2><p>Signs of a manufacturing defect:</p><ul><li>Hinge broke during normal use (no drop/impact)</li><li>Frame cracked at a stress point without impact</li><li>Temple snapped while putting on/removing glasses</li><li>Joint separated with normal handling</li></ul><p>What to do:</p><ol><li>Contact us with your order number</li><li>Send 2-3 photos from different angles</li><li>Describe how/when the damage happened</li><li>We\'ll review and process a warranty replacement</li></ol><h2>IF IT\'S ACCIDENTAL DAMAGE</h2><p>Drops, impacts, sitting on glasses, and similar accidents are not covered by the standard warranty. Your options:</p><p><strong>Option A: Lucyd Pro Insurance Claim</strong><br>If you purchased Lucyd Pro, file an insurance claim. Small deductible applies, full replacement provided.</p><p><strong>Option B: Discounted Replacement</strong><br>Special pricing for existing customers on a new pair. Contact us for current offers.</p><p><strong>Option C: Paid Repair</strong><br>Some damage can be repaired for a fee. Send photos and we\'ll quote a repair price.</p><p><strong>Option D: Upgrade Trade-In</strong><br>Trade your damaged pair toward new Lucyd glasses. Ask about current trade-in programs.</p><h2>WHAT ABOUT MY PRESCRIPTION LENSES?</h2><p>If your lenses are undamaged, they may be transferable to a replacement frame of the same model. Ask us when you contact support.</p><h2>READY TO GET HELP?</h2><p>Contact us with:</p><ol><li>Your order number</li><li>2-3 photos of the damage</li><li>Description of how it happened</li><li>Whether you have Lucyd Pro insurance</li></ol><p>We\'ll get back to you within 1 business day with your best options!</p>',
    },
    {
        "title": "How to Photograph Damage for a Warranty Claim",
        "category": "Warranty & Protection",
        "content": '<p>Good photos help us process your claim faster!</p><p>Sending clear photos of the damage reduces back-and-forth and helps us resolve your claim quickly.</p><h2>WHAT WE NEED: 2-3 PHOTOS</h2><h3>Photo 1: Overall View</h3><ul><li>Hold glasses at arm\'s length</li><li>Show the full frame with damage visible</li><li>Good lighting, no shadows on the damage</li></ul><h3>Photo 2: Close-Up of Damage</h3><ul><li>Get as close as possible to the broken area</li><li>Make sure the damage is in focus</li><li>Show the break point clearly</li></ul><h3>Photo 3: Detail Shot (if applicable)</h3><ul><li>If both sides of a break are visible, show how they separated</li><li>If hinge damage, show the hinge area close-up</li><li>If multiple damage points, photograph each one</li></ul><h2>PHOTO TIPS</h2><p><strong>DO:</strong></p><ul><li>Use good, natural lighting</li><li>Hold the camera steady (rest on a table if needed)</li><li>Take photos on a plain, contrasting background</li><li>Make sure the damage area is in sharp focus</li><li>Include something for scale if helpful (coin, finger)</li></ul><p><strong>DON\'T:</strong></p><ul><li>Use flash directly on the damage (causes glare)</li><li>Take photos in dim lighting</li><li>Send blurry or out-of-focus images</li><li>Photograph from far away only</li></ul><h2>COMMON DAMAGE TYPES &amp; BEST ANGLES</h2><ul><li>Broken hinge &rarr; Side view showing hinge separation</li><li>Cracked frame &rarr; Front view + close-up of crack</li><li>Snapped temple &rarr; Show both pieces and break point</li><li>Nose bridge crack &rarr; Top-down view + front view</li><li>Joint separation &rarr; Side view showing gap</li></ul><h2>HOW TO SEND PHOTOS</h2><ul><li>Reply to your support ticket with photos attached</li><li>Or email to info@lucyd.co with your order number</li><li>Accepted formats: JPG, PNG (under 10MB each)</li></ul>',
    },
    {
        "title": "Warranty vs Accidental Damage: What's Covered?",
        "category": "Warranty & Protection",
        "content": '<p>Understanding what\'s covered helps set expectations and speeds up your claim.</p><h2>MANUFACTURING DEFECT (WARRANTY COVERED)</h2><p>A manufacturing defect means the product failed due to a flaw in materials or workmanship, NOT from external force.</p><p>Examples of covered defects:</p><ul><li>Hinge breaks during normal open/close action</li><li>Frame cracks at a stress point without any impact</li><li>Temple snaps while being worn or adjusted normally</li><li>Nose bridge separates without being bent or dropped</li><li>Screws fall out repeatedly despite being tightened</li><li>Frame warps or bends permanently from normal body heat</li></ul><p><strong>Key indicator:</strong> The damage happened during normal, everyday use with no external force or accident.</p><h2>ACCIDENTAL DAMAGE (NOT WARRANTY COVERED)</h2><p>Accidental damage results from external force, misuse, or events beyond normal wear.</p><p>Examples of accidental damage:</p><ul><li>Dropped glasses and frame cracked</li><li>Sat on glasses</li><li>Stepped on glasses</li><li>Glasses fell off head onto hard surface</li><li>Pet chewed on frames</li><li>Stored in back pocket and broke</li><li>Bent frames trying to adjust fit</li><li>Damage from extreme heat (left in hot car)</li></ul><h2>HOW WE DETERMINE THE CAUSE</h2><p>We look at:</p><ol><li>Break pattern &mdash; Clean snaps at stress points suggest defects; irregular breaks suggest impact</li><li>Location &mdash; Known weak points vs unusual locations</li><li>Timeline &mdash; Defects typically appear within months; impact damage is immediate</li><li>Photos &mdash; Visual evidence of the damage type</li></ol><h2>WHAT IF I DISAGREE?</h2><p>If you believe your damage is a manufacturing defect and we\'ve classified it as accidental:</p><ul><li>You can request a second review</li><li>Provide additional context or photos</li><li>Our team will re-evaluate</li></ul><h2>COVERAGE SUMMARY</h2><p><strong>Covered (Warranty):</strong> Hinge failure, stress cracks, joint separation, screw failure, material fatigue, normal use breakage</p><p><strong>Not Covered (Accidental):</strong> Drops and impacts, sitting/stepping on, bending/forcing, pet damage, heat damage, water submersion damage</p><h2>HAVE LUCYD PRO INSURANCE?</h2><p>Lucyd Pro covers BOTH manufacturing defects AND accidental damage. If you purchased Lucyd Pro, you\'re covered either way!</p>',
    },
    {
        "title": "Frame Damage Assessment Guide",
        "category": "Warranty & Protection",
        "content": '<p>This guide helps you understand how we assess frame damage claims.</p><h2>COMMON FRAME FAILURE POINTS</h2><ul><li><strong>Hinge joint</strong> &mdash; Common cause: Repeated open/close &mdash; Usually defect if &lt;12 months</li><li><strong>Temple mid-point</strong> &mdash; Common cause: Flexing/bending &mdash; Depends on force applied</li><li><strong>Nose bridge</strong> &mdash; Common cause: Stress from wear &mdash; Usually defect if no impact</li><li><strong>Frame front corners</strong> &mdash; Common cause: Impact point &mdash; Usually accidental</li><li><strong>Screw holes</strong> &mdash; Common cause: Material fatigue &mdash; Usually defect</li></ul><h2>FRAME MATERIALS &amp; EXPECTED DURABILITY</h2><p>Lucyd frames are designed for everyday use including:</p><ul><li>Daily wearing and removing</li><li>Normal adjustment for fit</li><li>Cleaning and handling</li><li>Carrying in a pouch or case</li></ul><h2>WHEN TO SUSPECT A DEFECT</h2><ul><li>Damage appears within the first 6 months</li><li>Break occurs at a known stress point (hinge, joint)</li><li>Customer describes normal use when damage occurred</li><li>Similar reports from same batch/model</li><li>Clean break pattern consistent with material failure</li></ul><h2>WHEN TO SUSPECT ACCIDENTAL DAMAGE</h2><ul><li>Impact marks visible near break point</li><li>Customer mentions a drop, sit-on, or similar event</li><li>Break pattern shows external force (splintering, crushing)</li><li>Damage at unusual location (not a stress point)</li><li>Cosmetic scratches/scuffs suggesting rough handling</li></ul><h2>ASSESSMENT PROCESS</h2><ol><li>Request photos (see photo guide article)</li><li>Check purchase date and order history</li><li>Review customer\'s description of events</li><li>Examine break pattern in photos</li><li>Check for known issues with that model/batch</li><li>Make determination and communicate clearly</li></ol>',
    },
    {
        "title": "Broken Frames FAQ: Hinges, Temples, Nose Bridge",
        "category": "Warranty & Protection",
        "content": '<p>Common questions about specific types of frame damage.</p><h2>HINGE ISSUES</h2><p><strong>Q: My hinge is loose. What should I do?</strong><br>A: A loose hinge can sometimes be tightened. Try using a small eyeglass screwdriver on the hinge screw. If the screw won\'t hold or keeps loosening, contact us &mdash; this may be a warranty issue.</p><p><strong>Q: The hinge broke completely. Is this covered?</strong><br>A: If the hinge broke during normal use (opening/closing your glasses), this is typically a manufacturing defect covered under warranty. Send us photos and your order number.</p><p><strong>Q: Can a broken hinge be repaired?</strong><br>A: In some cases, yes. Send photos and we\'ll assess whether repair is possible or if a full replacement is needed.</p><h2>TEMPLE (ARM) ISSUES</h2><p><strong>Q: One temple snapped off. Now what?</strong><br>A: This depends on how it happened:</p><ul><li>Broke during normal wear &rarr; Likely warranty covered</li><li>Broke from a drop or impact &rarr; Accidental damage (see options in &quot;My Frames Are Broken&quot; article)</li></ul><p><strong>Q: Can I get just one replacement temple?</strong><br>A: Due to the electronics in each temple, individual temple replacement isn\'t available. We replace the full pair.</p><p><strong>Q: The temple is bent. Can I straighten it?</strong><br>A: Light bending for fit adjustment is okay. If the temple is significantly bent from an impact, don\'t force it &mdash; this can cause further damage. Contact us for options.</p><h2>NOSE BRIDGE ISSUES</h2><p><strong>Q: The nose bridge cracked. What are my options?</strong><br>A: Nose bridge cracks during normal wear are typically covered under warranty. Contact us with photos and your order number.</p><p><strong>Q: The nose pads fell off. Can I replace them?</strong><br>A: Yes! Replacement nose pads are available. These are easy to replace yourself.</p><p><strong>Q: The frame is too tight/loose on my nose.</strong><br>A: Minor fit adjustments are normal. If the frame doesn\'t fit well, consider exchanging for a different size (free within 30 days).</p><h2>GENERAL FRAME QUESTIONS</h2><p><strong>Q: How long should Lucyd frames last?</strong><br>A: With proper care, Lucyd frames should last 2+ years. The 1-year warranty covers manufacturing defects. Lucyd Pro insurance extends protection to 2 years including accidental damage.</p><p><strong>Q: Do you sell just frames without electronics?</strong><br>A: No, Lucyd frames include integrated electronics. Replacement requires a full new pair.</p><p><strong>Q: Can my prescription lenses be moved to a new frame?</strong><br>A: Often yes, if the replacement is the same model and your lenses are undamaged. Ask us when filing your claim.</p>',
    },
    {
        "title": "Current Promotions & How to Apply Discount Codes",
        "category": "Product Info",
        "content": '<p>Find current deals and learn how to apply discount codes at checkout.</p><h2>HOW TO APPLY A DISCOUNT CODE</h2><ol><li>Add items to your cart at lucyd.co</li><li>Proceed to checkout</li><li>Look for &quot;Discount Code&quot; or &quot;Promo Code&quot; field</li><li>Enter your code exactly as provided (case-sensitive)</li><li>Click &quot;Apply&quot;</li><li>Discount appears in order total</li></ol><h2>DISCOUNT CODE NOT WORKING?</h2><p>Common issues:</p><ul><li>Expired code &mdash; Check the expiration date</li><li>Already used &mdash; Most codes are one-time use</li><li>Wrong case &mdash; Enter exactly as written</li><li>Minimum not met &mdash; Some codes require minimum purchase</li><li>Exclusions &mdash; Some items may be excluded (sale items, bundles)</li><li>Stacking &mdash; Only one code per order unless stated otherwise</li></ul><h2>WHERE TO FIND DISCOUNT CODES</h2><ul><li>Email newsletter (sign up at lucyd.co)</li><li>Social media (follow @lucabordigon on Instagram)</li><li>Seasonal sales and holiday promotions</li><li>First-time buyer offers</li></ul><h2>CURRENT OFFERS</h2><p>Visit lucyd.co for the latest promotions. Offers change regularly and may include seasonal sales, bundle deals, first-time buyer discounts, and newsletter subscriber specials.</p><h2>IMPORTANT NOTES</h2><ul><li>Discount codes cannot be applied retroactively to placed orders</li><li>Codes cannot be combined unless specifically stated</li><li>Sale prices and discount codes typically cannot be stacked</li><li>We cannot create custom discount codes upon request</li></ul><p>Questions? Contact us if you\'re having trouble applying a valid code at checkout!</p>',
    },
    {
        "title": "Amazon Orders: How to Get Support",
        "category": "Orders & Shipping",
        "content": '<p>Purchased Lucyd glasses on Amazon? Here\'s how to get help.</p><h2>FOR ORDER ISSUES (SHIPPING, RETURNS, REFUNDS)</h2><p>Amazon orders are fulfilled and managed by Amazon. For these issues, contact Amazon directly:</p><ul><li>Track your order: Amazon.com &rarr; Your Orders</li><li>Return request: Amazon.com &rarr; Your Orders &rarr; Return or Replace</li><li>Refund status: Amazon.com &rarr; Your Orders &rarr; View Return/Refund Status</li><li>Missing/wrong item: Contact Amazon Customer Service</li></ul><h2>FOR PRODUCT ISSUES (TECHNICAL SUPPORT, WARRANTY)</h2><p>We can help with product-related issues:</p><ul><li>Bluetooth pairing problems</li><li>Audio/charging issues</li><li>Firmware updates</li><li>Technical troubleshooting</li><li>Warranty claims (with Amazon order proof)</li></ul><p>Contact us with:</p><ul><li>Amazon order number (starts with 113- or similar)</li><li>Description of the issue</li><li>Photos if applicable</li></ul><h2>WARRANTY ON AMAZON PURCHASES</h2><p>The same 1-year warranty applies to Amazon purchases. To file a warranty claim:</p><ol><li>Provide your Amazon order number</li><li>Show proof of purchase (Amazon order confirmation)</li><li>Follow standard warranty claim process</li></ol><h2>IMPORTANT NOTES</h2><ul><li>We cannot process Amazon returns/refunds &mdash; only Amazon can</li><li>Amazon\'s return policy may differ from ours</li><li>Prescription lenses are NOT available through Amazon</li><li>Lucyd Pro insurance is NOT available for Amazon purchases</li></ul>',
    },
    {
        "title": "Wholesale & Partnership Inquiries",
        "category": "Product Info",
        "content": '<p>Interested in Lucyd for your business, retail store, or organization?</p><h2>WHOLESALE PURCHASING</h2><p>We offer wholesale pricing for:</p><ul><li>Optical retailers and eyewear stores</li><li>Corporate gifting programs</li><li>Employee wellness programs</li><li>Educational institutions</li><li>Gym and fitness centers</li></ul><p>Minimum Order: Contact us for current minimums</p><h2>WHAT WE PROVIDE WHOLESALE PARTNERS</h2><ul><li>Volume pricing discounts</li><li>Marketing materials and displays</li><li>Product training for your staff</li><li>Dedicated account manager</li><li>Custom packaging options (for large orders)</li></ul><h2>HOW TO INQUIRE</h2><p>Contact us with the following information:</p><ol><li>Business name and website</li><li>Type of business (retail, corporate, etc.)</li><li>Estimated order quantity</li><li>Desired product mix (models, sizes)</li><li>Your contact name, email, and phone</li><li>Any specific requirements</li></ol><h2>PARTNERSHIP OPPORTUNITIES</h2><p>We\'re also interested in:</p><ul><li>Retail distribution partnerships</li><li>Co-branding opportunities</li><li>Affiliate programs</li><li>Influencer collaborations</li><li>Technology integration partners</li></ul><h2>CONTACT</h2><p>Email: info@lucyd.co<br>Subject: &quot;Wholesale Inquiry&quot; or &quot;Partnership Inquiry&quot;</p><p>We typically respond to wholesale inquiries within 2-3 business days.</p>',
    },
    {
        "title": "Lucyd Pro Insurance: Is It Worth It?",
        "category": "Warranty & Protection",
        "content": '<p>Wondering if Lucyd Pro is a smart purchase? Here\'s an honest breakdown.</p><h2>WHAT LUCYD PRO ADDS BEYOND STANDARD WARRANTY</h2><p><strong>Standard Warranty (Free):</strong></p><ul><li>Manufacturing defects &mdash; 1 year</li><li>Accidental drops &mdash; NOT covered</li><li>Cracked/broken frames (if accidental) &mdash; NOT covered</li><li>Water damage &mdash; NOT covered</li><li>Theft &mdash; NOT covered</li></ul><p><strong>Lucyd Pro (Paid):</strong></p><ul><li>Manufacturing defects &mdash; 2 years</li><li>Accidental drops &mdash; COVERED</li><li>Cracked/broken frames &mdash; COVERED</li><li>Water damage &mdash; COVERED</li><li>Theft &mdash; COVERED (with police report)</li></ul><h2>THE BIG QUESTION: FRAMES</h2><p>25% of all support tickets involve broken frames. Without Lucyd Pro:</p><ul><li>Accidental frame damage = no free replacement</li><li>You\'ll need to purchase a new pair or pay for repair</li><li>Replacement cost is full retail price</li></ul><p>With Lucyd Pro:</p><ul><li>Accidental frame damage = small deductible for replacement</li><li>Covers drops, impacts, and accidents</li><li>2 claims during coverage period</li></ul><h2>WHO SHOULD GET LUCYD PRO?</h2><p><strong>Strongly recommended if you:</strong></p><ul><li>Are active or play sports while wearing glasses</li><li>Have a history of breaking glasses</li><li>Chose Lucyd as your only pair of glasses</li><li>Ordered expensive prescription lenses</li><li>Work in environments where damage is likely</li><li>Travel frequently</li></ul><p><strong>May not need it if you:</strong></p><ul><li>Are very careful with eyewear</li><li>Have backup glasses</li><li>Primarily use indoors at a desk</li><li>Ordered non-prescription (lower replacement cost)</li></ul><h2>COST COMPARISON</h2><p>Think about it this way:</p><ul><li>Lucyd Pro cost: A fraction of a new pair</li><li>Replacement without insurance: Full retail price</li><li>If you use even one claim, Lucyd Pro typically saves you money</li></ul><h2>HOW TO PURCHASE</h2><p>Lucyd Pro is available at checkout when ordering your glasses. It cannot be added after purchase.</p><h2>BOTTOM LINE</h2><p>If your Lucyd glasses are your primary eyewear, especially with prescription lenses, Lucyd Pro is a smart investment. The most common damage type (broken frames from accidental causes) is exactly what it covers.</p>',
    },
    {
        "title": "Common Frame Issues & When to Contact Us",
        "category": "Warranty & Protection",
        "content": '<p>Know what\'s normal, what\'s fixable at home, and when to reach out.</p><h2>NORMAL WEAR (NO ACTION NEEDED)</h2><p>These are normal and don\'t require support:</p><ul><li>Minor scratches on frame surface after months of use</li><li>Nose pads becoming slightly compressed over time</li><li>Slight loosening of fit (can be adjusted)</li><li>Temple tips softening with regular use</li></ul><h2>FIXABLE AT HOME</h2><ul><li>Loose hinge screw &rarr; Tighten with eyeglass screwdriver</li><li>Loose nose pads &rarr; Gently push back into place</li><li>Temples too tight &rarr; Warm gently with hairdryer, bend outward slightly</li><li>Temples too loose &rarr; Warm gently, bend inward slightly</li><li>Dirty frame &rarr; Clean with mild soap and lukewarm water</li></ul><p><strong>Be Gentle:</strong> When adjusting temples, apply minimal force. Excessive bending can cause permanent damage.</p><h2>CONTACT US FOR</h2><p><strong>High Priority:</strong></p><ul><li>Hinge broken or cracked &mdash; Likely warranty or replacement needed</li><li>Temple snapped &mdash; Cannot be repaired at home</li><li>Nose bridge cracked &mdash; Structural damage</li><li>Frame cracked anywhere &mdash; Replacement needed</li></ul><p><strong>Medium Priority:</strong></p><ul><li>Screw won\'t hold despite tightening &mdash; May need thread repair</li><li>Frame bent significantly &mdash; May affect electronics</li><li>Repeated same issue &mdash; Quality concern</li></ul><h2>PREVENTIVE CARE TIPS</h2><ol><li>Always use two hands to put on and remove glasses</li><li>Store in the pouch when not wearing</li><li>Never place face-down on hard surfaces</li><li>Don\'t push up on the bridge with one finger (stresses the frame)</li><li>Avoid leaving in hot cars (heat can warp frames)</li><li>Don\'t wear on top of head (stretches temples)</li><li>Clean regularly (sweat and oils can degrade materials)</li></ol><h2>WHEN FRAME DAMAGE IS URGENT</h2><p>Contact us immediately if:</p><ul><li>Sharp edges from a break (safety risk)</li><li>Broken lens near eyes</li><li>Electronics exposed from frame damage</li><li>Damage during first week of ownership</li></ul><p><strong>HOW TO CONTACT US</strong></p><p>Have your order number ready and include photos of any damage. This speeds up the process significantly!</p>',
    },
]


def run_applescript(script):
    """Run AppleScript and return output."""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout.strip(), result.returncode, result.stderr.strip()


def run_js(js_code):
    """Execute JS in Chrome via AppleScript using temp file."""
    tmp_path = "/tmp/gorgias_js_tmp.js"
    with open(tmp_path, "w") as f:
        f.write(js_code)

    script = '''tell application "Google Chrome"
    set jsCode to read POSIX file "/tmp/gorgias_js_tmp.js" as string
    execute front window's active tab javascript jsCode
end tell'''

    out, code, err = run_applescript(script)
    if code != 0:
        print(f"    JS ERROR: {err[:200]}")
        return None
    return out


def navigate(url):
    """Navigate Chrome active tab to URL."""
    run_applescript(
        f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'
    )
    time.sleep(4)


def create_article(article, index, total):
    """Create one article in Gorgias Help Center."""
    title = article["title"]
    category = article["category"]
    content = article["content"]
    cat_value = CATEGORY_VALUES[category]

    print(f"\n{'='*60}")
    print(f"[{index+1}/{total}] {title}")
    print(f"  Category: {category}")
    print(f"{'='*60}")

    # 1. Navigate to articles list
    print("  1. Navigating to articles list...")
    navigate(HELP_CENTER_URL)

    # 2. Click "Create Article" dropdown
    print("  2. Clicking Create Article...")
    result = run_js("""
var btns = Array.from(document.querySelectorAll('button, [role=button]'));
var btn = btns.find(function(b) { return b.textContent.indexOf('Create Article') >= 0; });
if (btn) { btn.click(); 'clicked'; } else { 'not found'; }
""")
    print(f"    -> {result}")
    time.sleep(1.5)

    # 3. Click "From scratch"
    print("  3. Clicking From scratch...")
    result = run_js("""
var els = Array.from(document.querySelectorAll('*'));
var el = els.find(function(e) {
    return e.textContent.trim() === 'From scratch'
        && e.offsetParent !== null
        && e.children.length === 0;
});
if (el) { el.click(); 'clicked'; } else { 'not found'; }
""")
    print(f"    -> {result}")
    time.sleep(3)

    # 4. Set title using native setter to trigger framework
    print("  4. Setting title...")
    escaped_title = title.replace("\\", "\\\\").replace("'", "\\'")
    result = run_js(f"""
var input = document.querySelector('input[placeholder=Title]');
if (input) {{
    var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    nativeSetter.call(input, '{escaped_title}');
    input.dispatchEvent(new Event('input', {{bubbles: true}}));
    input.dispatchEvent(new Event('change', {{bubbles: true}}));
    input.dispatchEvent(new Event('blur', {{bubbles: true}}));
    'set: ' + input.value.substring(0, 40);
}} else {{ 'input not found'; }}
""")
    print(f"    -> {result}")

    # 5. Set content in Froala editor
    print("  5. Setting content...")
    escaped_content = content.replace("\\", "\\\\").replace("'", "\\'")
    result = run_js(f"""
var editor = document.querySelector('.fr-element.fr-view');
if (editor) {{
    editor.focus();
    editor.innerHTML = '{escaped_content}';
    editor.dispatchEvent(new Event('input', {{bubbles: true}}));
    editor.dispatchEvent(new Event('change', {{bubbles: true}}));
    'set (' + editor.innerHTML.length + ' chars)';
}} else {{ 'editor not found'; }}
""")
    print(f"    -> {result}")

    # 6. Set category with full event simulation
    print(f"  6. Setting category to {category}...")
    result = run_js(f"""
var catSelect = document.querySelectorAll('select')[1];
if (catSelect) {{
    catSelect.focus();
    catSelect.dispatchEvent(new Event('focus', {{bubbles: true}}));
    catSelect.dispatchEvent(new MouseEvent('mousedown', {{bubbles: true}}));
    for (var i = 0; i < catSelect.options.length; i++) {{
        if (catSelect.options[i].value === '{cat_value}') {{
            catSelect.options[i].selected = true;
            break;
        }}
    }}
    catSelect.dispatchEvent(new Event('input', {{bubbles: true}}));
    catSelect.dispatchEvent(new Event('change', {{bubbles: true}}));
    catSelect.dispatchEvent(new MouseEvent('mouseup', {{bubbles: true}}));
    catSelect.dispatchEvent(new Event('blur', {{bubbles: true}}));
    'set: ' + catSelect.options[catSelect.selectedIndex].text;
}} else {{ 'category select not found'; }}
""")
    print(f"    -> {result}")

    # 7. Set visibility to Public
    print("  7. Setting visibility to Public...")
    result = run_js("""
var visSelects = document.querySelectorAll('select');
var visSelect = visSelects[0];
if (visSelect) {
    visSelect.focus();
    visSelect.dispatchEvent(new Event('focus', {bubbles: true}));
    visSelect.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
    for (var i = 0; i < visSelect.options.length; i++) {
        if (visSelect.options[i].text === 'Public') {
            visSelect.options[i].selected = true;
            break;
        }
    }
    visSelect.dispatchEvent(new Event('input', {bubbles: true}));
    visSelect.dispatchEvent(new Event('change', {bubbles: true}));
    visSelect.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
    visSelect.dispatchEvent(new Event('blur', {bubbles: true}));
    'set: ' + visSelect.options[visSelect.selectedIndex].text;
} else { 'visibility select not found'; }
""")
    print(f"    -> {result}")
    time.sleep(1)

    # 8. Click Save & Publish
    print("  8. Saving & Publishing...")
    result = run_js("""
var btns = Array.from(document.querySelectorAll('button'));
var btn = btns.find(function(b) { return b.textContent.indexOf('Save') >= 0 && b.textContent.indexOf('Publish') >= 0; });
if (btn) { btn.click(); 'clicked'; } else {
    btn = btns.find(function(b) { return b.textContent.indexOf('Save') >= 0; });
    if (btn) { btn.click(); 'clicked Save'; } else { 'not found'; }
}
""")
    print(f"    -> {result}")
    time.sleep(3)

    # 9. Verify
    result = run_js("""
var text = document.body.innerText;
var published = text.indexOf('PUBLISHED') >= 0;
var saved = text.indexOf('SAVED') >= 0;
var unsaved = text.indexOf('UNSAVED') >= 0;
published ? 'PUBLISHED' : (saved ? 'SAVED' : (unsaved ? 'UNSAVED' : 'UNKNOWN'));
""")
    print(f"  => Status: {result}")
    return result in ("PUBLISHED", "SAVED")


def main():
    print("=" * 60)
    print("GORGIAS HELP CENTER ARTICLE AUTOMATION v2")
    print(f"Creating {len(ARTICLES)} articles")
    print("=" * 60)

    success = 0
    failed = 0
    failed_articles = []

    for i, article in enumerate(ARTICLES):
        try:
            if create_article(article, i, len(ARTICLES)):
                success += 1
            else:
                failed += 1
                failed_articles.append(article["title"])
        except Exception as e:
            failed += 1
            failed_articles.append(article["title"])
            print(f"  EXCEPTION: {e}")

    print(f"\n{'='*60}")
    print(f"RESULTS: {success} published, {failed} failed")
    if failed_articles:
        print(f"Failed: {', '.join(failed_articles)}")
    print(f"{'='*60}")
    print(f"\nReminder: Delete duplicate 'My Frames Are Broken' from Uncategorized.")


if __name__ == "__main__":
    main()

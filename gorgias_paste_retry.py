#!/usr/bin/env python3
"""Retry the 4 failed articles with longer wait times."""

import subprocess
import time

HELP_CENTER_URL = "https://lucyd.gorgias.com/app/settings/help-center/120364/articles"

CATEGORY_VALUES = {
    "Warranty & Protection": "category-377091",
    "Product Info": "category-377095",
    "Orders & Shipping": "category-377096",
}

ARTICLES = [
    {
        "title": "Broken Frames FAQ: Hinges, Temples, Nose Bridge",
        "category": "Warranty & Protection",
        "content": '<p>Common questions about specific types of frame damage.</p><h2>HINGE ISSUES</h2><p><strong>Q: My hinge is loose. What should I do?</strong><br>A: A loose hinge can sometimes be tightened. Try using a small eyeglass screwdriver on the hinge screw. If the screw won\'t hold or keeps loosening, contact us &mdash; this may be a warranty issue.</p><p><strong>Q: The hinge broke completely. Is this covered?</strong><br>A: If the hinge broke during normal use (opening/closing your glasses), this is typically a manufacturing defect covered under warranty. Send us photos and your order number.</p><p><strong>Q: Can a broken hinge be repaired?</strong><br>A: In some cases, yes. Send photos and we\'ll assess whether repair is possible or if a full replacement is needed.</p><h2>TEMPLE (ARM) ISSUES</h2><p><strong>Q: One temple snapped off. Now what?</strong><br>A: This depends on how it happened:</p><ul><li>Broke during normal wear &rarr; Likely warranty covered</li><li>Broke from a drop or impact &rarr; Accidental damage (see options in &quot;My Frames Are Broken&quot; article)</li></ul><p><strong>Q: Can I get just one replacement temple?</strong><br>A: Due to the electronics in each temple, individual temple replacement isn\'t available. We replace the full pair.</p><p><strong>Q: The temple is bent. Can I straighten it?</strong><br>A: Light bending for fit adjustment is okay. If the temple is significantly bent from an impact, don\'t force it &mdash; this can cause further damage. Contact us for options.</p><h2>NOSE BRIDGE ISSUES</h2><p><strong>Q: The nose bridge cracked. What are my options?</strong><br>A: Nose bridge cracks during normal wear are typically covered under warranty. Contact us with photos and your order number.</p><p><strong>Q: The nose pads fell off. Can I replace them?</strong><br>A: Yes! Replacement nose pads are available. These are easy to replace yourself.</p><p><strong>Q: The frame is too tight/loose on my nose.</strong><br>A: Minor fit adjustments are normal. If the frame doesn\'t fit well, consider exchanging for a different size (free within 30 days).</p><h2>GENERAL FRAME QUESTIONS</h2><p><strong>Q: How long should Lucyd frames last?</strong><br>A: With proper care, Lucyd frames should last 2+ years. The 1-year warranty covers manufacturing defects. Lucyd Pro insurance extends protection to 2 years including accidental damage.</p><p><strong>Q: Do you sell just frames without electronics?</strong><br>A: No, Lucyd frames include integrated electronics. Replacement requires a full new pair.</p><p><strong>Q: Can my prescription lenses be moved to a new frame?</strong><br>A: Often yes, if the replacement is the same model and your lenses are undamaged. Ask us when filing your claim.</p>',
    },
    {
        "title": "Amazon Orders: How to Get Support",
        "category": "Orders & Shipping",
        "content": '<p>Purchased Lucyd glasses on Amazon? Here\'s how to get help.</p><h2>FOR ORDER ISSUES (SHIPPING, RETURNS, REFUNDS)</h2><p>Amazon orders are fulfilled and managed by Amazon. For these issues, contact Amazon directly:</p><ul><li>Track your order: Amazon.com &rarr; Your Orders</li><li>Return request: Amazon.com &rarr; Your Orders &rarr; Return or Replace</li><li>Refund status: Amazon.com &rarr; Your Orders &rarr; View Return/Refund Status</li><li>Missing/wrong item: Contact Amazon Customer Service</li></ul><h2>FOR PRODUCT ISSUES (TECHNICAL SUPPORT, WARRANTY)</h2><p>We can help with product-related issues:</p><ul><li>Bluetooth pairing problems</li><li>Audio/charging issues</li><li>Firmware updates</li><li>Technical troubleshooting</li><li>Warranty claims (with Amazon order proof)</li></ul><p>Contact us with:</p><ul><li>Amazon order number (starts with 113- or similar)</li><li>Description of the issue</li><li>Photos if applicable</li></ul><h2>WARRANTY ON AMAZON PURCHASES</h2><p>The same 1-year warranty applies to Amazon purchases. To file a warranty claim:</p><ol><li>Provide your Amazon order number</li><li>Show proof of purchase (Amazon order confirmation)</li><li>Follow standard warranty claim process</li></ol><h2>IMPORTANT NOTES</h2><ul><li>We cannot process Amazon returns/refunds &mdash; only Amazon can</li><li>Amazon\'s return policy may differ from ours</li><li>Prescription lenses are NOT available through Amazon</li><li>Lucyd Pro insurance is NOT available for Amazon purchases</li></ul>',
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


def run_js(js_code):
    tmp_path = "/tmp/gorgias_js_tmp.js"
    with open(tmp_path, "w") as f:
        f.write(js_code)
    script = '''tell application "Google Chrome"
    set jsCode to read POSIX file "/tmp/gorgias_js_tmp.js" as string
    execute front window's active tab javascript jsCode
end tell'''
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"    JS ERROR: {result.stderr.strip()[:200]}")
        return None
    return result.stdout.strip()


def navigate(url):
    subprocess.run(
        ["osascript", "-e", f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'],
        capture_output=True, text=True, timeout=10
    )
    time.sleep(5)  # Longer wait


def create_article(article, index, total):
    title = article["title"]
    category = article["category"]
    content = article["content"]
    cat_value = CATEGORY_VALUES[category]

    print(f"\n{'='*60}")
    print(f"[{index+1}/{total}] {title}")
    print(f"{'='*60}")

    # 1. Navigate
    print("  1. Navigating...")
    navigate(HELP_CENTER_URL)
    time.sleep(2)  # Extra wait for page to fully load

    # 2. Click Create Article
    print("  2. Create Article...")
    for attempt in range(3):
        result = run_js("""
var btns = Array.from(document.querySelectorAll('button, [role=button]'));
var btn = btns.find(function(b) { return b.textContent.indexOf('Create Article') >= 0; });
if (btn) { btn.click(); 'clicked'; } else { 'not found'; }
""")
        print(f"    -> {result}")
        if result == "clicked":
            break
        time.sleep(2)

    time.sleep(2)

    # 3. From scratch
    print("  3. From scratch...")
    for attempt in range(3):
        result = run_js("""
var els = Array.from(document.querySelectorAll('*'));
var el = els.find(function(e) {
    return e.textContent.trim() === 'From scratch'
        && e.offsetParent !== null
        && e.children.length === 0;
});
if (el) { el.click(); 'clicked'; } else { 'not found (attempt)'; }
""")
        print(f"    -> {result}")
        if result == "clicked":
            break
        time.sleep(1)

    time.sleep(4)  # Wait for editor to load

    # 4. Title
    print("  4. Title...")
    escaped_title = title.replace("\\", "\\\\").replace("'", "\\'")
    result = run_js(f"""
var input = document.querySelector('input[placeholder=Title]');
if (input) {{
    var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    nativeSetter.call(input, '{escaped_title}');
    input.dispatchEvent(new Event('input', {{bubbles: true}}));
    input.dispatchEvent(new Event('change', {{bubbles: true}}));
    input.dispatchEvent(new Event('blur', {{bubbles: true}}));
    'set';
}} else {{ 'not found'; }}
""")
    print(f"    -> {result}")

    # 5. Content
    print("  5. Content...")
    escaped_content = content.replace("\\", "\\\\").replace("'", "\\'")
    result = run_js(f"""
var editor = document.querySelector('.fr-element.fr-view');
if (editor) {{
    editor.focus();
    editor.innerHTML = '{escaped_content}';
    editor.dispatchEvent(new Event('input', {{bubbles: true}}));
    'set (' + editor.innerHTML.length + ' chars)';
}} else {{ 'not found'; }}
""")
    print(f"    -> {result}")

    # 6. Category
    print(f"  6. Category: {category}...")
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
}} else {{ 'not found'; }}
""")
    print(f"    -> {result}")

    # 7. Visibility
    print("  7. Public...")
    result = run_js("""
var visSelect = document.querySelectorAll('select')[0];
if (visSelect) {
    visSelect.focus();
    visSelect.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
    for (var i = 0; i < visSelect.options.length; i++) {
        if (visSelect.options[i].text === 'Public') { visSelect.options[i].selected = true; break; }
    }
    visSelect.dispatchEvent(new Event('change', {bubbles: true}));
    visSelect.dispatchEvent(new Event('blur', {bubbles: true}));
    'set';
} else { 'not found'; }
""")
    print(f"    -> {result}")
    time.sleep(1)

    # 8. Save
    print("  8. Save & Publish...")
    result = run_js("""
var btns = Array.from(document.querySelectorAll('button'));
var btn = btns.find(function(b) { return b.textContent.indexOf('Save') >= 0; });
if (btn) { btn.click(); 'clicked'; } else { 'not found'; }
""")
    print(f"    -> {result}")
    time.sleep(3)

    # 9. Verify
    result = run_js("""
var t = document.body.innerText;
t.indexOf('PUBLISHED') >= 0 ? 'PUBLISHED' : (t.indexOf('UNSAVED') >= 0 ? 'UNSAVED' : 'UNKNOWN');
""")
    print(f"  => {result}")
    return result == "PUBLISHED"


def main():
    print("Retrying 4 failed articles with longer waits...\n")
    success = 0
    for i, a in enumerate(ARTICLES):
        if create_article(a, i, len(ARTICLES)):
            success += 1
    print(f"\nDone: {success}/{len(ARTICLES)} published")


if __name__ == "__main__":
    main()

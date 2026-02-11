"""
Shopify Daily Report — Sales summary, late orders, top products.
Outputs to terminal, CSV, and optionally email.

Usage:
    python3 shopify_daily_report.py              # terminal + CSV
    python3 shopify_daily_report.py --email      # terminal + CSV + email
"""

import os
import csv
import smtplib
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import requests
from dotenv import load_dotenv

load_dotenv()

STORE = os.getenv("SHOPIFY_STORE")
TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
API_VERSION = "2025-01"
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": TOKEN,
}

LATE_THRESHOLD_DAYS = 5
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")

ORDERS_QUERY = """
query($cursor: String, $query: String) {
  orders(first: 50, after: $cursor, sortKey: CREATED_AT, reverse: true, query: $query) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        name
        createdAt
        displayFinancialStatus
        displayFulfillmentStatus
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        subtotalPriceSet {
          shopMoney {
            amount
          }
        }
        totalDiscountsSet {
          shopMoney {
            amount
          }
        }
        totalRefundedSet {
          shopMoney {
            amount
          }
        }
        customer {
          firstName
          lastName
          email
        }
        lineItems(first: 20) {
          edges {
            node {
              title
              quantity
              originalUnitPriceSet {
                shopMoney {
                  amount
                }
              }
              sku
            }
          }
        }
      }
    }
  }
}
"""


# ---------- API ----------

def fetch_orders(query_filter=None, max_pages=10):
    all_orders = []
    cursor = None

    for _ in range(max_pages):
        variables = {}
        if cursor:
            variables["cursor"] = cursor
        if query_filter:
            variables["query"] = query_filter

        resp = requests.post(
            ENDPOINT, headers=HEADERS,
            json={"query": ORDERS_QUERY, "variables": variables},
        )
        resp.raise_for_status()
        data = resp.json()

        if "errors" in data:
            for err in data["errors"]:
                if "ACCESS_DENIED" not in str(err):
                    print(f"  API error: {err['message']}")
            break

        orders_data = data["data"]["orders"]
        for edge in orders_data["edges"]:
            all_orders.append(edge["node"])

        if orders_data["pageInfo"]["hasNextPage"]:
            cursor = orders_data["pageInfo"]["endCursor"]
        else:
            break

    return all_orders


# ---------- Analysis ----------

def get_today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def analyze_todays_sales(orders):
    today = get_today_str()
    todays = [o for o in orders if o["createdAt"][:10] == today]

    total_revenue = sum(float(o["totalPriceSet"]["shopMoney"]["amount"]) for o in todays)
    total_orders = len(todays)
    avg_order = total_revenue / total_orders if total_orders else 0

    paid = [o for o in todays if o["displayFinancialStatus"] == "PAID"]
    refunded = [o for o in todays if o["displayFinancialStatus"] == "REFUNDED"]
    total_refunded = sum(
        float(o.get("totalRefundedSet", {}).get("shopMoney", {}).get("amount", 0))
        for o in todays
    )
    total_discounts = sum(
        float(o.get("totalDiscountsSet", {}).get("shopMoney", {}).get("amount", 0))
        for o in todays
    )

    return {
        "date": today,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order,
        "paid_count": len(paid),
        "refunded_count": len(refunded),
        "total_refunded": total_refunded,
        "total_discounts": total_discounts,
        "orders": todays,
    }


def find_late_orders(orders):
    cutoff = datetime.now(timezone.utc) - timedelta(days=LATE_THRESHOLD_DAYS)
    late = []
    for o in orders:
        created = datetime.fromisoformat(o["createdAt"].replace("Z", "+00:00"))
        status = o["displayFulfillmentStatus"]
        financial = o["displayFinancialStatus"]

        if financial == "PAID" and status in ("UNFULFILLED", "IN_PROGRESS", "ON_HOLD") and created < cutoff:
            days_old = (datetime.now(timezone.utc) - created).days
            late.append({**o, "_days_old": days_old})

    late.sort(key=lambda x: x["_days_old"], reverse=True)
    return late


def top_products(orders):
    product_qty = Counter()
    product_revenue = defaultdict(float)

    for o in orders:
        for item in o["lineItems"]["edges"]:
            li = item["node"]
            qty = li["quantity"]
            title = li["title"]
            price = float(li["originalUnitPriceSet"]["shopMoney"]["amount"])
            product_qty[title] += qty
            product_revenue[title] += price * qty

    return sorted(
        [(title, product_qty[title], product_revenue[title]) for title in product_qty],
        key=lambda x: x[2], reverse=True,
    )[:15]


# ---------- Output: Terminal ----------

def print_report(sales, late, products):
    print(f"\n{'='*65}")
    print(f"  LUCYD DAILY REPORT — {sales['date']}")
    print(f"{'='*65}")

    print(f"\n  SALES SUMMARY")
    print(f"  {'─'*40}")
    print(f"  Orders today:       {sales['total_orders']}")
    print(f"  Revenue:            ${sales['total_revenue']:,.2f}")
    print(f"  Avg order value:    ${sales['avg_order_value']:,.2f}")
    print(f"  Discounts given:    ${sales['total_discounts']:,.2f}")
    print(f"  Refunds:            ${sales['total_refunded']:,.2f} ({sales['refunded_count']} orders)")

    print(f"\n  LATE ORDERS (unfulfilled {LATE_THRESHOLD_DAYS}+ days)")
    print(f"  {'─'*40}")
    if late:
        for o in late:
            customer = o.get("customer") or {}
            name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
            total = float(o["totalPriceSet"]["shopMoney"]["amount"])
            print(f"  {o['name']}  |  {o['_days_old']}d late  |  ${total:,.2f}  |  {name or 'N/A'}  |  {o['displayFulfillmentStatus']}")
        print(f"\n  Total late orders: {len(late)}")
    else:
        print("  None — all orders fulfilled on time!")

    print(f"\n  TOP PRODUCTS (today)")
    print(f"  {'─'*40}")
    if products:
        for title, qty, rev in products:
            print(f"  {qty:>4}x  ${rev:>10,.2f}  {title}")
    else:
        print("  No orders today.")

    print(f"\n{'='*65}\n")


# ---------- Output: CSV ----------

def export_csv(sales, late, products):
    os.makedirs(REPORT_DIR, exist_ok=True)
    date_str = sales["date"]

    # Sales summary CSV
    summary_path = os.path.join(REPORT_DIR, f"sales_summary_{date_str}.csv")
    with open(summary_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Value"])
        w.writerow(["Date", date_str])
        w.writerow(["Total Orders", sales["total_orders"]])
        w.writerow(["Revenue", f"${sales['total_revenue']:,.2f}"])
        w.writerow(["Avg Order Value", f"${sales['avg_order_value']:,.2f}"])
        w.writerow(["Discounts", f"${sales['total_discounts']:,.2f}"])
        w.writerow(["Refunds", f"${sales['total_refunded']:,.2f}"])

    # Today's orders CSV
    orders_path = os.path.join(REPORT_DIR, f"orders_{date_str}.csv")
    with open(orders_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Order", "Date", "Customer", "Email", "Total", "Financial Status", "Fulfillment Status", "Items"])
        for o in sales["orders"]:
            customer = o.get("customer") or {}
            name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
            items = "; ".join(
                f"{i['node']['title']} x{i['node']['quantity']}"
                for i in o["lineItems"]["edges"]
            )
            w.writerow([
                o["name"], o["createdAt"][:10], name or "N/A",
                customer.get("email", "N/A"),
                f"${float(o['totalPriceSet']['shopMoney']['amount']):,.2f}",
                o["displayFinancialStatus"], o["displayFulfillmentStatus"], items,
            ])

    # Late orders CSV
    late_path = os.path.join(REPORT_DIR, f"late_orders_{date_str}.csv")
    with open(late_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Order", "Date", "Days Late", "Customer", "Email", "Total", "Fulfillment Status"])
        for o in late:
            customer = o.get("customer") or {}
            name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
            w.writerow([
                o["name"], o["createdAt"][:10], o["_days_old"], name or "N/A",
                customer.get("email", "N/A"),
                f"${float(o['totalPriceSet']['shopMoney']['amount']):,.2f}",
                o["displayFulfillmentStatus"],
            ])

    print(f"  CSV files saved to {REPORT_DIR}/")
    return [summary_path, orders_path, late_path]


# ---------- Output: Email ----------

def build_html_report(sales, late, products):
    html = f"""
    <html><body style="font-family: Arial, sans-serif; color: #333; max-width: 700px;">
    <h2 style="color: #1a1a2e;">Lucyd Daily Report — {sales['date']}</h2>

    <h3>Sales Summary</h3>
    <table style="border-collapse: collapse; width: 100%;">
        <tr><td style="padding: 6px 12px; border-bottom: 1px solid #eee;"><b>Orders today</b></td>
            <td style="padding: 6px 12px; border-bottom: 1px solid #eee;">{sales['total_orders']}</td></tr>
        <tr><td style="padding: 6px 12px; border-bottom: 1px solid #eee;"><b>Revenue</b></td>
            <td style="padding: 6px 12px; border-bottom: 1px solid #eee;">${sales['total_revenue']:,.2f}</td></tr>
        <tr><td style="padding: 6px 12px; border-bottom: 1px solid #eee;"><b>Avg order value</b></td>
            <td style="padding: 6px 12px; border-bottom: 1px solid #eee;">${sales['avg_order_value']:,.2f}</td></tr>
        <tr><td style="padding: 6px 12px; border-bottom: 1px solid #eee;"><b>Discounts</b></td>
            <td style="padding: 6px 12px; border-bottom: 1px solid #eee;">${sales['total_discounts']:,.2f}</td></tr>
        <tr><td style="padding: 6px 12px; border-bottom: 1px solid #eee;"><b>Refunds</b></td>
            <td style="padding: 6px 12px; border-bottom: 1px solid #eee;">${sales['total_refunded']:,.2f} ({sales['refunded_count']} orders)</td></tr>
    </table>

    <h3>Late Orders (unfulfilled {LATE_THRESHOLD_DAYS}+ days) — {len(late)} total</h3>
    """

    if late:
        html += """<table style="border-collapse: collapse; width: 100%; font-size: 13px;">
        <tr style="background: #f5f5f5;">
            <th style="padding: 6px; text-align: left; border-bottom: 2px solid #ddd;">Order</th>
            <th style="padding: 6px; text-align: left; border-bottom: 2px solid #ddd;">Days Late</th>
            <th style="padding: 6px; text-align: left; border-bottom: 2px solid #ddd;">Total</th>
            <th style="padding: 6px; text-align: left; border-bottom: 2px solid #ddd;">Customer</th>
            <th style="padding: 6px; text-align: left; border-bottom: 2px solid #ddd;">Status</th>
        </tr>"""
        for o in late:
            customer = o.get("customer") or {}
            name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
            total = float(o["totalPriceSet"]["shopMoney"]["amount"])
            color = "#d32f2f" if o["_days_old"] >= 10 else "#e65100" if o["_days_old"] >= 7 else "#333"
            html += f"""<tr>
                <td style="padding: 5px; border-bottom: 1px solid #eee;">{o['name']}</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee; color: {color}; font-weight: bold;">{o['_days_old']}d</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee;">${total:,.2f}</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee;">{name or 'N/A'}</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee;">{o['displayFulfillmentStatus']}</td>
            </tr>"""
        html += "</table>"
    else:
        html += "<p style='color: green;'>All orders fulfilled on time!</p>"

    html += f"<h3>Top Products (today)</h3>"
    if products:
        html += """<table style="border-collapse: collapse; width: 100%; font-size: 13px;">
        <tr style="background: #f5f5f5;">
            <th style="padding: 6px; text-align: left; border-bottom: 2px solid #ddd;">Product</th>
            <th style="padding: 6px; text-align: right; border-bottom: 2px solid #ddd;">Qty</th>
            <th style="padding: 6px; text-align: right; border-bottom: 2px solid #ddd;">Revenue</th>
        </tr>"""
        for title, qty, rev in products:
            html += f"""<tr>
                <td style="padding: 5px; border-bottom: 1px solid #eee;">{title}</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee; text-align: right;">{qty}</td>
                <td style="padding: 5px; border-bottom: 1px solid #eee; text-align: right;">${rev:,.2f}</td>
            </tr>"""
        html += "</table>"
    else:
        html += "<p>No orders today.</p>"

    html += "<br><p style='color: #999; font-size: 11px;'>Generated by Lucyd Orders API</p></body></html>"
    return html


def send_email(html, csv_files):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    recipients = os.getenv("REPORT_RECIPIENTS", "").split(",")

    if not smtp_pass or smtp_pass == "REPLACE_WITH_APP_PASSWORD":
        print("  Skipping email — SMTP_PASSWORD not set in .env")
        print("  Set up a Google App Password and add it to .env")
        return

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = f"Lucyd Daily Report — {get_today_str()}"
    msg.attach(MIMEText(html, "html"))

    for path in csv_files:
        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(path)}")
            msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipients, msg.as_string())

    print(f"  Email sent to {', '.join(recipients)}")


# ---------- Main ----------

def main():
    send_mail = "--email" in sys.argv

    if not TOKEN:
        print("ERROR: SHOPIFY_ACCESS_TOKEN not set in .env")
        raise SystemExit(1)

    print(f"Fetching data from {STORE}...")

    # Fetch today's orders
    today = get_today_str()
    today_orders = fetch_orders(query_filter=f"created_at:>={today}", max_pages=20)

    # Fetch recent orders for late order detection (last 30 days)
    thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
    recent_orders = fetch_orders(query_filter=f"created_at:>={thirty_days_ago} fulfillment_status:unfulfilled", max_pages=20)

    # Analyze
    sales = analyze_todays_sales(today_orders)
    late = find_late_orders(recent_orders)
    products = top_products(today_orders)

    # Terminal output
    print_report(sales, late, products)

    # CSV export
    csv_files = export_csv(sales, late, products)

    # Email (optional)
    if send_mail:
        html = build_html_report(sales, late, products)
        send_email(html, csv_files)


if __name__ == "__main__":
    main()

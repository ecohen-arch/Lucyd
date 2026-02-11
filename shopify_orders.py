"""
Shopify Orders API - Fetch sales orders via GraphQL Admin API.
"""

import os
import json
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

ORDERS_QUERY = """
query($cursor: String) {
  orders(first: 25, after: $cursor, sortKey: CREATED_AT, reverse: true) {
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
        customer {
          firstName
          lastName
          email
        }
        lineItems(first: 10) {
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


def fetch_orders(max_pages=1):
    """Fetch orders with cursor-based pagination."""
    all_orders = []
    cursor = None

    for _ in range(max_pages):
        variables = {"cursor": cursor} if cursor else {}
        resp = requests.post(
            ENDPOINT,
            headers=HEADERS,
            json={"query": ORDERS_QUERY, "variables": variables},
        )
        resp.raise_for_status()
        data = resp.json()

        if "errors" in data:
            print("API Errors:", json.dumps(data["errors"], indent=2))
            break

        orders_data = data["data"]["orders"]
        for edge in orders_data["edges"]:
            all_orders.append(edge["node"])

        if orders_data["pageInfo"]["hasNextPage"]:
            cursor = orders_data["pageInfo"]["endCursor"]
        else:
            break

    return all_orders


def print_orders(orders):
    """Display orders in a readable format."""
    print(f"\n{'='*60}")
    print(f"  Found {len(orders)} orders")
    print(f"{'='*60}\n")

    for order in orders:
        total = order["totalPriceSet"]["shopMoney"]
        customer = order.get("customer") or {}
        name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()

        print(f"Order {order['name']}  |  {order['createdAt'][:10]}")
        print(f"  Customer: {name or 'N/A'}  ({customer.get('email', 'N/A')})")
        print(f"  Total: {total['amount']} {total['currencyCode']}")
        print(f"  Status: {order['displayFinancialStatus']} / {order['displayFulfillmentStatus']}")

        for item in order["lineItems"]["edges"]:
            li = item["node"]
            price = li["originalUnitPriceSet"]["shopMoney"]["amount"]
            print(f"    - {li['title']} (x{li['quantity']})  SKU: {li.get('sku', 'N/A')}  @ ${price}")

        print()


if __name__ == "__main__":
    if not TOKEN or TOKEN == "shpat_REPLACE_WITH_YOUR_TOKEN":
        print("ERROR: Set SHOPIFY_ACCESS_TOKEN in .env file first.")
        print("See Step 1 in the plan for how to create a custom app and get the token.")
        raise SystemExit(1)

    print(f"Fetching orders from {STORE}...")
    orders = fetch_orders(max_pages=2)
    print_orders(orders)

"""
Lucyd Shopify Dashboard — Streamlit app for sales analytics.

Run: streamlit run shopify_dashboard.py
"""

import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
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
        cancelledAt
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
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

@st.cache_data(ttl=300)
def fetch_orders(query_filter=None, max_pages=20):
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
            break
        orders_data = data["data"]["orders"]
        for edge in orders_data["edges"]:
            all_orders.append(edge["node"])
        if orders_data["pageInfo"]["hasNextPage"]:
            cursor = orders_data["pageInfo"]["endCursor"]
        else:
            break
    return all_orders


def orders_to_df(orders):
    rows = []
    for o in orders:
        customer = o.get("customer") or {}
        name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
        total = float(o["totalPriceSet"]["shopMoney"]["amount"])
        discounts = float(o.get("totalDiscountsSet", {}).get("shopMoney", {}).get("amount", 0))
        refunded = float(o.get("totalRefundedSet", {}).get("shopMoney", {}).get("amount", 0))
        created = datetime.fromisoformat(o["createdAt"].replace("Z", "+00:00"))

        items = []
        total_qty = 0
        for item in o["lineItems"]["edges"]:
            li = item["node"]
            items.append(li["title"])
            total_qty += li["quantity"]

        rows.append({
            "order": o["name"],
            "date": created,
            "date_str": created.strftime("%Y-%m-%d"),
            "customer": name or "N/A",
            "email": customer.get("email", "N/A"),
            "total": total,
            "discounts": discounts,
            "refunded": refunded,
            "net_revenue": total - refunded,
            "financial_status": o["displayFinancialStatus"],
            "fulfillment_status": o["displayFulfillmentStatus"],
            "cancelled": o.get("cancelledAt") is not None,
            "items": ", ".join(items),
            "item_count": total_qty,
        })
    return pd.DataFrame(rows)


def line_items_df(orders):
    rows = []
    for o in orders:
        created = datetime.fromisoformat(o["createdAt"].replace("Z", "+00:00"))
        for item in o["lineItems"]["edges"]:
            li = item["node"]
            rows.append({
                "date": created.strftime("%Y-%m-%d"),
                "order": o["name"],
                "product": li["title"],
                "sku": li.get("sku", "N/A"),
                "quantity": li["quantity"],
                "unit_price": float(li["originalUnitPriceSet"]["shopMoney"]["amount"]),
                "line_total": float(li["originalUnitPriceSet"]["shopMoney"]["amount"]) * li["quantity"],
            })
    return pd.DataFrame(rows)


# ---------- Dashboard ----------

def main():
    st.set_page_config(page_title="Lucyd Dashboard", page_icon="🕶️", layout="wide")
    st.title("Lucyd Sales Dashboard")

    # Sidebar controls
    st.sidebar.header("Filters")
    days_back = st.sidebar.selectbox("Date range", [7, 14, 30, 60, 90], index=2)
    start_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")

    with st.spinner("Fetching orders..."):
        orders = fetch_orders(query_filter=f"created_at:>={start_date}", max_pages=40)

    if not orders:
        st.warning("No orders found for this period.")
        return

    df = orders_to_df(orders)
    items_df = line_items_df(orders)

    # ---------- KPI Row ----------
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_df = df[df["date_str"] == today]
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_df = df[df["date_str"] == yesterday]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        val = today_df["total"].sum()
        delta = val - yesterday_df["total"].sum() if len(yesterday_df) else None
        st.metric("Today's Revenue", f"${val:,.2f}", delta=f"${delta:,.2f}" if delta else None)
    with col2:
        val = len(today_df)
        delta = val - len(yesterday_df) if len(yesterday_df) else None
        st.metric("Today's Orders", val, delta=delta)
    with col3:
        avg = today_df["total"].mean() if len(today_df) else 0
        st.metric("Avg Order Value", f"${avg:,.2f}")
    with col4:
        total_rev = df["total"].sum()
        st.metric(f"Revenue ({days_back}d)", f"${total_rev:,.2f}")
    with col5:
        st.metric(f"Orders ({days_back}d)", len(df))

    st.divider()

    # ---------- Revenue Over Time ----------
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Daily Revenue")
        daily = df.groupby("date_str").agg(
            revenue=("total", "sum"),
            orders=("order", "count"),
        ).reset_index()
        daily.columns = ["Date", "Revenue", "Orders"]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily["Date"], y=daily["Revenue"], name="Revenue", marker_color="#4CAF50"))
        fig.add_trace(go.Scatter(x=daily["Date"], y=daily["Orders"], name="Orders", yaxis="y2",
                                 mode="lines+markers", marker_color="#FF9800"))
        fig.update_layout(
            yaxis=dict(title="Revenue ($)", side="left"),
            yaxis2=dict(title="Orders", side="right", overlaying="y"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            height=350, margin=dict(t=30, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Fulfillment Status")
        status_counts = df["fulfillment_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        colors = {
            "FULFILLED": "#4CAF50", "UNFULFILLED": "#f44336", "IN_PROGRESS": "#FF9800",
            "ON_HOLD": "#9C27B0", "PARTIALLY_FULFILLED": "#2196F3",
        }
        fig = px.pie(status_counts, values="Count", names="Status",
                     color="Status", color_discrete_map=colors, hole=0.4)
        fig.update_layout(height=350, margin=dict(t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------- Late Orders ----------
    st.subheader(f"Late Orders (unfulfilled {LATE_THRESHOLD_DAYS}+ days)")
    cutoff = datetime.now(timezone.utc) - timedelta(days=LATE_THRESHOLD_DAYS)
    late_df = df[
        (df["financial_status"] == "PAID") &
        (df["fulfillment_status"].isin(["UNFULFILLED", "IN_PROGRESS", "ON_HOLD"])) &
        (df["date"] < cutoff)
    ].copy()
    late_df["days_late"] = late_df["date"].apply(lambda x: (datetime.now(timezone.utc) - x).days)
    late_df = late_df.sort_values("days_late", ascending=False)

    if len(late_df):
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.metric("Late Orders", len(late_df))
            avg_days = late_df["days_late"].mean()
            st.metric("Avg Days Late", f"{avg_days:.0f}")
            oldest = late_df["days_late"].max()
            st.metric("Oldest", f"{oldest} days")
        with col_b:
            display_late = late_df[["order", "date_str", "days_late", "customer", "total", "fulfillment_status"]].copy()
            display_late.columns = ["Order", "Date", "Days Late", "Customer", "Total", "Status"]
            display_late["Total"] = display_late["Total"].apply(lambda x: f"${x:,.2f}")

            def color_late(val):
                if isinstance(val, (int, float)):
                    if val >= 10:
                        return "color: #d32f2f; font-weight: bold"
                    elif val >= 7:
                        return "color: #e65100; font-weight: bold"
                return ""

            st.dataframe(
                display_late.style.applymap(color_late, subset=["Days Late"]),
                use_container_width=True, height=300,
            )
    else:
        st.success("All orders fulfilled on time!")

    st.divider()

    # ---------- Top Products ----------
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("Top Products by Revenue")
        if len(items_df):
            product_rev = items_df.groupby("product").agg(
                revenue=("line_total", "sum"),
                quantity=("quantity", "sum"),
            ).sort_values("revenue", ascending=True).tail(15).reset_index()
            fig = px.bar(product_rev, x="revenue", y="product", orientation="h",
                         color="quantity", color_continuous_scale="Oranges",
                         labels={"revenue": "Revenue ($)", "product": "", "quantity": "Units"})
            fig.update_layout(height=400, margin=dict(t=10, b=10, l=10))
            st.plotly_chart(fig, use_container_width=True)

    with col_right2:
        st.subheader("Top Products by Units Sold")
        if len(items_df):
            product_qty = items_df.groupby("product").agg(
                quantity=("quantity", "sum"),
                revenue=("line_total", "sum"),
            ).sort_values("quantity", ascending=True).tail(15).reset_index()
            fig = px.bar(product_qty, x="quantity", y="product", orientation="h",
                         color="revenue", color_continuous_scale="Greens",
                         labels={"quantity": "Units Sold", "product": "", "revenue": "Revenue ($)"})
            fig.update_layout(height=400, margin=dict(t=10, b=10, l=10))
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------- SKU Breakdown ----------
    st.subheader("SKU Performance")
    if len(items_df):
        sku_perf = items_df.groupby(["sku", "product"]).agg(
            quantity=("quantity", "sum"),
            revenue=("line_total", "sum"),
        ).sort_values("revenue", ascending=False).reset_index()
        sku_perf.columns = ["SKU", "Product", "Units Sold", "Revenue"]
        sku_perf["Revenue"] = sku_perf["Revenue"].apply(lambda x: f"${x:,.2f}")
        st.dataframe(sku_perf, use_container_width=True, height=300)

    st.divider()

    # ---------- Discounts Analysis ----------
    st.subheader("Discount Analysis")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        total_discounts = df["discounts"].sum()
        total_gross = df["total"].sum() + total_discounts
        discount_rate = (total_discounts / total_gross * 100) if total_gross else 0
        st.metric("Total Discounts", f"${total_discounts:,.2f}")
        st.metric("Discount Rate", f"{discount_rate:.1f}%")
    with col_d2:
        daily_disc = df.groupby("date_str").agg(
            discounts=("discounts", "sum"),
        ).reset_index()
        daily_disc.columns = ["Date", "Discounts"]
        fig = px.area(daily_disc, x="Date", y="Discounts",
                      color_discrete_sequence=["#e91e63"])
        fig.update_layout(height=200, margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------- Recent Orders Table ----------
    st.subheader("Recent Orders")

    status_filter = st.sidebar.multiselect(
        "Fulfillment status",
        df["fulfillment_status"].unique().tolist(),
        default=df["fulfillment_status"].unique().tolist(),
    )
    filtered = df[df["fulfillment_status"].isin(status_filter)]

    display_df = filtered[["order", "date_str", "customer", "email", "total", "discounts",
                           "financial_status", "fulfillment_status", "items"]].copy()
    display_df.columns = ["Order", "Date", "Customer", "Email", "Total", "Discounts",
                          "Payment", "Fulfillment", "Items"]
    display_df["Total"] = display_df["Total"].apply(lambda x: f"${x:,.2f}")
    display_df["Discounts"] = display_df["Discounts"].apply(lambda x: f"${x:,.2f}")

    st.dataframe(display_df, use_container_width=True, height=400)

    # ---------- CSV Download ----------
    st.sidebar.divider()
    st.sidebar.header("Export")
    csv_data = df.to_csv(index=False)
    st.sidebar.download_button("Download Orders CSV", csv_data, f"lucyd_orders_{today}.csv", "text/csv")

    items_csv = items_df.to_csv(index=False)
    st.sidebar.download_button("Download Products CSV", items_csv, f"lucyd_products_{today}.csv", "text/csv")

    if len(late_df):
        late_csv = late_df.to_csv(index=False)
        st.sidebar.download_button("Download Late Orders CSV", late_csv, f"lucyd_late_orders_{today}.csv", "text/csv")

    # Footer
    st.sidebar.divider()
    st.sidebar.caption(f"Data from {STORE}")
    st.sidebar.caption(f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}")
    st.sidebar.caption("Data cached for 5 min. Reload to refresh.")


if __name__ == "__main__":
    main()

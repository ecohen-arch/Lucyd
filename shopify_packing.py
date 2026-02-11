"""
Lucyd Packing Station Dashboard — For warehouse/fulfillment staff.
Run: streamlit run shopify_packing.py --server.port 8502
"""

import os
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
LOW_STOCK_THRESHOLD = 10

PRIORITY_MAP = {
    "CRITICAL": {"emoji": "🔴", "label": "CRITICAL", "color": "#d32f2f", "bg": "#ffebee", "desc": "10+ days"},
    "LATE": {"emoji": "🟠", "label": "LATE", "color": "#e65100", "bg": "#fff3e0", "desc": "5-9 days"},
    "SOON": {"emoji": "🟡", "label": "SHIP SOON", "color": "#f9a825", "bg": "#fff8e1", "desc": "3-4 days"},
    "NORMAL": {"emoji": "🟢", "label": "ON TIME", "color": "#2e7d32", "bg": "#e8f5e9", "desc": "0-2 days"},
}


# ---------- API ----------

def gql(query, variables=None):
    resp = requests.post(ENDPOINT, headers=HEADERS, json={"query": query, "variables": variables or {}})
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        real_errors = [e for e in data["errors"] if "ACCESS_DENIED" not in str(e)]
        if real_errors:
            st.error(f"API error: {real_errors[0]['message']}")
    return data.get("data")


UNFULFILLED_QUERY = """
query($cursor: String, $query: String) {
  orders(first: 50, after: $cursor, sortKey: CREATED_AT, reverse: false, query: $query) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id name createdAt
        displayFinancialStatus displayFulfillmentStatus
        note
        totalPriceSet { shopMoney { amount currencyCode } }
        totalShippingPriceSet { shopMoney { amount } }
        shippingAddress { city provinceCode province country countryCodeV2 }
        shippingLine { title }
        customer { firstName lastName email }
        lineItems(first: 30) {
          edges {
            node {
              title quantity sku
              variant { id }
              originalUnitPriceSet { shopMoney { amount } }
            }
          }
        }
      }
    }
  }
}
"""

INVENTORY_QUERY = """
query($cursor: String) {
  productVariants(first: 100, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id title sku inventoryQuantity
        product { title }
      }
    }
  }
}
"""


@st.cache_data(ttl=120)
def fetch_unfulfilled_orders():
    all_orders = []
    cursor = None
    for _ in range(40):
        variables = {"query": "fulfillment_status:unfulfilled financial_status:paid"}
        if cursor:
            variables["cursor"] = cursor
        data = gql(UNFULFILLED_QUERY, variables)
        if not data:
            break
        orders_data = data["orders"]
        for edge in orders_data["edges"]:
            all_orders.append(edge["node"])
        if orders_data["pageInfo"]["hasNextPage"]:
            cursor = orders_data["pageInfo"]["endCursor"]
        else:
            break
    return all_orders


@st.cache_data(ttl=300)
def fetch_inventory():
    all_variants = []
    cursor = None
    for _ in range(20):
        variables = {}
        if cursor:
            variables["cursor"] = cursor
        data = gql(INVENTORY_QUERY, variables)
        if not data:
            break
        v_data = data["productVariants"]
        for edge in v_data["edges"]:
            all_variants.append(edge["node"])
        if v_data["pageInfo"]["hasNextPage"]:
            cursor = v_data["pageInfo"]["endCursor"]
        else:
            break
    return all_variants


# ---------- Data Processing ----------

def process_orders(orders):
    now = datetime.now(timezone.utc)
    rows = []
    for o in orders:
        created = datetime.fromisoformat(o["createdAt"].replace("Z", "+00:00"))
        days_waiting = (now - created).days
        customer = o.get("customer") or {}
        name = f"{customer.get('firstName', '')} {customer.get('lastName', '')}".strip()
        shipping = o.get("shippingAddress") or {}
        location = ", ".join(filter(None, [shipping.get("city"), shipping.get("provinceCode"), shipping.get("country")]))
        state = shipping.get("province") or shipping.get("provinceCode") or "Unknown"
        country = shipping.get("countryCodeV2") or shipping.get("country") or "Unknown"
        shipping_line = (o.get("shippingLine") or {}).get("title") or "N/A"
        shipping_cost = float((o.get("totalShippingPriceSet") or {}).get("shopMoney", {}).get("amount", 0))

        items = []
        skus = []
        total_qty = 0
        for item in o["lineItems"]["edges"]:
            li = item["node"]
            items.append({"title": li["title"], "sku": li.get("sku", "N/A"), "qty": li["quantity"]})
            skus.append(li.get("sku", ""))
            total_qty += li["quantity"]

        if days_waiting >= 10:
            priority = "CRITICAL"
        elif days_waiting >= LATE_THRESHOLD_DAYS:
            priority = "LATE"
        elif days_waiting >= 3:
            priority = "SOON"
        else:
            priority = "NORMAL"

        rows.append({
            "order": o["name"],
            "created": created,
            "date_str": created.strftime("%b %d, %H:%M"),
            "days_waiting": days_waiting,
            "priority": priority,
            "customer": name or "N/A",
            "email": customer.get("email", "N/A"),
            "location": location or "N/A",
            "total": float(o["totalPriceSet"]["shopMoney"]["amount"]),
            "item_count": total_qty,
            "items": items,
            "items_str": " | ".join(f"{i['title']} x{i['qty']}" for i in items),
            "skus_str": ", ".join(filter(None, skus)),
            "note": o.get("note") or "",
            "state": state,
            "country": country,
            "shipping_method": shipping_line,
            "shipping_cost": shipping_cost,
        })

    df = pd.DataFrame(rows)
    if len(df):
        priority_order = {"CRITICAL": 0, "LATE": 1, "SOON": 2, "NORMAL": 3}
        df["priority_rank"] = df["priority"].map(priority_order)
        df = df.sort_values(["priority_rank", "days_waiting"], ascending=[True, False])
    return df


def process_inventory(variants):
    rows = []
    for v in variants:
        rows.append({
            "product": v.get("product", {}).get("title", "Unknown"),
            "variant": v["title"],
            "sku": v.get("sku") or "N/A",
            "stock": v["inventoryQuantity"],
        })
    return pd.DataFrame(rows)


# ---------- UI Components ----------

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }

/* Priority cards */
.priority-card {
    border-radius: 12px; padding: 20px; text-align: center;
    transition: transform 0.2s; cursor: default;
}
.priority-card:hover { transform: translateY(-2px); }
.priority-card .number { font-size: 42px; font-weight: 800; line-height: 1; }
.priority-card .label { font-size: 13px; font-weight: 600; letter-spacing: 0.5px; margin-top: 4px; }

/* Order cards */
.order-card {
    border-radius: 10px; padding: 16px 20px; margin: 8px 0;
    border-left: 6px solid; display: flex; align-items: center;
    justify-content: space-between; gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    transition: box-shadow 0.2s;
}
.order-card:hover { box-shadow: 0 3px 12px rgba(0,0,0,0.12); }
.order-card .order-id { font-size: 18px; font-weight: 700; }
.order-card .order-meta { font-size: 13px; color: #666; margin-top: 2px; }
.order-card .days-badge {
    font-size: 14px; font-weight: 700; padding: 4px 12px;
    border-radius: 20px; white-space: nowrap; min-width: 60px; text-align: center;
}
.order-card .items-count {
    font-size: 13px; color: #555; font-weight: 500;
    background: #f0f0f0; padding: 3px 10px; border-radius: 12px;
}

/* Packing list */
.pack-item {
    display: flex; align-items: center; padding: 10px 14px;
    border-bottom: 1px solid #f0f0f0; gap: 12px;
}
.pack-item:last-child { border-bottom: none; }
.pack-item .item-name { flex: 3; font-size: 14px; }
.pack-item .item-qty {
    flex: 0; font-size: 16px; font-weight: 700; color: #1a1a2e;
    background: #e3f2fd; padding: 4px 14px; border-radius: 8px; white-space: nowrap;
}
.pack-item .item-sku {
    flex: 1; font-size: 12px; font-family: 'SF Mono', monospace;
    color: #666; background: #f5f5f5; padding: 4px 10px; border-radius: 6px;
}

/* Stock table enhancements */
.stock-critical { color: #d32f2f; font-weight: 700; }
.stock-low { color: #e65100; font-weight: 600; }
.stock-ok { color: #2e7d32; }

/* Alert banner */
.alert-banner {
    background: linear-gradient(135deg, #d32f2f, #b71c1c);
    color: white; padding: 14px 24px; border-radius: 10px;
    font-size: 16px; font-weight: 600; text-align: center;
    margin-bottom: 16px; animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.85; }
}

/* Search */
.search-result {
    background: #fafafa; border-radius: 10px; padding: 16px;
    margin: 8px 0; border: 1px solid #eee;
}

/* Section headers */
.section-header {
    font-size: 20px; font-weight: 700; color: #1a1a2e;
    margin: 24px 0 12px 0; display: flex; align-items: center; gap: 8px;
}

/* Note badge */
.note-badge {
    background: #fff3e0; border: 1px solid #ffe0b2; border-radius: 8px;
    padding: 8px 14px; margin-top: 8px; font-size: 13px; color: #e65100;
}

/* Donut center */
.donut-center {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    font-size: 32px; font-weight: 800; color: #1a1a2e;
}

/* Toolbar */
.toolbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 0; margin-bottom: 8px;
}
</style>
"""


def render_kpi_row(df):
    if not len(df):
        return

    total_value = df["total"].sum()
    avg_wait = df["days_waiting"].mean()
    oldest = df["days_waiting"].max()
    total_items = int(df["item_count"].sum())
    late_mask = df["priority"].isin(["CRITICAL", "LATE"])
    late_value = df[late_mask]["total"].sum()
    late_pct = (len(df[late_mask]) / len(df) * 100) if len(df) else 0
    unique_skus = set()
    for _, row in df.iterrows():
        for item in row["items"]:
            unique_skus.add(item["sku"])
    avg_items_per_order = df["item_count"].mean()
    shipping_total = df["shipping_cost"].sum()

    st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
    r1c1, r1c2, r1c3, r1c4, r1c5, r1c6 = st.columns(6)
    with r1c1:
        st.markdown(f"""<div class="priority-card" style="background:#e3f2fd; border:1px solid #90caf920; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#1565c0;">${total_value:,.0f}</div>
            <div style="font-size:11px; color:#1565c0; font-weight:600;">PENDING VALUE</div>
        </div>""", unsafe_allow_html=True)
    with r1c2:
        color = "#d32f2f" if avg_wait >= 5 else "#e65100" if avg_wait >= 3 else "#2e7d32"
        st.markdown(f"""<div class="priority-card" style="background:#f3e5f5; border:1px solid #ce93d820; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:{color};">{avg_wait:.1f}d</div>
            <div style="font-size:11px; color:#7b1fa2; font-weight:600;">AVG WAIT TIME</div>
        </div>""", unsafe_allow_html=True)
    with r1c3:
        st.markdown(f"""<div class="priority-card" style="background:#fce4ec; border:1px solid #f4849920; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#c62828;">{oldest}d</div>
            <div style="font-size:11px; color:#c62828; font-weight:600;">OLDEST ORDER</div>
        </div>""", unsafe_allow_html=True)
    with r1c4:
        st.markdown(f"""<div class="priority-card" style="background:#fff3e0; border:1px solid #ffcc8020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#e65100;">${late_value:,.0f}</div>
            <div style="font-size:11px; color:#e65100; font-weight:600;">LATE ORDER VALUE</div>
        </div>""", unsafe_allow_html=True)
    with r1c5:
        color = "#d32f2f" if late_pct > 40 else "#e65100" if late_pct > 20 else "#2e7d32"
        st.markdown(f"""<div class="priority-card" style="background:#e8f5e9; border:1px solid #a5d6a720; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:{color};">{late_pct:.0f}%</div>
            <div style="font-size:11px; color:#2e7d32; font-weight:600;">LATE RATE</div>
        </div>""", unsafe_allow_html=True)
    with r1c6:
        st.markdown(f"""<div class="priority-card" style="background:#e0f2f1; border:1px solid #80cbc420; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#00695c;">{len(unique_skus)}</div>
            <div style="font-size:11px; color:#00695c; font-weight:600;">UNIQUE SKUS</div>
        </div>""", unsafe_allow_html=True)

    # Second KPI row
    r2c1, r2c2, r2c3, r2c4, r2c5, r2c6 = st.columns(6)
    with r2c1:
        st.markdown(f"""<div class="priority-card" style="background:#f5f5f5; border:1px solid #e0e0e020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#424242;">{total_items}</div>
            <div style="font-size:11px; color:#616161; font-weight:600;">TOTAL ITEMS</div>
        </div>""", unsafe_allow_html=True)
    with r2c2:
        st.markdown(f"""<div class="priority-card" style="background:#f5f5f5; border:1px solid #e0e0e020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#424242;">{avg_items_per_order:.1f}</div>
            <div style="font-size:11px; color:#616161; font-weight:600;">AVG ITEMS/ORDER</div>
        </div>""", unsafe_allow_html=True)
    with r2c3:
        avg_value = total_value / len(df) if len(df) else 0
        st.markdown(f"""<div class="priority-card" style="background:#f5f5f5; border:1px solid #e0e0e020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#424242;">${avg_value:,.0f}</div>
            <div style="font-size:11px; color:#616161; font-weight:600;">AVG ORDER VALUE</div>
        </div>""", unsafe_allow_html=True)
    with r2c4:
        st.markdown(f"""<div class="priority-card" style="background:#f5f5f5; border:1px solid #e0e0e020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#424242;">${shipping_total:,.0f}</div>
            <div style="font-size:11px; color:#616161; font-weight:600;">SHIPPING COSTS</div>
        </div>""", unsafe_allow_html=True)
    with r2c5:
        countries = df["country"].nunique()
        st.markdown(f"""<div class="priority-card" style="background:#f5f5f5; border:1px solid #e0e0e020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#424242;">{countries}</div>
            <div style="font-size:11px; color:#616161; font-weight:600;">COUNTRIES</div>
        </div>""", unsafe_allow_html=True)
    with r2c6:
        states = df[df["country"] == "US"]["state"].nunique()
        st.markdown(f"""<div class="priority-card" style="background:#f5f5f5; border:1px solid #e0e0e020; padding:14px;">
            <div style="font-size:28px; font-weight:800; color:#424242;">{states}</div>
            <div style="font-size:11px; color:#616161; font-weight:600;">US STATES</div>
        </div>""", unsafe_allow_html=True)


def render_priority_cards(df):
    cols = st.columns(5)
    for i, (key, info) in enumerate(PRIORITY_MAP.items()):
        count = len(df[df["priority"] == key]) if len(df) else 0
        with cols[i]:
            st.markdown(f"""
            <div class="priority-card" style="background: {info['bg']}; border: 2px solid {info['color']}20;">
                <div class="number" style="color: {info['color']};">{count}</div>
                <div class="label" style="color: {info['color']};">{info['emoji']} {info['label']}<br>
                <span style="font-weight:400; font-size:11px; opacity:0.7;">{info['desc']}</span></div>
            </div>""", unsafe_allow_html=True)
    with cols[4]:
        total = len(df) if len(df) else 0
        total_items = int(df["item_count"].sum()) if len(df) else 0
        st.markdown(f"""
        <div class="priority-card" style="background: #e8eaf6; border: 2px solid #3f51b520;">
            <div class="number" style="color: #283593;">{total}</div>
            <div class="label" style="color: #283593;">TOTAL ORDERS<br>
            <span style="font-weight:400; font-size:11px; opacity:0.7;">{total_items} items</span></div>
        </div>""", unsafe_allow_html=True)


def render_order_card(row):
    p = PRIORITY_MAP[row["priority"]]
    st.markdown(f"""
    <div class="order-card" style="border-left-color: {p['color']}; background: {p['bg']}40;">
        <div style="flex: 2;">
            <div class="order-id">{p['emoji']} {row['order']}</div>
            <div class="order-meta">{row['customer']} &middot; {row['location']}</div>
        </div>
        <div class="days-badge" style="background: {p['color']}18; color: {p['color']};">
            {row['days_waiting']}d
        </div>
        <div style="text-align: right;">
            <div style="font-size: 16px; font-weight: 600;">${row['total']:,.2f}</div>
            <div class="items-count">{row['item_count']} item{'s' if row['item_count'] != 1 else ''}</div>
        </div>
    </div>""", unsafe_allow_html=True)


def render_packing_list(row):
    html = '<div style="background: #fafafa; border-radius: 8px; margin: 4px 0 16px 0; overflow: hidden;">'
    html += '<div style="background: #e8eaf6; padding: 8px 14px; font-size: 12px; font-weight: 600; color: #283593;">PACKING LIST</div>'
    for item in row["items"]:
        html += f"""
        <div class="pack-item">
            <span class="item-name">{item['title']}</span>
            <span class="item-qty">x{item['qty']}</span>
            <span class="item-sku">{item['sku']}</span>
        </div>"""
    if row["note"]:
        html += f'<div class="note-badge">📝 {row["note"]}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_fulfillment_chart(df):
    if not len(df):
        return
    by_day = df.groupby(["date_str", "priority"]).size().reset_index(name="count")
    color_map = {k: v["color"] for k, v in PRIORITY_MAP.items()}
    fig = px.bar(by_day, x="date_str", y="count", color="priority",
                 color_discrete_map=color_map, barmode="stack",
                 labels={"date_str": "", "count": "Orders", "priority": ""})
    fig.update_layout(
        height=220, margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------- Main ----------

def main():
    st.set_page_config(page_title="Lucyd Packing Station", page_icon="📦", layout="wide")
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    # Header
    header_left, header_right = st.columns([5, 1])
    with header_left:
        st.markdown('<h1 style="margin:0; font-size:32px;">📦 Lucyd Packing Station</h1>', unsafe_allow_html=True)
        st.caption(f"Live data from Shopify &middot; Updated {datetime.now().strftime('%I:%M %p')}")
    with header_right:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # Load data
    with st.spinner("Loading..."):
        orders = fetch_unfulfilled_orders()
        inventory = fetch_inventory()

    df = process_orders(orders)
    inv_df = process_inventory(inventory)

    if len(df) == 0:
        st.markdown("""
        <div style="text-align:center; padding: 80px 20px;">
            <div style="font-size: 64px;">🎉</div>
            <h2 style="color: #2e7d32;">All caught up!</h2>
            <p style="color: #666; font-size: 18px;">No unfulfilled orders. Everything has been shipped.</p>
        </div>""", unsafe_allow_html=True)
        return

    # Critical alert banner
    critical = df[df["priority"] == "CRITICAL"]
    if len(critical):
        st.markdown(f"""
        <div class="alert-banner">
            ⚠️ {len(critical)} CRITICAL ORDER{'S' if len(critical) != 1 else ''} — waiting 10+ days to ship!
        </div>""", unsafe_allow_html=True)

    # Priority cards
    render_priority_cards(df)
    st.markdown("<br>", unsafe_allow_html=True)

    # KPI row
    render_kpi_row(df)
    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs
    tab_queue, tab_stock, tab_region, tab_overview, tab_search = st.tabs([
        "📋 Packing Queue", "📊 Inventory & Stock", "🌎 Regional", "📈 Overview", "🔍 Search"
    ])

    # ==================== TAB: PACKING QUEUE ====================
    with tab_queue:
        # Filters row
        fcol1, fcol2 = st.columns([3, 1])
        with fcol1:
            show_priority = st.multiselect(
                "Filter by priority",
                ["CRITICAL", "LATE", "SOON", "NORMAL"],
                default=["CRITICAL", "LATE", "SOON", "NORMAL"],
                label_visibility="collapsed",
            )
        with fcol2:
            sort_by = st.selectbox(
                "Sort", ["Priority (urgent first)", "Oldest first", "Newest first", "Highest value"],
                label_visibility="collapsed",
            )

        filtered = df[df["priority"].isin(show_priority)].copy()
        if sort_by == "Oldest first":
            filtered = filtered.sort_values("created")
        elif sort_by == "Newest first":
            filtered = filtered.sort_values("created", ascending=False)
        elif sort_by == "Highest value":
            filtered = filtered.sort_values("total", ascending=False)

        st.markdown(f'<div class="section-header">📋 {len(filtered)} Orders to Pack</div>', unsafe_allow_html=True)

        for idx, (_, row) in enumerate(filtered.iterrows()):
            render_order_card(row)
            with st.expander(f"View packing list — {row['order']}", expanded=False):
                render_packing_list(row)

    # ==================== TAB: INVENTORY ====================
    with tab_stock:
        if not len(inv_df):
            st.warning("Could not load inventory data.")
        else:
            out_of_stock = inv_df[inv_df["stock"] <= 0]
            low_stock = inv_df[(inv_df["stock"] > 0) & (inv_df["stock"] <= LOW_STOCK_THRESHOLD)]

            # SKU demand from pending orders
            sku_demand = {}
            for _, row in df.iterrows():
                for item in row["items"]:
                    sku = item["sku"]
                    if sku and sku != "N/A":
                        sku_demand[sku] = sku_demand.get(sku, 0) + item["qty"]

            # Summary cards
            scol1, scol2, scol3 = st.columns(3)
            with scol1:
                st.markdown(f"""
                <div class="priority-card" style="background: #ffebee; border: 2px solid #d32f2f20;">
                    <div class="number" style="color: #d32f2f;">{len(out_of_stock)}</div>
                    <div class="label" style="color: #d32f2f;">⛔ OUT OF STOCK</div>
                </div>""", unsafe_allow_html=True)
            with scol2:
                st.markdown(f"""
                <div class="priority-card" style="background: #fff3e0; border: 2px solid #e6510020;">
                    <div class="number" style="color: #e65100;">{len(low_stock)}</div>
                    <div class="label" style="color: #e65100;">⚠️ LOW STOCK (&lt;{LOW_STOCK_THRESHOLD})</div>
                </div>""", unsafe_allow_html=True)
            with scol3:
                cannot_fulfill = sum(
                    1 for sku, needed in sku_demand.items()
                    if inv_df[inv_df["sku"] == sku]["stock"].sum() < needed
                )
                st.markdown(f"""
                <div class="priority-card" style="background: {'#ffebee' if cannot_fulfill else '#e8f5e9'}; border: 2px solid {'#d32f2f' if cannot_fulfill else '#2e7d32'}20;">
                    <div class="number" style="color: {'#d32f2f' if cannot_fulfill else '#2e7d32'};">{cannot_fulfill}</div>
                    <div class="label" style="color: {'#d32f2f' if cannot_fulfill else '#2e7d32'};">{'❌' if cannot_fulfill else '✅'} CAN'T FULFILL</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Stock vs Demand table (most actionable)
            st.markdown('<div class="section-header">📦 Stock vs Pending Orders</div>', unsafe_allow_html=True)
            if sku_demand:
                demand_rows = []
                for sku, needed in sorted(sku_demand.items(), key=lambda x: -x[1]):
                    stock_row = inv_df[inv_df["sku"] == sku]
                    available = int(stock_row["stock"].sum()) if len(stock_row) else 0
                    product_name = stock_row["product"].iloc[0] if len(stock_row) else "Unknown"
                    shortage = max(0, needed - available)
                    demand_rows.append({
                        "Product": product_name,
                        "SKU": sku,
                        "Needed": needed,
                        "In Stock": available,
                        "Shortage": shortage,
                        "Status": "❌ SHORTAGE" if shortage > 0 else "✅ OK",
                    })
                demand_df = pd.DataFrame(demand_rows).sort_values("Shortage", ascending=False)
                st.dataframe(
                    demand_df, use_container_width=True, height=400, hide_index=True,
                    column_config={
                        "Shortage": st.column_config.NumberColumn(format="%d"),
                        "Needed": st.column_config.NumberColumn(format="%d"),
                        "In Stock": st.column_config.NumberColumn(format="%d"),
                    },
                )

            st.divider()

            # Out of stock
            st.markdown('<div class="section-header">⛔ Out of Stock Items</div>', unsafe_allow_html=True)
            if len(out_of_stock):
                pending_skus = set()
                for _, row in df.iterrows():
                    for item in row["items"]:
                        pending_skus.add(item["sku"])
                oos = out_of_stock[["product", "variant", "sku", "stock"]].copy()
                oos["Pending Orders"] = oos["sku"].isin(pending_skus).map({True: "⚠️ YES", False: "—"})
                oos.columns = ["Product", "Variant", "SKU", "Stock", "Pending Orders"]
                st.dataframe(oos, use_container_width=True, height=350, hide_index=True)
            else:
                st.success("No items are out of stock!")

            st.divider()

            # Low stock
            st.markdown(f'<div class="section-header">⚠️ Low Stock (1-{LOW_STOCK_THRESHOLD} units)</div>', unsafe_allow_html=True)
            if len(low_stock):
                low_display = low_stock[["product", "variant", "sku", "stock"]].copy()
                low_display.columns = ["Product", "Variant", "SKU", "Stock"]
                low_display = low_display.sort_values("Stock")
                st.dataframe(
                    low_display, use_container_width=True, height=350, hide_index=True,
                    column_config={
                        "Stock": st.column_config.ProgressColumn(min_value=0, max_value=LOW_STOCK_THRESHOLD, format="%d"),
                    },
                )
            else:
                st.success("No low stock items!")

    # ==================== TAB: REGIONAL ====================
    with tab_region:
        if not len(df):
            st.info("No data to display.")
        else:
            # Country breakdown
            rcol1, rcol2 = st.columns(2)

            with rcol1:
                st.markdown('<div class="section-header">🌎 Orders by Country</div>', unsafe_allow_html=True)
                country_data = df.groupby("country").agg(
                    orders=("order", "count"),
                    value=("total", "sum"),
                    avg_wait=("days_waiting", "mean"),
                ).sort_values("orders", ascending=False).reset_index()
                country_data.columns = ["Country", "Orders", "Value", "Avg Wait (d)"]
                country_data["Value"] = country_data["Value"].apply(lambda x: f"${x:,.2f}")
                country_data["Avg Wait (d)"] = country_data["Avg Wait (d)"].apply(lambda x: f"{x:.1f}")
                st.dataframe(country_data, use_container_width=True, hide_index=True, height=300)

            with rcol2:
                st.markdown('<div class="section-header">📊 Order Value by Country</div>', unsafe_allow_html=True)
                country_chart = df.groupby("country")["total"].sum().sort_values(ascending=True).reset_index()
                country_chart.columns = ["Country", "Value"]
                fig = px.bar(country_chart, x="Value", y="Country", orientation="h",
                             color_discrete_sequence=["#3f51b5"],
                             labels={"Value": "Pending Value ($)", "Country": ""})
                fig.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10),
                                  plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # US State breakdown
            us_df = df[df["country"] == "US"]
            if len(us_df):
                st.markdown(f'<div class="section-header">🇺🇸 US Orders by State ({len(us_df)} orders)</div>', unsafe_allow_html=True)

                scol1, scol2 = st.columns(2)

                with scol1:
                    # Map
                    state_map = us_df.groupby("state").agg(
                        orders=("order", "count"),
                        value=("total", "sum"),
                    ).reset_index()
                    state_map.columns = ["State", "Orders", "Value"]
                    fig = px.choropleth(
                        state_map, locations="State", locationmode="USA-states",
                        color="Orders", scope="usa",
                        color_continuous_scale="Blues",
                        labels={"Orders": "Pending Orders"},
                        hover_data={"Value": ":$,.2f"},
                    )
                    fig.update_layout(
                        height=400, margin=dict(t=10, b=10, l=10, r=10),
                        geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)"),
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with scol2:
                    # State table
                    state_data = us_df.groupby("state").agg(
                        orders=("order", "count"),
                        value=("total", "sum"),
                        avg_wait=("days_waiting", "mean"),
                        late=("priority", lambda x: sum(x.isin(["CRITICAL", "LATE"]))),
                    ).sort_values("orders", ascending=False).reset_index()
                    state_data.columns = ["State", "Orders", "Value", "Avg Wait (d)", "Late"]
                    state_data["Value"] = state_data["Value"].apply(lambda x: f"${x:,.2f}")
                    state_data["Avg Wait (d)"] = state_data["Avg Wait (d)"].apply(lambda x: f"{x:.1f}")
                    st.dataframe(state_data, use_container_width=True, hide_index=True, height=400)

                st.divider()

                # Top states bar chart
                st.markdown('<div class="section-header">📊 Top States by Volume</div>', unsafe_allow_html=True)
                top_states = us_df.groupby("state").agg(
                    orders=("order", "count"),
                    value=("total", "sum"),
                    late=("priority", lambda x: sum(x.isin(["CRITICAL", "LATE"]))),
                ).sort_values("orders", ascending=False).head(15).reset_index()
                top_states.columns = ["State", "Orders", "Value", "Late"]
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=top_states["State"], y=top_states["Orders"] - top_states["Late"],
                    name="On Time", marker_color="#4CAF50",
                ))
                fig.add_trace(go.Bar(
                    x=top_states["State"], y=top_states["Late"],
                    name="Late", marker_color="#f44336",
                ))
                fig.update_layout(
                    barmode="stack", height=300, margin=dict(t=10, b=10),
                    plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", yanchor="bottom", y=1.02),
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f0f0", title="Orders"),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No US orders in the current queue.")

            st.divider()

            # Shipping method breakdown
            st.markdown('<div class="section-header">🚚 Shipping Methods</div>', unsafe_allow_html=True)
            ship_col1, ship_col2 = st.columns(2)
            with ship_col1:
                ship_data = df.groupby("shipping_method").agg(
                    orders=("order", "count"),
                    value=("total", "sum"),
                    avg_wait=("days_waiting", "mean"),
                ).sort_values("orders", ascending=False).reset_index()
                ship_data.columns = ["Method", "Orders", "Value", "Avg Wait (d)"]
                ship_data["Value"] = ship_data["Value"].apply(lambda x: f"${x:,.2f}")
                ship_data["Avg Wait (d)"] = ship_data["Avg Wait (d)"].apply(lambda x: f"{x:.1f}")
                st.dataframe(ship_data, use_container_width=True, hide_index=True)
            with ship_col2:
                ship_chart = df["shipping_method"].value_counts().reset_index()
                ship_chart.columns = ["Method", "Count"]
                fig = px.pie(ship_chart, values="Count", names="Method", hole=0.4,
                             color_discrete_sequence=px.colors.qualitative.Set2)
                fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

            # Regional priority heatmap
            st.markdown('<div class="section-header">🔥 Late Orders by Region</div>', unsafe_allow_html=True)
            late_df = df[df["priority"].isin(["CRITICAL", "LATE"])]
            if len(late_df):
                late_by_state = late_df.groupby("state").agg(
                    late_orders=("order", "count"),
                    total_value=("total", "sum"),
                    max_wait=("days_waiting", "max"),
                ).sort_values("late_orders", ascending=False).head(20).reset_index()
                late_by_state.columns = ["State/Region", "Late Orders", "Value at Risk", "Oldest (d)"]
                late_by_state["Value at Risk"] = late_by_state["Value at Risk"].apply(lambda x: f"${x:,.2f}")
                st.dataframe(late_by_state, use_container_width=True, hide_index=True)
            else:
                st.success("No late orders!")

    # ==================== TAB: OVERVIEW ====================
    with tab_overview:
        ocol1, ocol2 = st.columns(2)

        with ocol1:
            st.markdown('<div class="section-header">📊 Orders by Priority</div>', unsafe_allow_html=True)
            priority_counts = df["priority"].value_counts().reset_index()
            priority_counts.columns = ["Priority", "Count"]
            color_map = {k: v["color"] for k, v in PRIORITY_MAP.items()}
            fig = px.pie(priority_counts, values="Count", names="Priority",
                         color="Priority", color_discrete_map=color_map, hole=0.5)
            fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
            fig.update_traces(textposition="outside", textinfo="label+value")
            st.plotly_chart(fig, use_container_width=True)

        with ocol2:
            st.markdown('<div class="section-header">📅 Orders by Date</div>', unsafe_allow_html=True)
            render_fulfillment_chart(df)

        st.divider()

        # Aging breakdown
        st.markdown('<div class="section-header">⏱️ Order Aging</div>', unsafe_allow_html=True)
        if len(df):
            bins = [0, 1, 2, 3, 5, 7, 10, 15, 30, 999]
            labels = ["Today", "1d", "2d", "3-4d", "5-6d", "7-9d", "10-14d", "15-29d", "30d+"]
            df["age_bucket"] = pd.cut(df["days_waiting"], bins=bins, labels=labels, right=False)
            age_counts = df["age_bucket"].value_counts().sort_index().reset_index()
            age_counts.columns = ["Age", "Orders"]
            colors = ["#4CAF50", "#66BB6A", "#8BC34A", "#FDD835", "#FFB300", "#FF9800", "#FF5722", "#D32F2F", "#B71C1C"]
            fig = px.bar(age_counts, x="Age", y="Orders", color="Age",
                         color_discrete_sequence=colors)
            fig.update_layout(
                height=250, margin=dict(t=10, b=10),
                showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Top items waiting
        st.markdown('<div class="section-header">📦 Most Ordered Items (Pending)</div>', unsafe_allow_html=True)
        item_counts = {}
        for _, row in df.iterrows():
            for item in row["items"]:
                key = f"{item['title']} ({item['sku']})"
                item_counts[key] = item_counts.get(key, 0) + item["qty"]
        if item_counts:
            top_items = sorted(item_counts.items(), key=lambda x: -x[1])[:15]
            top_df = pd.DataFrame(top_items, columns=["Product (SKU)", "Units Pending"])
            fig = px.bar(top_df, x="Units Pending", y="Product (SKU)", orientation="h",
                         color_discrete_sequence=["#3f51b5"])
            fig.update_layout(
                height=max(250, len(top_df) * 30), margin=dict(t=10, b=10, l=10, r=10),
                plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ==================== TAB: SEARCH ====================
    with tab_search:
        st.markdown('<div class="section-header">🔍 Find an Order</div>', unsafe_allow_html=True)
        search = st.text_input("Search by order #, customer name, or SKU",
                               placeholder="e.g. LU31696 or John Smith or LCD008-10")
        if search:
            s = search.lower()
            results = df[
                df["order"].str.lower().str.contains(s) |
                df["customer"].str.lower().str.contains(s) |
                df["skus_str"].str.lower().str.contains(s)
            ]
            if len(results):
                st.markdown(f"**{len(results)} orders found**")
                for _, row in results.iterrows():
                    render_order_card(row)
                    render_packing_list(row)
            else:
                st.info("No matching orders found. Try a different search term.")
        else:
            st.caption("Start typing to search across all pending orders.")

    # ==================== SIDEBAR ====================
    st.sidebar.markdown("### 📦 Packing Station")
    st.sidebar.caption(f"Store: {STORE}")
    st.sidebar.caption(f"Last updated: {datetime.now().strftime('%I:%M:%S %p')}")
    st.sidebar.caption("Data cached 2 min. Click Refresh for latest.")

    st.sidebar.divider()
    st.sidebar.markdown("### ⬇️ Export")
    if len(df):
        today = datetime.now().strftime("%Y-%m-%d")
        queue_csv = df[["order", "date_str", "days_waiting", "priority", "customer",
                        "location", "state", "country", "shipping_method", "total",
                        "shipping_cost", "items_str", "skus_str", "note"]].copy()
        queue_csv.columns = ["Order", "Date", "Days Waiting", "Priority", "Customer",
                             "Location", "State", "Country", "Shipping Method", "Total",
                             "Shipping Cost", "Items", "SKUs", "Note"]
        st.sidebar.download_button("📋 Packing Queue CSV", queue_csv.to_csv(index=False),
                                   f"packing_queue_{today}.csv", "text/csv", use_container_width=True)

    if len(inv_df):
        st.sidebar.download_button("📊 Full Inventory CSV", inv_df.to_csv(index=False),
                                   f"inventory_{today}.csv", "text/csv", use_container_width=True)

    st.sidebar.divider()
    st.sidebar.markdown("### ⚙️ Settings")
    st.sidebar.caption(f"Late threshold: {LATE_THRESHOLD_DAYS} days")
    st.sidebar.caption(f"Low stock alert: <{LOW_STOCK_THRESHOLD} units")


if __name__ == "__main__":
    main()

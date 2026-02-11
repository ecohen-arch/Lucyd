"""
Shopify OAuth flow to obtain an Admin API access token.

1. Starts a local server to catch the OAuth callback
2. Opens browser to Shopify authorization URL
3. Exchanges the auth code for an access token
4. Saves the token to .env
"""

import os
import re
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

load_dotenv()

STORE = os.getenv("SHOPIFY_STORE")
CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3456/callback"
SCOPES = "read_orders,read_products,read_all_orders"

access_token = None


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global access_token
        parsed = urlparse(self.path)

        if parsed.path == "/callback":
            params = parse_qs(parsed.query)
            code = params.get("code", [None])[0]

            if code:
                # Exchange code for access token
                token_url = f"https://{STORE}/admin/oauth/access_token"
                resp = requests.post(token_url, json={
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                })

                if resp.status_code == 200:
                    data = resp.json()
                    access_token = data["access_token"]

                    # Save to .env
                    env_path = os.path.join(os.path.dirname(__file__), ".env")
                    with open(env_path, "r") as f:
                        content = f.read()
                    content = re.sub(
                        r"SHOPIFY_ACCESS_TOKEN=.*",
                        f"SHOPIFY_ACCESS_TOKEN={access_token}",
                        content,
                    )
                    with open(env_path, "w") as f:
                        f.write(content)

                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"""
                        <html><body style="font-family:sans-serif;text-align:center;padding:60px">
                        <h1>Success!</h1>
                        <p>Access token saved to .env file. You can close this tab.</p>
                        </body></html>
                    """)
                    print(f"\nAccess token obtained and saved to .env")
                    print(f"Token prefix: {access_token[:12]}...")
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(f"Error: {resp.text}".encode())
                    print(f"\nError exchanging code: {resp.status_code} {resp.text}")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No authorization code received")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress default logging


def main():
    if not all([STORE, CLIENT_ID, CLIENT_SECRET]):
        print("ERROR: Set SHOPIFY_STORE, SHOPIFY_CLIENT_ID, and SHOPIFY_CLIENT_SECRET in .env")
        raise SystemExit(1)

    auth_url = (
        f"https://{STORE}/admin/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&scope={SCOPES}"
        f"&redirect_uri={REDIRECT_URI}"
    )

    print(f"Starting local server on http://localhost:3456 ...")
    print(f"Opening browser for Shopify authorization...\n")
    print(f"If the browser doesn't open, visit:\n{auth_url}\n")

    server = HTTPServer(("localhost", 3456), OAuthHandler)
    webbrowser.open(auth_url)

    # Handle one request (the callback), then stop
    server.handle_request()
    server.server_close()

    if access_token:
        print("\nDone! You can now run: python3 shopify_orders.py")
    else:
        print("\nFailed to obtain access token.")


if __name__ == "__main__":
    main()

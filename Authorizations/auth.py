import requests
import os
from google.cloud import firestore

# Config
CLIENT_ID = "gmxnZHTUvGTO97SgKmrRE7Ob_cBrcai4"  # Your client ID

# Legacy paths kept only as constants (no writes will happen)
REFRESH_TOKEN_FILE = "connectors/deliverect/Auth/RefreshToken.txt"
ACCESS_TOKEN_FILE = "connectors/deliverect/Auth/Token.txt"
BEARER_TOKEN_FILE = "connectors/deliverect/Auth/BearerToken.txt"

# Firestore config
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "trofi-data")
FS_COLLECTION = "deliverect_tokens"
FS_DOCUMENT  = "refresh_and_access_token"

def _fs_client():
    return firestore.Client(project=GCP_PROJECT_ID)

def _fs_doc():
    return _fs_client().collection(FS_COLLECTION).document(FS_DOCUMENT)


# Load existing refresh token (from Firestore)
def load_refresh_token():
    snap = _fs_doc().get()
    if not snap.exists:
        raise RuntimeError(f"Firestore doc {FS_COLLECTION}/{FS_DOCUMENT} not found.")
    data = snap.to_dict() or {}
    rt = data.get("refresh_token")
    if not rt:
        raise RuntimeError(f"'refresh_token' missing in {FS_COLLECTION}/{FS_DOCUMENT}.")
    return rt.strip()

# Save new refresh token (to Firestore)
def save_refresh_token(new_refresh_token):
    if not new_refresh_token:
        return
    _fs_doc().set({"refresh_token": new_refresh_token}, merge=True)
    print("🔁 Refresh token updated in Firestore.")

# Save Bearer token (to Firestore)
def save_bearer_token(access_token):
    if not access_token:
        return
    _fs_doc().set({"access_token": access_token}, merge=True)
    print("✅ Bearer (access) token saved to Firestore.")

# Load Bearer token (from Firestore)
def load_bearer_token():
    snap = _fs_doc().get()
    if not snap.exists:
        raise RuntimeError(f"Firestore doc {FS_COLLECTION}/{FS_DOCUMENT} not found.")
    data = snap.to_dict() or {}
    at = data.get("access_token")
    if not at:
        raise RuntimeError(f"'access_token' missing in {FS_COLLECTION}/{FS_DOCUMENT}.")
    return at.strip()


# Refresh access token and optionally update refresh token
def refresh_access_token():
    refresh_token = load_refresh_token()
    url = "https://login.deliverect.com/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("🔄 Refreshing access token...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token")

        if access_token:
            save_bearer_token(access_token)

        if new_refresh_token:
            save_refresh_token(new_refresh_token)

    else:
        print(f"❌ Failed to refresh token: {response.status_code}")
        print(response.text)


# Main function to run the refresh
if __name__ == "__main__":
    refresh_access_token()
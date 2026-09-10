"""
Automated GitHub File Uploader for EcoProject AI
This script uploads index.html, README.md, and LICENSE to your GitHub repository using the GitHub REST API.
"""

import os
import base64
import requests

FILES_TO_UPLOAD = ["index.html", "README.md", "LICENSE"]

def upload_file(token, username, repo, filepath, branch="main"):
    filename = os.path.basename(filepath)
    if not os.path.exists(filepath):
        print(f"[-] File {filepath} not found. Skipping.")
        return False

    with open(filepath, "rb") as f:
        content_bytes = f.read()
    
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")
    
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{filename}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if file already exists to get its SHA (for update)
    res = requests.get(url, headers=headers)
    sha = None
    if res.status_code == 200:
        sha = res.json().get("sha")

    payload = {
        "message": f"Upload {filename}",
        "content": content_b64,
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    put_res = requests.put(url, headers=headers, json=payload)
    if put_res.status_code in [200, 201]:
        action = "Updated" if sha else "Created"
        print(f"[+] Successfully {action} {filename} in {username}/{repo} on branch {branch}!")
        return True
    else:
        print(f"[-] Failed to upload {filename}. HTTP {put_res.status_code}: {put_res.text}")
        return False

def main():
    print("=" * 60)
    print("🚀 ECOPROJECT AI - GITHUB AUTOMATED UPLOADER")
    print("=" * 60)
    
    username = input("Enter your GitHub Username: ").strip()
    repo = input("Enter your Repository Name (e.g., ecoproject-ai): ").strip()
    token = input("Enter your GitHub Personal Access Token (classic): ").strip()
    branch = input("Enter branch name (press Enter for 'main'): ").strip() or "main"

    if not username or not repo or not token:
        print("[-] Username, repository name, and token are required.")
        return

    print("\nUploading files...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    success_count = 0

    for fname in FILES_TO_UPLOAD:
        fpath = os.path.join(base_dir, fname)
        if upload_file(token, username, repo, fpath, branch):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"🎉 Done! {success_count}/{len(FILES_TO_UPLOAD)} files uploaded successfully.")
    print(f"🌐 Visit your repo: https://github.com/{username}/{repo}")
    print("=" * 60)

if __name__ == "__main__":
    main()

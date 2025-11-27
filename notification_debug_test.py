#!/usr/bin/env python3
"""
Debug notification creation issue
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "https://role-test-operai.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

def test_notification_flow():
    print("🔍 Debugging Notification Flow")
    
    # Login as HR
    hr_login = {"email": "hr@operai.com", "password": "hr123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=hr_login, headers=HEADERS)
    hr_token = response.json()["access_token"]
    hr_headers = HEADERS.copy()
    hr_headers["Authorization"] = f"Bearer {hr_token}"
    
    # Login as Employee
    emp_login = {"email": "employee@operai.com", "password": "emp123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=emp_login, headers=HEADERS)
    emp_token = response.json()["access_token"]
    emp_headers = HEADERS.copy()
    emp_headers["Authorization"] = f"Bearer {emp_token}"
    
    print("✅ Logged in as HR and Employee")
    
    # Get notifications before announcement
    response = requests.get(f"{BASE_URL}/notifications", headers=emp_headers)
    notifications_before = response.json()
    print(f"📋 Employee notifications before: {len(notifications_before)}")
    
    # HR creates announcement
    announcement_data = {
        "title": "Debug Test Announcement",
        "content": "This is a test announcement to debug notification creation.",
        "target_roles": []  # Empty means all roles
    }
    
    response = requests.post(f"{BASE_URL}/announcements", json=announcement_data, headers=hr_headers)
    if response.status_code == 200:
        announcement = response.json()
        print(f"✅ HR created announcement: {announcement['title']}")
        print(f"   ID: {announcement['id']}")
        print(f"   Target roles: {announcement['target_roles']}")
    else:
        print(f"❌ Failed to create announcement: {response.status_code} - {response.text}")
        return
    
    # Wait for notification to be created
    print("⏳ Waiting 3 seconds for notification creation...")
    time.sleep(3)
    
    # Get notifications after announcement
    response = requests.get(f"{BASE_URL}/notifications", headers=emp_headers)
    notifications_after = response.json()
    print(f"📋 Employee notifications after: {len(notifications_after)}")
    
    # Check for announcement notification
    announcement_notifications = [
        n for n in notifications_after 
        if n.get("type") == "announcement" and "Debug Test Announcement" in n.get("title", "")
    ]
    
    if announcement_notifications:
        print("✅ Found announcement notification!")
        notif = announcement_notifications[0]
        print(f"   Title: {notif['title']}")
        print(f"   Type: {notif['type']}")
        print(f"   User ID: {notif.get('user_id')}")
        print(f"   Target Roles: {notif.get('target_roles')}")
    else:
        print("❌ No announcement notification found")
        print("All notifications:")
        for i, notif in enumerate(notifications_after):
            print(f"   {i+1}. {notif.get('title')} (type: {notif.get('type')})")
    
    # Check all notifications in database (as HR)
    response = requests.get(f"{BASE_URL}/notifications", headers=hr_headers)
    hr_notifications = response.json()
    print(f"📋 HR notifications: {len(hr_notifications)}")
    
    # Look for any announcement notifications
    all_announcement_notifs = [
        n for n in hr_notifications 
        if n.get("type") == "announcement"
    ]
    print(f"📢 Total announcement notifications in system: {len(all_announcement_notifs)}")
    
    for notif in all_announcement_notifs:
        print(f"   - {notif.get('title')} | User: {notif.get('user_id')} | Roles: {notif.get('target_roles')}")

if __name__ == "__main__":
    test_notification_flow()
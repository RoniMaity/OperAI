#!/usr/bin/env python3
"""
OperAI Local Demo Data Seeding Script
Seeds demo data into THIS workspace's MongoDB instance
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
from passlib.context import CryptContext
import uuid
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'operai_db')

print(f"Connecting to: {MONGO_URL}")
print(f"Database: {DB_NAME}")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DEMO_PASSWORD = "Password123!"

# Demo users
DEMO_USERS = [
    {
        "email": "admin@operai.demo",
        "name": "Admin User",
        "role": "admin",
        "department_id": None
    },
    {
        "email": "hr@operai.demo",
        "name": "Sarah HR Manager",
        "role": "hr",
        "department_id": None
    },
    {
        "email": "lead@operai.demo",
        "name": "John Team Lead",
        "role": "team_lead",
        "department_id": None
    },
    {
        "email": "emp1@operai.demo",
        "name": "Alice Employee",
        "role": "employee",
        "department_id": None
    },
    {
        "email": "intern@operai.demo",
        "name": "Charlie Intern",
        "role": "intern",
        "department_id": None
    }
]


def clear_collections(db):
    """Clear demo data collections"""
    print("\n=== Clearing existing demo data ===")
    
    collections = [
        "users", "tasks", "leaves", "attendance",
        "announcements", "ai_messages", "deadline_requests", "notifications"
    ]
    
    for collection_name in collections:
        count = db[collection_name].count_documents({})
        if count > 0:
            db[collection_name].delete_many({})
            print(f"✓ Cleared {count} documents from '{collection_name}'")
        else:
            print(f"  '{collection_name}' was already empty")


def seed_users(db):
    """Create demo users"""
    print("\n=== Creating demo users ===")
    
    hashed_password = pwd_context.hash(DEMO_PASSWORD)
    user_ids = {}
    
    for user_data in DEMO_USERS:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "email": user_data["email"],
            "name": user_data["name"],
            "role": user_data["role"],
            "department_id": user_data["department_id"],
            "password": hashed_password,
            "is_active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        db.users.insert_one(user)
        user_ids[user_data["role"] + "_" + user_data["email"].split("@")[0]] = user_id
        print(f"✓ Created {user_data['role']:12} - {user_data['name']:20} ({user_data['email']})")
    
    return user_ids


def seed_tasks(db, user_ids):
    """Create realistic tasks"""
    print("\n=== Creating demo tasks ===")
    
    lead_id = user_ids["team_lead_lead"]
    emp1_id = user_ids["employee_emp1"]
    intern_id = user_ids["intern_intern"]
    
    today = datetime.now(timezone.utc)
    
    tasks_data = [
        {
            "title": "Complete Q1 Financial Report",
            "description": "Prepare and submit the Q1 financial analysis report",
            "assigned_to": emp1_id,
            "created_by": lead_id,
            "status": "in_progress",
            "priority": "high",
            "progress": 65,
            "deadline": (today + timedelta(days=3)).isoformat(),
            "notes": "Waiting for data from finance"
        },
        {
            "title": "Update Employee Onboarding Documentation",
            "description": "Review and update all onboarding materials",
            "assigned_to": emp1_id,
            "created_by": lead_id,
            "status": "todo",
            "priority": "medium",
            "progress": 0,
            "deadline": (today + timedelta(days=7)).isoformat(),
            "notes": ""
        },
        {
            "title": "Setup Development Environment",
            "description": "Install and configure all development tools",
            "assigned_to": intern_id,
            "created_by": lead_id,
            "status": "completed",
            "priority": "urgent",
            "progress": 100,
            "deadline": (today - timedelta(days=2)).isoformat(),
            "notes": "All tools installed"
        },
        {
            "title": "Write Unit Tests for API Endpoints",
            "description": "Create comprehensive unit tests for REST API",
            "assigned_to": intern_id,
            "created_by": lead_id,
            "status": "in_progress",
            "priority": "medium",
            "progress": 40,
            "deadline": (today + timedelta(days=10)).isoformat(),
            "notes": "Auth endpoints tests completed"
        },
        {
            "title": "Customer Feedback Analysis",
            "description": "Analyze customer feedback from Q4",
            "assigned_to": emp1_id,
            "created_by": lead_id,
            "status": "blocked",
            "priority": "high",
            "progress": 10,
            "deadline": (today + timedelta(days=5)).isoformat(),
            "notes": "Waiting for data export"
        },
        {
            "title": "Database Migration Planning",
            "description": "Plan migration strategy to PostgreSQL",
            "assigned_to": emp1_id,
            "created_by": lead_id,
            "status": "todo",
            "priority": "low",
            "progress": 0,
            "deadline": (today + timedelta(days=21)).isoformat(),
            "notes": ""
        }
    ]
    
    task_ids = []
    for task_data in tasks_data:
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            **task_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        db.tasks.insert_one(task)
        task_ids.append(task_id)
        
        status_emoji = {
            "todo": "📋",
            "in_progress": "🔄",
            "completed": "✅",
            "blocked": "🚫"
        }
        assignee = "emp1" if task_data["assigned_to"] == emp1_id else "intern"
        print(f"{status_emoji[task_data['status']]} {task_data['title'][:45]:45} [{assignee:6}] {task_data['status']:12}")
    
    return task_ids


def seed_attendance(db, user_ids):
    """Create attendance records for past 5 days"""
    print("\n=== Creating attendance records ===")
    
    emp1_id = user_ids["employee_emp1"]
    
    today = datetime.now(timezone.utc)
    count = 0
    
    # Create attendance for past 5 days
    for days_ago in range(5, 0, -1):
        date = today - timedelta(days=days_ago)
        date_str = date.strftime('%Y-%m-%d')
        
        # Alice has perfect attendance
        work_mode = "wfo" if days_ago % 2 == 0 else "wfh"
        attendance_id = str(uuid.uuid4())
        attendance = {
            "id": attendance_id,
            "user_id": emp1_id,
            "date": date_str,
            "work_mode": work_mode,
            "status": "present" if work_mode == "wfo" else "wfh",
            "check_in": date.replace(hour=9, minute=0).isoformat(),
            "check_out": date.replace(hour=18, minute=0).isoformat(),
            "notes": None,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        db.attendance.insert_one(attendance)
        count += 1
    
    print(f"✓ Created {count} attendance records (past 5 days for emp1)")
    print(f"  - Mix of WFO and WFH")
    print(f"  - All check-ins completed")


def seed_leaves(db, user_ids):
    """Create leave applications"""
    print("\n=== Creating leave applications ===")
    
    hr_id = user_ids["hr_hr"]
    emp1_id = user_ids["employee_emp1"]
    intern_id = user_ids["intern_intern"]
    
    today = datetime.now(timezone.utc)
    
    leaves_data = [
        {
            "user_id": emp1_id,
            "leave_type": "casual",
            "start_date": (today + timedelta(days=10)).strftime('%Y-%m-%d'),
            "end_date": (today + timedelta(days=12)).strftime('%Y-%m-%d'),
            "reason": "Family vacation planned",
            "status": "pending",
            "approved_by": None,
            "rejection_reason": None
        },
        {
            "user_id": intern_id,
            "leave_type": "sick",
            "start_date": (today - timedelta(days=2)).strftime('%Y-%m-%d'),
            "end_date": (today - timedelta(days=1)).strftime('%Y-%m-%d'),
            "reason": "Flu and fever",
            "status": "approved",
            "approved_by": hr_id,
            "rejection_reason": None
        },
        {
            "user_id": emp1_id,
            "leave_type": "earned",
            "start_date": (today + timedelta(days=30)).strftime('%Y-%m-%d'),
            "end_date": (today + timedelta(days=34)).strftime('%Y-%m-%d'),
            "reason": "Annual vacation",
            "status": "approved",
            "approved_by": hr_id,
            "rejection_reason": None
        }
    ]
    
    for leave_data in leaves_data:
        leave_id = str(uuid.uuid4())
        leave = {
            "id": leave_id,
            **leave_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        db.leaves.insert_one(leave)
        
        status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
        user = "emp1" if leave_data["user_id"] == emp1_id else "intern"
        print(f"{status_emoji[leave_data['status']]} {leave_data['leave_type']:8} - {leave_data['start_date']} to {leave_data['end_date']} [{user:6}] {leave_data['status']:8}")


def seed_deadline_requests(db, user_ids, task_ids):
    """Create deadline extension request"""
    print("\n=== Creating deadline request ===")
    
    emp1_id = user_ids["employee_emp1"]
    lead_id = user_ids["team_lead_lead"]
    
    today = datetime.now(timezone.utc)
    
    request_id = str(uuid.uuid4())
    request = {
        "id": request_id,
        "task_id": task_ids[0] if len(task_ids) > 0 else str(uuid.uuid4()),
        "requested_by": emp1_id,
        "requested_new_deadline": (today + timedelta(days=7)).strftime('%Y-%m-%d'),
        "reason": "Need additional time for data analysis from finance team",
        "status": "pending",
        "responded_by": None,
        "response_note": None,
        "created_at": (today - timedelta(days=1)).isoformat(),
        "updated_at": None
    }
    db.deadline_requests.insert_one(request)
    print("⏳ Created 1 pending deadline request for Financial Report task")


def seed_announcements(db, user_ids):
    """Create company announcement"""
    print("\n=== Creating announcement ===")
    
    hr_id = user_ids["hr_hr"]
    today = datetime.now(timezone.utc)
    
    announcement_id = str(uuid.uuid4())
    announcement = {
        "id": announcement_id,
        "title": "🎉 Company All-Hands Meeting - Q1 Results",
        "content": "Join us this Friday at 3 PM for our quarterly all-hands meeting. We'll discuss Q1 achievements, upcoming projects, and team recognitions. Attendance is mandatory.",
        "created_by": hr_id,
        "target_roles": [],  # All users
        "created_at": (today - timedelta(days=1)).isoformat()
    }
    db.announcements.insert_one(announcement)
    print("📢 Created 1 company-wide announcement")
    
    return announcement_id


def seed_notifications(db, user_ids):
    """Create notifications"""
    print("\n=== Creating notifications ===")
    
    emp1_id = user_ids["employee_emp1"]
    today = datetime.now(timezone.utc)
    
    notifications_data = [
        {
            "user_id": None,
            "target_roles": [],
            "type": "announcement",
            "title": "🎉 Company All-Hands Meeting - Q1 Results",
            "message": "Join us this Friday at 3 PM for our quarterly all-hands meeting...",
            "related_task_id": None,
            "related_request_id": None,
            "is_read": False
        },
        {
            "user_id": emp1_id,
            "target_roles": [],
            "type": "task_assigned",
            "title": "New task assigned",
            "message": "You have been assigned: 'Complete Q1 Financial Report'",
            "related_task_id": None,
            "related_request_id": None,
            "is_read": False
        },
        {
            "user_id": emp1_id,
            "target_roles": [],
            "type": "deadline_change",
            "title": "Task deadline approaching",
            "message": "'Complete Q1 Financial Report' is due in 3 days",
            "related_task_id": None,
            "related_request_id": None,
            "is_read": True
        }
    ]
    
    count = 0
    for notif_data in notifications_data:
        notif_id = str(uuid.uuid4())
        notification = {
            "id": notif_id,
            **notif_data,
            "metadata": None,
            "created_at": (today - timedelta(hours=12 - count * 4)).isoformat()
        }
        db.notifications.insert_one(notification)
        count += 1
    
    print(f"✓ Created {count} notifications")
    print(f"  - 1 company announcement")
    print(f"  - 2 user-specific notifications")


def print_summary():
    """Print summary"""
    print("\n" + "="*60)
    print("  ✅ Local demo data seeded successfully!")
    print("="*60)
    
    print("\n📋 DEMO ACCOUNTS:")
    print(f"{'Role':<12} {'Email':<25} {'Password'}")
    print("-" * 60)
    
    accounts = [
        ("Admin", "admin@operai.demo", DEMO_PASSWORD),
        ("HR", "hr@operai.demo", DEMO_PASSWORD),
        ("Team Lead", "lead@operai.demo", DEMO_PASSWORD),
        ("Employee", "emp1@operai.demo", DEMO_PASSWORD),
        ("Intern", "intern@operai.demo", DEMO_PASSWORD)
    ]
    
    for role, email, password in accounts:
        print(f"{role:<12} {email:<25} {password}")
    
    print("\n📊 DATA SEEDED:")
    print("  ✓ 5 demo users (all roles)")
    print("  ✓ 6 tasks (assigned to emp1 and intern)")
    print("  ✓ 5 attendance records (past 5 days for emp1)")
    print("  ✓ 3 leave applications (pending + approved)")
    print("  ✓ 1 pending deadline request")
    print("  ✓ 1 company announcement")
    print("  ✓ 3 notifications")
    
    print("\n🚀 READY TO TEST:")
    print("  1. Login as emp1@operai.demo")
    print("  2. Go to AI Assistant")
    print("  3. Try: 'show my tasks'")
    print("  4. Try: 'check my attendance'")
    print("  5. Try: 'summarize my tasks'")
    print("\n" + "="*60 + "\n")


def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("  🌱 OperAI Local Demo Data Seeding")
    print("="*60)
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URL)
        db = client[DB_NAME]
        
        # Verify connection
        client.admin.command('ping')
        print("✓ MongoDB connection successful\n")
        
        # Execute seeding
        clear_collections(db)
        user_ids = seed_users(db)
        task_ids = seed_tasks(db, user_ids)
        seed_attendance(db, user_ids)
        seed_leaves(db, user_ids)
        seed_deadline_requests(db, user_ids, task_ids)
        seed_announcements(db, user_ids)
        seed_notifications(db, user_ids)
        
        # Print summary
        print_summary()
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

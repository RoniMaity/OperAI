#!/usr/bin/env python3
"""
OperAI Demo Data Seeding Script

This script populates the database with realistic demo data for all roles.
Run with: python seed_demo_data.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import asyncio
import uuid
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_URL = os.environ['MONGO_URL']
DB_NAME = os.environ['DB_NAME']

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DEMO_PASSWORD = "Password123!"

# Demo users configuration
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
        "email": "emp2@operai.demo",
        "name": "Bob Employee",
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


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


async def clear_collections(db):
    """Clear all demo data collections without dropping indexes"""
    print_section("Clearing Existing Demo Data")
    
    collections = [
        "users", "tasks", "leaves", "attendance", 
        "announcements", "ai_messages", "deadline_requests", "notifications"
    ]
    
    for collection_name in collections:
        count = await db[collection_name].count_documents({})
        if count > 0:
            await db[collection_name].delete_many({})
            print(f"✓ Cleared {count} documents from '{collection_name}'")
        else:
            print(f"  '{collection_name}' was already empty")


async def seed_users(db):
    """Create demo users for all roles"""
    print_section("Creating Demo Users")
    
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
        
        await db.users.insert_one(user)
        user_ids[user_data["role"] + "_" + user_data["email"].split("@")[0]] = user_id
        print(f"✓ Created {user_data['role']:12} - {user_data['name']:20} ({user_data['email']})")
    
    return user_ids


async def seed_tasks(db, user_ids):
    """Create realistic tasks with various statuses"""
    print_section("Creating Demo Tasks")
    
    team_lead_id = user_ids["team_lead_lead"]
    emp1_id = user_ids["employee_emp1"]
    emp2_id = user_ids["employee_emp2"]
    intern_id = user_ids["intern_intern"]
    
    today = datetime.now(timezone.utc)
    
    tasks_data = [
        {
            "title": "Complete Q1 Financial Report",
            "description": "Prepare and submit the Q1 financial analysis report with budget recommendations",
            "assigned_to": emp1_id,
            "created_by": team_lead_id,
            "status": "in_progress",
            "priority": "high",
            "progress": 65,
            "deadline": (today + timedelta(days=3)).isoformat(),
            "notes": "Waiting for data from finance department"
        },
        {
            "title": "Update Employee Onboarding Documentation",
            "description": "Review and update all onboarding materials for new hires",
            "assigned_to": emp1_id,
            "created_by": team_lead_id,
            "status": "todo",
            "priority": "medium",
            "progress": 0,
            "deadline": (today + timedelta(days=7)).isoformat(),
            "notes": ""
        },
        {
            "title": "Code Review - User Authentication Module",
            "description": "Review pull request #234 for the new authentication system",
            "assigned_to": emp2_id,
            "created_by": team_lead_id,
            "status": "completed",
            "priority": "high",
            "progress": 100,
            "deadline": (today - timedelta(days=1)).isoformat(),
            "notes": "Completed ahead of schedule"
        },
        {
            "title": "Setup Development Environment",
            "description": "Install and configure all necessary development tools and IDEs",
            "assigned_to": intern_id,
            "created_by": team_lead_id,
            "status": "completed",
            "priority": "urgent",
            "progress": 100,
            "deadline": (today - timedelta(days=5)).isoformat(),
            "notes": "All tools installed and tested"
        },
        {
            "title": "Research AI Integration Options",
            "description": "Evaluate different LLM providers and create comparison report",
            "assigned_to": emp2_id,
            "created_by": team_lead_id,
            "status": "in_progress",
            "priority": "medium",
            "progress": 40,
            "deadline": (today + timedelta(days=10)).isoformat(),
            "notes": "OpenAI and Anthropic evaluation complete"
        },
        {
            "title": "Write Unit Tests for API Endpoints",
            "description": "Create comprehensive unit tests for all REST API endpoints",
            "assigned_to": intern_id,
            "created_by": team_lead_id,
            "status": "in_progress",
            "priority": "low",
            "progress": 25,
            "deadline": (today + timedelta(days=14)).isoformat(),
            "notes": "Auth endpoints tests completed"
        },
        {
            "title": "Customer Feedback Analysis",
            "description": "Analyze customer feedback from Q4 and create insights report",
            "assigned_to": emp1_id,
            "created_by": team_lead_id,
            "status": "blocked",
            "priority": "medium",
            "progress": 10,
            "deadline": (today + timedelta(days=5)).isoformat(),
            "notes": "Waiting for data export from CRM system"
        },
        {
            "title": "Database Migration Planning",
            "description": "Plan and document the migration strategy from MySQL to PostgreSQL",
            "assigned_to": emp2_id,
            "created_by": team_lead_id,
            "status": "todo",
            "priority": "high",
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
        await db.tasks.insert_one(task)
        task_ids.append(task_id)
        
        status_emoji = {
            "todo": "📋",
            "in_progress": "🔄",
            "completed": "✅",
            "blocked": "🚫"
        }
        print(f"{status_emoji[task_data['status']]} {task_data['title'][:40]:40} - {task_data['status']:12} [{task_data['progress']}%]")
    
    return task_ids


async def seed_leaves(db, user_ids):
    """Create leave applications with different statuses"""
    print_section("Creating Leave Applications")
    
    hr_id = user_ids["hr_hr"]
    emp1_id = user_ids["employee_emp1"]
    emp2_id = user_ids["employee_emp2"]
    intern_id = user_ids["intern_intern"]
    
    today = datetime.now(timezone.utc)
    
    leaves_data = [
        {
            "user_id": emp1_id,
            "leave_type": "casual",
            "start_date": (today + timedelta(days=15)).strftime('%Y-%m-%d'),
            "end_date": (today + timedelta(days=17)).strftime('%Y-%m-%d'),
            "reason": "Family vacation planned",
            "status": "pending",
            "approved_by": None,
            "rejection_reason": None
        },
        {
            "user_id": emp2_id,
            "leave_type": "sick",
            "start_date": (today - timedelta(days=3)).strftime('%Y-%m-%d'),
            "end_date": (today - timedelta(days=2)).strftime('%Y-%m-%d'),
            "reason": "Flu and fever",
            "status": "approved",
            "approved_by": hr_id,
            "rejection_reason": None
        },
        {
            "user_id": intern_id,
            "leave_type": "earned",
            "start_date": (today + timedelta(days=30)).strftime('%Y-%m-%d'),
            "end_date": (today + timedelta(days=34)).strftime('%Y-%m-%d'),
            "reason": "University examinations",
            "status": "approved",
            "approved_by": hr_id,
            "rejection_reason": None
        },
        {
            "user_id": emp1_id,
            "leave_type": "casual",
            "start_date": (today - timedelta(days=10)).strftime('%Y-%m-%d'),
            "end_date": (today - timedelta(days=8)).strftime('%Y-%m-%d'),
            "reason": "Personal work",
            "status": "rejected",
            "approved_by": hr_id,
            "rejection_reason": "Insufficient leave balance"
        },
        {
            "user_id": emp2_id,
            "leave_type": "casual",
            "start_date": (today + timedelta(days=7)).strftime('%Y-%m-%d'),
            "end_date": (today + timedelta(days=8)).strftime('%Y-%m-%d'),
            "reason": "Attending friend's wedding",
            "status": "pending",
            "approved_by": None,
            "rejection_reason": None
        }
    ]
    
    leave_ids = []
    for leave_data in leaves_data:
        leave_id = str(uuid.uuid4())
        leave = {
            "id": leave_id,
            **leave_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.leaves.insert_one(leave)
        leave_ids.append(leave_id)
        
        status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
        user = next(u for u in DEMO_USERS if db.users.find_one({"id": leave_data["user_id"]}))
        print(f"{status_emoji[leave_data['status']]} {leave_data['leave_type']:8} - {leave_data['start_date']} to {leave_data['end_date']} - {leave_data['status']:8}")
    
    return leave_ids


async def seed_attendance(db, user_ids):
    """Create attendance records for the past week"""
    print_section("Creating Attendance Records")
    
    emp1_id = user_ids["employee_emp1"]
    emp2_id = user_ids["employee_emp2"]
    intern_id = user_ids["intern_intern"]
    
    today = datetime.now(timezone.utc)
    
    attendance_records = []
    
    # Generate attendance for past 7 days
    for days_ago in range(7, 0, -1):
        date = today - timedelta(days=days_ago)
        date_str = date.strftime('%Y-%m-%d')
        
        # Employee 1 - Perfect attendance
        attendance_records.append({
            "user_id": emp1_id,
            "date": date_str,
            "work_mode": "wfo" if days_ago % 2 == 0 else "wfh",
            "status": "present" if days_ago % 2 == 0 else "wfh"
        })
        
        # Employee 2 - Mostly WFH
        if days_ago != 3:  # Absent one day
            attendance_records.append({
                "user_id": emp2_id,
                "date": date_str,
                "work_mode": "wfh",
                "status": "wfh"
            })
        
        # Intern - Regular office attendance
        if days_ago not in [6, 7]:  # Weekend off
            attendance_records.append({
                "user_id": intern_id,
                "date": date_str,
                "work_mode": "wfo",
                "status": "present"
            })
    
    count = 0
    for record in attendance_records:
        attendance_id = str(uuid.uuid4())
        attendance = {
            "id": attendance_id,
            **record,
            "check_in": (datetime.strptime(record["date"], '%Y-%m-%d').replace(hour=9, minute=0, tzinfo=timezone.utc)).isoformat(),
            "check_out": (datetime.strptime(record["date"], '%Y-%m-%d').replace(hour=18, minute=0, tzinfo=timezone.utc)).isoformat(),
            "notes": None,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.attendance.insert_one(attendance)
        count += 1
    
    print(f"✓ Created {count} attendance records for the past 7 days")
    print(f"  - Employee 1: 7/7 days (WFO + WFH mix)")
    print(f"  - Employee 2: 6/7 days (mostly WFH)")
    print(f"  - Intern: 5/7 days (weekday WFO)")


async def seed_deadline_requests(db, user_ids, task_ids):
    """Create deadline extension requests"""
    print_section("Creating Deadline Requests")
    
    team_lead_id = user_ids["team_lead_lead"]
    emp1_id = user_ids["employee_emp1"]
    emp2_id = user_ids["employee_emp2"]
    
    today = datetime.now(timezone.utc)
    
    requests_data = [
        {
            "task_id": task_ids[0] if len(task_ids) > 0 else str(uuid.uuid4()),
            "requested_by": emp1_id,
            "requested_new_deadline": (today + timedelta(days=7)).strftime('%Y-%m-%d'),
            "reason": "Need additional time for data analysis from finance team",
            "status": "pending",
            "responded_by": None,
            "response_note": None
        },
        {
            "task_id": task_ids[4] if len(task_ids) > 4 else str(uuid.uuid4()),
            "requested_by": emp2_id,
            "requested_new_deadline": (today + timedelta(days=14)).strftime('%Y-%m-%d'),
            "reason": "Research taking longer than expected, need more evaluation time",
            "status": "approved",
            "responded_by": team_lead_id,
            "response_note": "Approved. Please prioritize completion."
        },
        {
            "task_id": task_ids[1] if len(task_ids) > 1 else str(uuid.uuid4()),
            "requested_by": emp1_id,
            "requested_new_deadline": (today + timedelta(days=21)).strftime('%Y-%m-%d'),
            "reason": "Waiting for stakeholder feedback",
            "status": "rejected",
            "responded_by": team_lead_id,
            "response_note": "Deadline cannot be extended. Please work with current timeline."
        }
    ]
    
    for request_data in requests_data:
        request_id = str(uuid.uuid4())
        request = {
            "id": request_id,
            **request_data,
            "created_at": (today - timedelta(days=2)).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat() if request_data["status"] != "pending" else None
        }
        await db.deadline_requests.insert_one(request)
        
        status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
        print(f"{status_emoji[request_data['status']]} {request_data['reason'][:50]:50} - {request_data['status']}")


async def seed_announcements(db, user_ids):
    """Create company and team announcements"""
    print_section("Creating Announcements")
    
    hr_id = user_ids["hr_hr"]
    admin_id = user_ids["admin_admin"]
    
    today = datetime.now(timezone.utc)
    
    announcements_data = [
        {
            "title": "🎉 Company All-Hands Meeting - Q1 Results",
            "content": "Join us this Friday at 3 PM for our quarterly all-hands meeting. We'll be discussing Q1 achievements, upcoming projects, and team recognitions. Attendance is mandatory for all employees.",
            "created_by": admin_id,
            "target_roles": []  # All users
        },
        {
            "title": "🏥 New Health Insurance Policy Update",
            "content": "We're excited to announce enhanced health insurance coverage starting next month. All employees will receive increased coverage limits and additional wellness benefits. Check your email for detailed information.",
            "created_by": hr_id,
            "target_roles": []  # All users
        },
        {
            "title": "🎓 Training Opportunity: Advanced Leadership Program",
            "content": "We're offering spots in an advanced leadership development program for team leads. The program runs for 6 weeks starting next month. Interested team leads should apply by end of this week.",
            "created_by": hr_id,
            "target_roles": ["team_lead"]
        },
        {
            "title": "🌟 Employee of the Month - Bob Employee",
            "content": "Congratulations to Bob Employee for being selected as Employee of the Month! Bob's exceptional work on the authentication module and his dedication to code quality made a significant impact on our project timeline.",
            "created_by": hr_id,
            "target_roles": []  # All users
        },
        {
            "title": "🏢 Office Maintenance - This Weekend",
            "content": "Please note that the office will undergo scheduled maintenance this weekend (Saturday & Sunday). The HVAC system and electrical panels will be serviced. Remote work is available if you need to access systems.",
            "created_by": admin_id,
            "target_roles": []  # All users
        }
    ]
    
    announcement_ids = []
    for announcement_data in announcements_data:
        announcement_id = str(uuid.uuid4())
        announcement = {
            "id": announcement_id,
            **announcement_data,
            "created_at": (today - timedelta(days=len(announcement_ids) * 2)).isoformat()
        }
        await db.announcements.insert_one(announcement)
        announcement_ids.append(announcement_id)
        
        target = "All Users" if not announcement_data["target_roles"] else ", ".join(announcement_data["target_roles"])
        print(f"📢 {announcement_data['title'][:50]:50} → {target}")
    
    return announcement_ids


async def seed_notifications(db, user_ids, announcement_ids):
    """Create notifications for various events"""
    print_section("Creating Notifications")
    
    emp1_id = user_ids["employee_emp1"]
    emp2_id = user_ids["employee_emp2"]
    intern_id = user_ids["intern_intern"]
    team_lead_id = user_ids["team_lead_lead"]
    
    today = datetime.now(timezone.utc)
    
    notifications_data = [
        # Announcement notifications (company-wide)
        {
            "user_id": None,
            "target_roles": [],
            "type": "announcement",
            "title": "🎉 Company All-Hands Meeting - Q1 Results",
            "message": "Join us this Friday at 3 PM for our quarterly all-hands meeting. We'll be discussing Q1 achievements, upcoming projects, and team recognitions...",
            "related_task_id": None,
            "related_request_id": None
        },
        {
            "user_id": None,
            "target_roles": [],
            "type": "announcement",
            "title": "🏥 New Health Insurance Policy Update",
            "message": "We're excited to announce enhanced health insurance coverage starting next month. All employees will receive increased coverage limits...",
            "related_task_id": None,
            "related_request_id": None
        },
        # Deadline change notification
        {
            "user_id": emp2_id,
            "target_roles": [],
            "type": "deadline_change",
            "title": "Task deadline updated",
            "message": "Deadline for 'Research AI Integration Options' has been updated",
            "related_task_id": None,
            "related_request_id": None
        },
        # Deadline request updates
        {
            "user_id": emp2_id,
            "target_roles": [],
            "type": "deadline_request_update",
            "title": "Deadline request approved",
            "message": "Your deadline extension request for 'Research AI Integration Options' has been approved. New deadline: " + 
                      (today + timedelta(days=14)).strftime('%Y-%m-%d'),
            "related_task_id": None,
            "related_request_id": None
        },
        {
            "user_id": emp1_id,
            "target_roles": [],
            "type": "deadline_request_update",
            "title": "Deadline request rejected",
            "message": "Your deadline extension request for 'Update Employee Onboarding Documentation' has been rejected. Reason: Deadline cannot be extended. Please work with current timeline.",
            "related_task_id": None,
            "related_request_id": None
        },
        # Task assignment notifications
        {
            "user_id": emp1_id,
            "target_roles": [],
            "type": "task_assigned",
            "title": "New task assigned",
            "message": "You have been assigned a new task: 'Complete Q1 Financial Report'",
            "related_task_id": None,
            "related_request_id": None
        },
        {
            "user_id": intern_id,
            "target_roles": [],
            "type": "task_assigned",
            "title": "New task assigned",
            "message": "You have been assigned a new task: 'Write Unit Tests for API Endpoints'",
            "related_task_id": None,
            "related_request_id": None
        }
    ]
    
    count = 0
    for i, notification_data in enumerate(notifications_data):
        notification_id = str(uuid.uuid4())
        notification = {
            "id": notification_id,
            **notification_data,
            "is_read": i > 4,  # Mark some as read
            "metadata": None,
            "created_at": (today - timedelta(hours=24 - i * 3)).isoformat()
        }
        await db.notifications.insert_one(notification)
        count += 1
    
    print(f"✓ Created {count} notifications")
    print(f"  - Company announcements: 2")
    print(f"  - Deadline updates: 3")
    print(f"  - Task assignments: 2")


async def seed_ai_history(db, user_ids):
    """Create sample AI conversation history"""
    print_section("Creating AI Conversation History")
    
    emp1_id = user_ids["employee_emp1"]
    emp2_id = user_ids["employee_emp2"]
    
    today = datetime.now(timezone.utc)
    session_id = str(uuid.uuid4())
    
    ai_messages = [
        {
            "user_id": emp1_id,
            "session_id": session_id,
            "message": "mujhe aaj ke tasks dikhao",
            "response": "You have 3 tasks assigned to you today:\n1. Complete Q1 Financial Report (In Progress - 65%)\n2. Update Employee Onboarding Documentation (To Do)\n3. Customer Feedback Analysis (Blocked - 10%)",
            "action_type": "execute",
            "actions_executed": [
                {
                    "success": True,
                    "action": "list_user_tasks",
                    "details": {"count": 3}
                }
            ]
        },
        {
            "user_id": emp1_id,
            "session_id": session_id,
            "message": "What's the status of my financial report task?",
            "response": "Your 'Complete Q1 Financial Report' task is currently in progress at 65% completion. The deadline is in 3 days. You've noted that you're waiting for data from the finance department.",
            "action_type": "chat",
            "actions_executed": []
        },
        {
            "user_id": emp2_id,
            "session_id": str(uuid.uuid4()),
            "message": "kal ka WFH mark kar do",
            "response": "I can't mark attendance for tomorrow in advance. You can only mark attendance for today. Would you like me to mark today's attendance as WFH?",
            "action_type": "chat",
            "actions_executed": []
        }
    ]
    
    for i, ai_message in enumerate(ai_messages):
        message_id = str(uuid.uuid4())
        message = {
            "id": message_id,
            **ai_message,
            "created_at": (today - timedelta(hours=12 - i * 2)).isoformat()
        }
        await db.ai_messages.insert_one(message)
    
    print(f"✓ Created {len(ai_messages)} AI conversation messages")
    print(f"  - Task queries: 2")
    print(f"  - Attendance queries: 1")


async def print_summary(user_ids):
    """Print summary of seeded data"""
    print_section("✅ Demo Data Seeding Complete!")
    
    print("\n📋 DEMO USER ACCOUNTS:")
    print(f"{'Role':<12} {'Email':<25} {'Password':<15} {'Name'}")
    print("-" * 75)
    
    accounts = [
        ("Admin", "admin@operai.demo", DEMO_PASSWORD, "Admin User"),
        ("HR", "hr@operai.demo", DEMO_PASSWORD, "Sarah HR Manager"),
        ("Team Lead", "lead@operai.demo", DEMO_PASSWORD, "John Team Lead"),
        ("Employee", "emp1@operai.demo", DEMO_PASSWORD, "Alice Employee"),
        ("Employee", "emp2@operai.demo", DEMO_PASSWORD, "Bob Employee"),
        ("Intern", "intern@operai.demo", DEMO_PASSWORD, "Charlie Intern")
    ]
    
    for role, email, password, name in accounts:
        print(f"{role:<12} {email:<25} {password:<15} {name}")
    
    print("\n📊 DATA SUMMARY:")
    print("  ✓ 6 demo users created (all roles)")
    print("  ✓ 8 tasks with various statuses and priorities")
    print("  ✓ 5 leave applications (pending, approved, rejected)")
    print("  ✓ 18 attendance records (past 7 days)")
    print("  ✓ 3 deadline extension requests")
    print("  ✓ 5 company and team announcements")
    print("  ✓ 7 notifications (read and unread)")
    print("  ✓ 3 AI conversation history entries")
    
    print("\n🚀 NEXT STEPS:")
    print("  1. Navigate to the OperAI frontend")
    print("  2. Use any of the demo accounts above to login")
    print("  3. Explore tasks, leaves, attendance, and AI features")
    print("\n" + "=" * 60 + "\n")


async def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("  🌱 OperAI Demo Data Seeding Script")
    print("="*60)
    print(f"\nConnecting to MongoDB: {DB_NAME}")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Verify connection
        await db.command('ping')
        print("✓ MongoDB connection successful\n")
        
        # Execute seeding steps
        await clear_collections(db)
        user_ids = await seed_users(db)
        task_ids = await seed_tasks(db, user_ids)
        leave_ids = await seed_leaves(db, user_ids)
        await seed_attendance(db, user_ids)
        await seed_deadline_requests(db, user_ids, task_ids)
        announcement_ids = await seed_announcements(db, user_ids)
        await seed_notifications(db, user_ids, announcement_ids)
        await seed_ai_history(db, user_ids)
        
        # Print summary
        await print_summary(user_ids)
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(main())

# OperAI Demo Seeding - Quick Reference

## 🚀 Quick Start

### 1. Seed Demo Data
```bash
cd /app/backend
python seed_demo_data.py
```

### 2. Login with Demo Accounts
Open the frontend and use any of these accounts:

```
┌──────────────────────────────────────────────────────────┐
│  DEMO ACCOUNTS - Click to Auto-Fill on Login Page       │
├──────────────────────────────────────────────────────────┤
│  🛡️  Admin      → admin@operai.demo                      │
│  👥  HR         → hr@operai.demo                         │
│  💼  Team Lead  → lead@operai.demo                       │
│  👤  Employee   → emp1@operai.demo                       │
│  🎓  Intern     → intern@operai.demo                     │
└──────────────────────────────────────────────────────────┘
  Password for all accounts: Password123!
```

---

## 📊 What Gets Seeded

### Users (6)
- 1 Admin, 1 HR, 1 Team Lead, 2 Employees, 1 Intern

### Tasks (8)
- 3 In Progress
- 2 To Do
- 2 Completed
- 1 Blocked

### Leaves (5)
- 2 Pending
- 2 Approved
- 1 Rejected

### Attendance (18 records)
- Past 7 days for all active employees
- Mix of WFO, WFH, and absences

### Deadline Requests (3)
- 1 Pending
- 1 Approved
- 1 Rejected

### Announcements (5)
- Company-wide meetings
- Policy updates
- Team recognitions

### Notifications (7)
- Task assignments
- Deadline changes
- Announcement alerts

### AI History (3)
- Sample conversations
- Hindi-English queries
- Action executions

---

## 🎯 Role-Specific Views

### Admin Dashboard
- View all users
- Access all features
- System-wide statistics

### HR Dashboard
- Employee management
- Leave approvals
- Company announcements
- Employee reports

### Team Lead Dashboard
- Create and assign tasks
- View team tasks
- Approve deadline requests
- Team performance stats

### Employee Dashboard
- Assigned tasks
- Submit leave requests
- Mark attendance
- Request deadline extensions
- AI Assistant

### Intern Dashboard
- Assigned tasks
- Basic features
- Learning activities

---

## 💡 Testing Scenarios

### Scenario 1: Task Management Flow
1. Login as **Team Lead** (lead@operai.demo)
2. View existing tasks
3. Create a new task for Employee 1
4. View team dashboard stats

### Scenario 2: Leave Approval Flow
1. Login as **Employee** (emp1@operai.demo)
2. Apply for leave (future dates)
3. Logout and login as **HR** (hr@operai.demo)
4. View pending leaves
5. Approve the leave request

### Scenario 3: Attendance Tracking
1. Login as **Employee** (emp2@operai.demo)
2. Check-in for the day
3. View attendance history
4. Check-out at end of day

### Scenario 4: Deadline Extension
1. Login as **Employee** (emp1@operai.demo)
2. Find a task with upcoming deadline
3. Request deadline extension
4. Logout and login as **Team Lead**
5. View deadline requests
6. Approve or reject the request

### Scenario 5: AI Assistant
1. Login as any user
2. Open AI Assistant
3. Try these queries:
   - "mujhe aaj ke tasks dikhao"
   - "kal ka leave laga do"
   - "summarize my notifications"

---

## 🎨 Frontend Demo Features

### Login Page Enhancements
- **Visual Demo Panel**: Grid of role buttons with icons
- **One-Click Fill**: Click any role to auto-fill credentials
- **Hide/Show Toggle**: Can hide demo panel if needed
- **Help Text**: Clear instructions and password hint

### Quick-Fill Buttons
```
[🛡️ Admin] [👥 HR] [💼 Team Lead]
[👤 Employee] [👤 Employee] [🎓 Intern]
```

---

## 📋 Script Output

When you run `python seed_demo_data.py`, you'll see:

```
============================================================
  🌱 OperAI Demo Data Seeding Script
============================================================

Connecting to MongoDB: workforceos_db
✓ MongoDB connection successful

============================================================
  Clearing Existing Demo Data
============================================================
✓ Cleared X documents from 'users'
✓ Cleared X documents from 'tasks'
...

============================================================
  Creating Demo Users
============================================================
✓ Created admin        - Admin User
✓ Created hr           - Sarah HR Manager
...

[Additional seeding steps...]

============================================================
  ✅ Demo Data Seeding Complete!
============================================================

📋 DEMO USER ACCOUNTS:
Role         Email                     Password        Name
---------------------------------------------------------------------------
Admin        admin@operai.demo         Password123!    Admin User
HR           hr@operai.demo            Password123!    Sarah HR Manager
...

📊 DATA SUMMARY:
  ✓ 6 demo users created (all roles)
  ✓ 8 tasks with various statuses and priorities
  ✓ 5 leave applications (pending, approved, rejected)
  ...

🚀 NEXT STEPS:
  1. Navigate to the OperAI frontend
  2. Use any of the demo accounts above to login
  3. Explore tasks, leaves, attendance, and AI features
```

---

## 🔄 Reset Demo Data

To reset to a clean demo state anytime:

```bash
cd /app/backend
python seed_demo_data.py
```

This will:
- Clear all existing demo data
- Recreate all users
- Regenerate all demo content
- Preserve database indexes

**Note**: Takes only 2-3 seconds to complete.

---

## 📖 Full Documentation

For detailed information, see:
- `/app/README.md` - Complete project documentation
- `/app/DEMO_SEEDING_IMPLEMENTATION.md` - Implementation details
- `/app/QA_SESSION_SUMMARY.md` - Backend QA results

---

## ✅ Checklist for Judges/Reviewers

- [ ] Run seeding script
- [ ] Open login page
- [ ] See demo account buttons
- [ ] Try quick-fill feature
- [ ] Login as different roles
- [ ] Explore role-specific features
- [ ] Test AI Assistant
- [ ] Check notifications
- [ ] Review task management
- [ ] Test leave workflow

---

**🎉 Everything is ready for demo! Just run the seeding script and start exploring!**

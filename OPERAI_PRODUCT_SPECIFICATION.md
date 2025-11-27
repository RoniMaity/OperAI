# OperAI - Enterprise WorkforceOS
## Complete Product Specification & Blueprint

**Version:** 1.0  
**Last Updated:** January 2025  
**Document Type:** Enterprise Product Blueprint

---

# 1. PRODUCT VISION

## 1.1 Purpose & Positioning

### Core Mission
OperAI is an AI-native enterprise workforce management platform that eliminates manual HR operations through intelligent automation, predictive analytics, and real-time workforce intelligence. Unlike traditional HRIS systems that digitize paper processes, OperAI reimagines workforce management from first principles with AI at the core.

### Market Positioning

**vs. Rippling:**
- Rippling: Systems of record with basic automation
- OperAI: AI-native decisioning engine with predictive workforce intelligence
- Advantage: Proactive vs reactive management

**vs. Workday:**
- Workday: Enterprise ERP with heavy implementation cycles
- OperAI: Lightweight, AI-first platform with zero-config intelligence
- Advantage: Deploy in days, not months

**vs. Zoho People:**
- Zoho: Traditional HR workflows with add-on AI features
- Zoho People: Process automation
- OperAI: Cognitive workforce orchestration
- Advantage: AI makes decisions, not just suggestions

**vs. Factorial:**
- Factorial: SMB-focused feature parity
- OperAI: Enterprise-grade with role-based AI agents
- Advantage: Scales from 10 to 10,000 employees

### Unique Value Propositions

1. **AI-Native Architecture**
   - Every workflow has an AI counterpart
   - Predictive rather than reactive
   - Learns from organizational patterns

2. **Zero-Touch Operations**
   - 80% of routine HR tasks automated
   - AI handles approvals within policy bounds
   - Escalates only exceptional cases

3. **Role-Based AI Agents**
   - Each user role gets a personalized AI assistant
   - Context-aware based on role, team, history
   - Proactive recommendations

4. **Real-Time Workforce Intelligence**
   - Live dashboards, not weekly reports
   - Predictive analytics for attrition, burnout
   - Anomaly detection across attendance, performance

5. **Cost Optimization**
   - Free-tier AI (Gemini 2.5 Flash)
   - Self-hosted option
   - Pay-per-use pricing

## 1.2 How AI Changes Workflows

### Traditional vs AI-Native

| Traditional Workflow | AI-Native Workflow |
|---------------------|-------------------|
| Employee applies leave → HR approves | AI checks conflicts → auto-approves if clear → notifies only if issue |
| Manager assigns tasks manually | AI suggests optimal assignments based on workload, skills, availability |
| HR reviews attendance monthly | AI flags anomalies real-time → auto-corrects minor issues |
| Annual performance reviews | Continuous AI-driven performance insights |
| Manual shift scheduling | AI optimizes schedules considering preferences, fairness, coverage |

### AI Intervention Points

1. **Preventive:** Stop issues before they occur (conflict detection)
2. **Corrective:** Auto-fix minor anomalies (attendance corrections)
3. **Suggestive:** Recommend optimal actions (task assignments)
4. **Predictive:** Forecast future states (attrition risk)
5. **Generative:** Create content (announcements, reports)

---

# 2. INFORMATION ARCHITECTURE

## 2.1 Module Hierarchy

```
OperAI
│
├── Authentication
│   ├── Login
│   ├── Register
│   ├── Password Reset
│   └── MFA (Phase 2)
│
├── Core Navigation
│   ├── Dashboard (Role-Specific)
│   ├── Global Search
│   ├── Notifications Center
│   └── Quick Actions
│
├── HR Module (Admin/HR Only)
│   ├── Overview Dashboard
│   ├── Employee Management
│   │   ├── Employee List
│   │   ├── Add Employee
│   │   ├── Employee Profile
│   │   ├── Bulk Import
│   │   └── Deactivate/Offboard
│   ├── Department Management
│   │   ├── Departments List
│   │   ├── Create Department
│   │   └── Department Analytics
│   ├── Leave Management
│   │   ├── Leave Requests Queue
│   │   ├── Approve/Reject
│   │   ├── Leave Policies
│   │   └── Leave Calendar
│   ├── Attendance Management
│   │   ├── Attendance Overview
│   │   ├── Corrections Queue
│   │   ├── Patterns & Anomalies
│   │   └── Shift Management
│   ├── Announcements
│   │   ├── Create Announcement
│   │   ├── Announcement List
│   │   └── Analytics (reach, engagement)
│   └── Analytics & Reports
│       ├── Workforce Analytics
│       ├── Attendance Reports
│       ├── Leave Reports
│       ├── Performance Insights
│       └── AI Predictions
│
├── Team Lead Module
│   ├── Team Dashboard
│   ├── Team Members View
│   ├── Task Management
│   │   ├── Assign Tasks
│   │   ├── Task Board (Kanban)
│   │   ├── Task List
│   │   └── Workload Distribution
│   ├── Performance Tracking
│   │   ├── Team Performance
│   │   ├── Individual Performance
│   │   └── 1-on-1 Notes
│   ├── Leave Approvals
│   └── Attendance Review
│
├── Employee Module
│   ├── Personal Dashboard
│   ├── My Tasks
│   │   ├── Active Tasks
│   │   ├── Completed Tasks
│   │   ├── Task Details
│   │   └── Update Progress
│   ├── My Attendance
│   │   ├── Check In/Out
│   │   ├── Attendance History
│   │   └── Request Correction
│   ├── My Leave
│   │   ├── Apply Leave
│   │   ├── Leave Balance
│   │   ├── Leave History
│   │   └── Cancel Request
│   ├── My Profile
│   │   ├── Personal Info
│   │   ├── Documents
│   │   └── Settings
│   └── Announcements
│
├── Intern Module
│   ├── Intern Dashboard
│   ├── My Tasks
│   │   ├── Task List
│   │   ├── Daily Log
│   │   ├── Progress Tracking
│   │   └── Submit Work
│   ├── Learning & Development
│   │   ├── Learning Path
│   │   ├── Skill Gap Analysis
│   │   └── Resources
│   ├── Attendance
│   ├── Leave
│   └── Mentor Connect
│
├── AI Assistant (All Roles)
│   ├── Chat Interface
│   ├── Quick Actions
│   │   ├── Rewrite Content
│   │   ├── Generate Report
│   │   ├── Explain Task
│   │   ├── Suggest Breakdown
│   │   └── Summarize
│   ├── Automations
│   │   ├── Auto-Approve
│   │   ├── Auto-Assign
│   │   ├── Auto-Nudge
│   │   └── Auto-Generate
│   └── Chat History
│
├── Notifications
│   ├── Notification Center
│   ├── Filter by Type
│   └── Mark Read/Unread
│
└── Admin Module
    ├── System Settings
    ├── User Roles & Permissions
    ├── Department Configuration
    ├── Policies Configuration
    ├── Integration Settings
    ├── Audit Logs
    └── System Health
```

## 2.2 Screen-by-Screen Breakdown

### 2.2.1 HR Dashboard

**URL:** `/hr-dashboard`  
**Access:** Admin, HR

**Layout:**
```
┌─────────────────────────────────────────────┐
│ Header: WorkforceOS | [Search] | [Profile]  │
├─────┬───────────────────────────────────────┤
│     │ HR Dashboard                          │
│ S   │ Manage your workforce operations      │
│ I   ├───────────────────────────────────────┤
│ D   │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│ E   │ │Total│ │Total│ │Pend.│ │Pres.│      │
│ B   │ │Emp. │ │Tasks│ │Leave│ │Today│      │
│ A   │ │ 245 │ │ 892 │ │  12 │ │ 231 │      │
│ R   │ └─────┘ └─────┘ └─────┘ └─────┘      │
│     │                                        │
│     │ ┌────────────────────────────────┐   │
│     │ │ Pending Approvals              │   │
│     │ │ • Leave Requests (12)          │   │
│     │ │ • Attendance Corrections (5)   │   │
│     │ │ • Document Verifications (3)   │   │
│     │ └────────────────────────────────┘   │
│     │                                        │
│     │ ┌────────────────────────────────┐   │
│     │ │ AI Insights                    │   │
│     │ │ ⚠ High attrition risk: Eng team│   │
│     │ │ 📊 Attendance anomaly detected │   │
│     │ └────────────────────────────────┘   │
└─────┴────────────────────────────────────────┘
```

**Components:**
- 4 Stat Cards (Total Employees, Total Tasks, Pending Leaves, Present Today)
- Pending Approvals Card with action buttons
- AI Insights Card with real-time alerts
- Quick Actions FAB (bottom right)

**Actions:**
- Click stat card → Navigate to detail view
- Click approval item → Open approval modal
- Click AI insight → View detailed analysis

**States:**
- Loading: Skeleton cards
- Empty: "No pending actions"
- Error: Retry banner

### 2.2.2 Employee Dashboard

**URL:** `/dashboard`  
**Access:** Employee, Intern

**Layout:**
```
┌─────────────────────────────────────────────┐
│ Header: WorkforceOS | [Search] | [Profile]  │
├─────┬───────────────────────────────────────┤
│     │ Dashboard                             │
│ S   │ Welcome back! Here's your overview.   │
│ I   ├───────────────────────────────────────┤
│ D   │ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│ E   │ │My   │ │Pend.│ │Comp.│ │Leave│      │
│ B   │ │Tasks│ │Tasks│ │Tasks│ │Req. │      │
│ A   │ │  8  │ │  3  │ │  5  │ │  2  │      │
│ R   │ └─────┘ └─────┘ └─────┘ └─────┘      │
│     │                                        │
│     │ ┌────────────────────────────────┐   │
│     │ │ Recent Tasks                   │   │
│     │ │ ┌──────────────────────────┐   │   │
│     │ │ │ [TODO] Fix login bug     │   │   │
│     │ │ │ Priority: HIGH           │   │   │
│     │ │ │ Progress: 45% [=====--- ]│   │   │
│     │ │ └──────────────────────────┘   │   │
│     │ └────────────────────────────────┘   │
│     │                                        │
│     │ ┌────────────────────────────────┐   │
│     │ │ Announcements                  │   │
│     │ │ • Team meeting at 3 PM         │   │
│     │ │ • New policy update            │   │
│     │ └────────────────────────────────┘   │
└─────┴────────────────────────────────────────┘
```

**Components:**
- 4 Stat Cards (My Tasks, Pending, Completed, Leave Requests)
- Recent Tasks List with progress bars
- Announcements Feed
- Check-in button (if not checked in)

**Actions:**
- Click task → Task details modal
- Drag progress slider → Update task progress
- Click announcement → Full announcement view

**States:**
- No tasks: "No tasks assigned yet"
- Checked in: Show check-out button
- Not checked in: Show check-in button

### 2.2.3 Task Management Page

**URL:** `/tasks`  
**Access:** All roles (permissions vary)

**Layout:**
```
┌─────────────────────────────────────────────┐
│ Tasks | [Filter] [Sort] [View: Grid/List]   │
│                          [+ Create Task] ←HR│
├─────────────────────────────────────────────┤
│ Filters: [Status] [Priority] [Assigned To] │
├─────────────────────────────────────────────┤
│                                              │
│ ┌──────────────────────────────────────┐   │
│ │ Fix authentication bug                │   │
│ │ [IN_PROGRESS] [HIGH]                  │   │
│ │ Assigned: John Doe                    │   │
│ │ Deadline: Jan 15, 2025                │   │
│ │ Progress: 60% [======----]            │   │
│ │ [View Details] [Update]               │   │
│ └──────────────────────────────────────┘   │
│                                              │
│ ┌──────────────────────────────────────┐   │
│ │ Design new dashboard                  │   │
│ │ [TODO] [MEDIUM]                       │   │
│ │ Assigned: Jane Smith                  │   │
│ │ Deadline: Jan 20, 2025                │   │
│ │ Progress: 10% [=------]               │   │
│ │ [View Details] [Update]               │   │
│ └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Components:**
- Filter bar (Status, Priority, Assigned To, Date Range)
- Sort dropdown (Deadline, Priority, Progress)
- View toggle (Grid/List/Kanban)
- Task cards with:
  - Title
  - Status badge
  - Priority badge
  - Assignee avatar
  - Progress bar
  - Action buttons

**Actions (Role-based):**
- **HR/Team Lead:**
  - Create task
  - Assign/reassign
  - Edit any task
  - Delete task
- **Employee/Intern:**
  - Update own task progress
  - Update status
  - Add notes
  - View details

**States:**
- Loading: Skeleton cards
- Empty: "No tasks yet"
- Filtered empty: "No tasks match filters"

### 2.2.4 Attendance Page

**URL:** `/attendance`  
**Access:** All roles

**Layout:**
```
┌─────────────────────────────────────────────┐
│ Attendance                                   │
├─────────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐    │
│ │ Today's Attendance                  │    │
│ │                                     │    │
│ │ Work Mode: [WFO ▼]                  │    │
│ │ [Check In] or                       │    │
│ │                                     │    │
│ │ Checked In: 09:15 AM                │    │
│ │ [Check Out]                         │    │
│ └─────────────────────────────────────┘    │
│                                              │
│ ┌─────────────────────────────────────┐    │
│ │ Attendance History                  │    │
│ │                                     │    │
│ │ ┌─────────────────────────────┐    │    │
│ │ │ Jan 10, 2025                │    │    │
│ │ │ In: 09:00 AM | Out: 06:00 PM│    │    │
│ │ │ [WFO] [PRESENT]             │    │    │
│ │ └─────────────────────────────┘    │    │
│ │                                     │    │
│ │ ┌─────────────────────────────┐    │    │
│ │ │ Jan 09, 2025                │    │    │
│ │ │ In: 09:30 AM | Out: 06:15 PM│    │    │
│ │ │ [WFH] [PRESENT]             │    │    │
│ │ └─────────────────────────────┘    │    │
│ └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

**Components:**
- Check-in card:
  - Work mode selector (WFO/WFH/Hybrid)
  - Check-in button (if not checked in)
  - Check-in/out times (if checked in)
  - Check-out button (if checked in)
- Attendance history list:
  - Date
  - Check-in/out times
  - Work mode badge
  - Status badge
  - Request correction button (HR approval required)

**Actions:**
- Check In → Record timestamp + work mode
- Check Out → Record timestamp
- Request Correction → Modal for correction reason

**States:**
- Not checked in: Show check-in form
- Checked in: Show times + check-out button
- Checked out: Show completed record

### 2.2.5 Leave Management Page

**URL:** `/leave`  
**Access:** All roles

**Layout:**
```
┌─────────────────────────────────────────────┐
│ Leave Requests              [+ Apply Leave] │
├─────────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐    │
│ │ Sick Leave                          │    │
│ │ Jan 15 - Jan 17, 2025 (3 days)     │    │
│ │ [PENDING] ⏱                         │    │
│ │ Reason: Medical checkup             │    │
│ │                                     │    │
│ │ [Approve] [Reject] ←HR only         │    │
│ └─────────────────────────────────────┘    │
│                                              │
│ ┌─────────────────────────────────────┐    │
│ │ Casual Leave                        │    │
│ │ Jan 05 - Jan 06, 2025 (2 days)     │    │
│ │ [APPROVED] ✓                        │    │
│ │ Approved by: HR Manager             │    │
│ └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

**Components:**
- Apply leave button (all users)
- Leave request cards:
  - Leave type
  - Date range
  - Status badge
  - Reason
  - Approval/rejection info
  - Action buttons (HR/Team Lead)

**Apply Leave Modal:**
```
┌─────────────────────────────┐
│ Apply for Leave             │
├─────────────────────────────┤
│ Leave Type: [Casual ▼]      │
│ Start Date: [📅]            │
│ End Date: [📅]              │
│ Reason: [____________]      │
│         [____________]      │
│                             │
│ [Cancel] [Submit]           │
└─────────────────────────────┘
```

**Actions:**
- **All Users:**
  - Apply leave
  - View own leave history
  - Cancel pending request
- **HR/Team Lead:**
  - Approve/reject leave
  - View all team leave requests
  - Add rejection reason

**States:**
- Pending: Yellow badge, awaiting approval
- Approved: Green badge
- Rejected: Red badge with reason

### 2.2.6 AI Assistant Page

**URL:** `/ai-assistant`  
**Access:** All roles

**Layout:**
```
┌─────────────────────────────────────────────┐
│ AI Assistant                                 │
│ Get help with tasks, reports, and more      │
├─────────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐    │
│ │ WorkforceOS AI                      │    │
│ ├─────────────────────────────────────┤    │
│ │                                     │    │
│ │ [AI] Hello! I'm here to help.      │    │
│ │                                     │    │
│ │ [USER] Can you explain my task?    │    │
│ │                                     │    │
│ │ [AI] Sure! The task "Fix bug"      │    │
│ │      involves...                    │    │
│ │                                     │    │
│ │                                     │    │
│ │                                     │    │
│ ├─────────────────────────────────────┤    │
│ │ [_____________________] [Send →]    │    │
│ └─────────────────────────────────────┘    │
│                                              │
│ Quick Actions:                               │
│ [Rewrite] [Generate Report] [Explain Task]  │
└─────────────────────────────────────────────┘
```

**Components:**
- Chat window:
  - Message bubbles (user vs AI)
  - Typing indicator
  - Timestamp
- Input area:
  - Text input
  - Send button
- Quick actions bar:
  - Pre-defined AI actions
  - Context-aware suggestions

**Actions:**
- Send message → AI processes and responds
- Quick action → Opens contextual modal/executes action
- View history → Past conversations

**AI Context (Role-based):**
- **Employee:** Can ask about own tasks, leave, attendance
- **Team Lead:** Can ask about team performance, workload
- **HR:** Can ask for reports, analytics, predictions

---

# 3. NAVIGATION BLUEPRINT

## 3.1 Global Navigation Structure

### Top Bar (Persistent)
```
┌────────────────────────────────────────────────┐
│ [☰] WorkforceOS | [🔍 Search] | [🔔] [👤]     │
└────────────────────────────────────────────────┘
```

**Components:**
- Logo: Click → Dashboard
- Global search: Quick access to users, tasks, documents
- Notifications bell: Unread count badge
- Profile menu:
  - User name + role badge
  - Settings
  - Profile
  - Logout

### Sidebar (Role-Based)

**HR/Admin Sidebar:**
```
├─ Dashboard
├─ Employees
├─ Tasks
├─ Attendance
├─ Leave
├─ Announcements
├─ AI Assistant
└─ Settings (Admin only)
```

**Team Lead Sidebar:**
```
├─ Dashboard
├─ Team
├─ Tasks
├─ Attendance
├─ Leave
├─ Announcements
└─ AI Assistant
```

**Employee/Intern Sidebar:**
```
├─ Dashboard
├─ Tasks
├─ Attendance
├─ Leave
├─ Announcements
└─ AI Assistant
```

## 3.2 Navigation Patterns

### Primary Navigation
- Sidebar for module access
- Always visible on desktop
- Collapsible on mobile (hamburger menu)

### Secondary Navigation
- Breadcrumbs for deep navigation
- Tabs for sub-sections within modules

### Contextual Navigation
- Action buttons (top right)
- Quick actions FAB (bottom right)
- Right-click context menus (Phase 2)

## 3.3 Mobile vs Desktop Mapping

| Feature | Desktop | Mobile |
|---------|---------|--------|
| Sidebar | Always visible | Hamburger menu |
| Top bar | Full width | Compact, icons only |
| Cards | Grid layout | Stacked list |
| Tables | Full table | Horizontal scroll |
| Modals | Center overlay | Full screen |
| FAB | Bottom right | Bottom center |

---

# 4. UX FLOW DIAGRAMS

## 4.1 Login Flow

```
START
  ↓
[Login Page]
  ↓
Enter credentials
  ↓
Valid? ─NO→ [Error: Invalid credentials] → RETRY
  ↓ YES
Fetch user profile
  ↓
Check role
  ├─ Admin/HR → Navigate to /hr-dashboard
  ├─ Team Lead → Navigate to /team-dashboard
  └─ Employee/Intern → Navigate to /dashboard
  ↓
[Dashboard loaded]
  ↓
END
```

## 4.2 Task Assignment Flow (HR/Team Lead)

```
START
  ↓
[Tasks Page]
  ↓
Click "Create Task"
  ↓
[Task Creation Modal]
  ├─ Enter title
  ├─ Enter description
  ├─ Select assignee
  ├─ Set priority
  ├─ Set deadline
  └─ Click "Create"
  ↓
AI checks workload
  ↓
Assignee overloaded? ─YES→ [AI Warning: Suggest alternative] → Confirm?
  ↓ NO                                                           ↓ YES/NO
Task created                                                    Reassign or Proceed
  ↓
Notification sent to assignee
  ↓
[Tasks Page updated]
  ↓
END
```

## 4.3 Leave Application Flow (Employee)

```
START
  ↓
[Leave Page]
  ↓
Click "Apply Leave"
  ↓
[Leave Application Modal]
  ├─ Select leave type
  ├─ Select start date
  ├─ Select end date
  └─ Enter reason
  ↓
Click "Submit"
  ↓
AI checks:
  ├─ Date conflicts?
  ├─ Leave balance?
  └─ Team coverage?
  ↓
Conflicts? ─YES→ [AI Alert: Cannot approve] → Show reason → CANCEL or EDIT
  ↓ NO
Leave request created (PENDING)
  ↓
AI decision:
  ├─ Within policy → Auto-approve → Status = APPROVED
  └─ Requires review → Status = PENDING → Notify HR/Team Lead
  ↓
Notification sent to employee
  ↓
[Leave Page updated]
  ↓
END
```

## 4.4 Attendance Check-In Flow

```
START
  ↓
[Attendance Page]
  ↓
Select work mode (WFO/WFH/Hybrid)
  ↓
Click "Check In"
  ↓
Record timestamp
  ↓
AI checks:
  ├─ Unusual time? → Flag for review
  └─ Within schedule? → Mark present
  ↓
Attendance record created
  ↓
[Success: Checked in at HH:MM]
  ↓
Show "Check Out" button
  ↓
END
```

## 4.5 AI-Assisted Workflow: Auto-Nudge Intern

```
TRIGGER: Task deadline approaching
  ↓
AI checks:
  ├─ Task progress < 50%
  └─ Deadline within 24 hours
  ↓
Condition met? ─NO→ END
  ↓ YES
AI sends nudge notification
  ↓
"Your task XYZ is due soon. Current progress: 30%"
  ↓
Wait 4 hours
  ↓
Progress updated? ─YES→ END
  ↓ NO
AI escalates to team lead
  ↓
"Intern needs help with task XYZ"
  ↓
Team lead notified
  ↓
END
```

## 4.6 HR Approval Flow

```
START
  ↓
[Leave Requests Queue]
  ↓
Click leave request
  ↓
[Leave Details Modal]
  ├─ View employee
  ├─ View dates
  ├─ View reason
  └─ AI recommendation: "Approve" or "Review"
  ↓
HR decision:
  ├─ Approve → Update status to APPROVED
  └─ Reject → Enter reason → Update status to REJECTED
  ↓
Notification sent to employee
  ↓
[Queue updated]
  ↓
END
```

## 4.7 AI Report Generation Flow

```
START
  ↓
[AI Assistant Page]
  ↓
User: "Generate weekly attendance report"
  ↓
AI parses request
  ↓
AI fetches attendance data (last 7 days)
  ↓
AI analyzes:
  ├─ Total present
  ├─ Total absent
  ├─ Average check-in time
  └─ Anomalies
  ↓
AI generates report (markdown)
  ↓
Display in chat
  ↓
[Download as PDF] button
  ↓
END
```

---

# 5. FULL UI SCREEN SPECIFICATIONS

## 5.1 Login Screen

**Route:** `/login`

**Layout Wireframe:**
```
┌────────────────────────────────────┐
│                                    │
│         [Grid Pattern BG]          │
│                                    │
│     ┌────────────────────┐        │
│     │  WorkforceOS       │        │
│     │  Enterprise...     │        │
│     │                    │        │
│     │  Email             │        │
│     │  [____________]    │        │
│     │                    │        │
│     │  Password          │        │
│     │  [____________]    │        │
│     │                    │        │
│     │  [Sign In →]       │        │
│     │                    │        │
│     │  No account?       │        │
│     │  Register          │        │
│     └────────────────────┘        │
│                                    │
└────────────────────────────────────┘
```

**Components:**
- Card (max-width: 400px, center aligned)
- Logo/Title (text-3xl, font-bold)
- Subtitle (text-sm, muted)
- Input fields (email, password)
- Submit button (full-width, primary)
- Link to register

**States:**
- Default
- Loading (spinner on button)
- Error (red border + error message)
- Success (redirect)

**Interactions:**
- Enter key → Submit
- Tab navigation between fields

## 5.2 HR Dashboard Screen

**Route:** `/hr-dashboard`

**Layout Wireframe:**
```
┌─────────────────────────────────────────────────────┐
│ [☰] WorkforceOS    [Search]         [🔔] [Profile] │
├───────┬─────────────────────────────────────────────┤
│       │ HR Dashboard                                │
│ Nav   │ Manage your workforce operations            │
│ ─     ├─────────────────────────────────────────────┤
│ Dash  │ ┌────────┐┌────────┐┌────────┐┌────────┐  │
│ Emp   │ │ 245    ││ 892    ││ 12     ││ 231    │  │
│ Tasks │ │ Total  ││ Total  ││ Pending││ Present│  │
│ Att.  │ │ Emp.   ││ Tasks  ││ Leaves ││ Today  │  │
│ Leave │ └────────┘└────────┘└────────┘└────────┘  │
│ Ann.  │                                             │
│ AI    │ ┌────────────────────────────────────────┐ │
│       │ │ Pending Approvals                      │ │
│       │ │ ───────────────                        │ │
│       │ │ • Leave Requests (12)      [View All]  │ │
│       │ │ • Attendance Corrections   [View All]  │ │
│       │ │ • Document Verifications   [View All]  │ │
│       │ └────────────────────────────────────────┘ │
│       │                                             │
│       │ ┌────────────────────────────────────────┐ │
│       │ │ AI Insights                            │ │
│       │ │ ───────────                            │ │
│       │ │ ⚠ High attrition risk in Engineering   │ │
│       │ │   team. View details →                 │ │
│       │ │ 📊 Attendance anomaly detected for     │ │
│       │ │   John Doe. Review →                   │ │
│       │ └────────────────────────────────────────┘ │
│       │                                             │
│       │                                        [+]  │
└───────┴─────────────────────────────────────────────┘
```

**Components:**
- Stat Cards (4):
  - Icon
  - Number (large)
  - Label (small)
  - Hover: slight elevation
- Pending Approvals Card:
  - Title
  - List of approval types with counts
  - "View All" link
- AI Insights Card:
  - Title
  - Alert items with icons
  - Action links
- FAB (bottom right): Quick actions

**States:**
- Loading: Skeleton cards
- Empty state: "No pending approvals"
- Error: Retry banner

**Interactions:**
- Click stat card → Navigate to detail
- Click approval → Open modal
- Click insight → Detail view

## 5.3 Task Management Screen

**Route:** `/tasks`

**Layout Wireframe:**
```
┌─────────────────────────────────────────────────────┐
│ [☰] WorkforceOS    [Search]         [🔔] [Profile] │
├───────┬─────────────────────────────────────────────┤
│       │ Tasks                      [+ Create Task]  │
│ Nav   ├─────────────────────────────────────────────┤
│ ─     │ [Status ▼][Priority ▼][Assignee ▼][View ▼] │
│       ├─────────────────────────────────────────────┤
│       │                                             │
│       │ ┌────────────────────────────────────────┐ │
│       │ │ Fix authentication bug                  │ │
│       │ │ [IN_PROGRESS] [HIGH]                   │ │
│       │ │                                        │ │
│       │ │ Assigned: John Doe                     │ │
│       │ │ Deadline: Jan 15, 2025                 │ │
│       │ │                                        │ │
│       │ │ Progress: 60%                          │ │
│       │ │ [======--------]                       │ │
│       │ │                                        │ │
│       │ │ [View Details] [Update Progress]       │ │
│       │ └────────────────────────────────────────┘ │
│       │                                             │
│       │ ┌────────────────────────────────────────┐ │
│       │ │ Design new dashboard                    │ │
│       │ │ [TODO] [MEDIUM]                        │ │
│       │ │                                        │ │
│       │ │ Assigned: Jane Smith                   │ │
│       │ │ Deadline: Jan 20, 2025                 │ │
│       │ │                                        │ │
│       │ │ Progress: 10%                          │ │
│       │ │ [=------------]                        │ │
│       │ │                                        │ │
│       │ │ [View Details] [Update Progress]       │ │
│       │ └────────────────────────────────────────┘ │
└───────┴─────────────────────────────────────────────┘
```

**Components:**
- Filter bar:
  - Dropdowns for Status, Priority, Assignee
  - Date range picker
  - View toggle (Grid/List/Kanban)
- Task cards:
  - Title
  - Status badge (color-coded)
  - Priority badge (color-coded)
  - Assignee info (avatar + name)
  - Deadline
  - Progress bar (interactive slider)
  - Action buttons

**States:**
- Empty: "No tasks yet"
- Filtered empty: "No tasks match filters"
- Loading: Skeleton cards

**Interactions:**
- Drag progress slider → Update task
- Click "View Details" → Modal
- Click "Create Task" → Creation modal

## 5.4 Create Task Modal

**Triggered by:** "Create Task" button

**Layout:**
```
┌─────────────────────────────────────┐
│ Create New Task              [X]    │
├─────────────────────────────────────┤
│ Task Title *                        │
│ [_____________________________]     │
│                                     │
│ Description                         │
│ [_____________________________]     │
│ [_____________________________]     │
│                                     │
│ Assign To *                         │
│ [Select user ▼______________ ]     │
│                                     │
│ Priority *                          │
│ [Medium ▼___________________]      │
│                                     │
│ Deadline                            │
│ [📅 Select date_____________]      │
│                                     │
│ AI Suggestion:                      │
│ ℹ John Doe has 8 pending tasks.    │
│   Consider assigning to Jane Smith. │
│                                     │
│         [Cancel]  [Create Task]     │
└─────────────────────────────────────┘
```

**Components:**
- Input: Task title
- Textarea: Description
- Dropdown: Assignee (searchable)
- Dropdown: Priority
- Date picker: Deadline
- AI suggestion box (conditional)
- Action buttons

**Validation:**
- Title: Required, 3-100 chars
- Assignee: Required
- Priority: Required

**AI Behavior:**
- After selecting assignee, AI checks workload
- If overloaded, shows suggestion
- User can proceed or reassign

## 5.5 AI Assistant Screen

**Route:** `/ai-assistant`

**Layout Wireframe:**
```
┌─────────────────────────────────────────────────────┐
│ [☰] WorkforceOS    [Search]         [🔔] [Profile] │
├───────┬─────────────────────────────────────────────┤
│       │ AI Assistant                                │
│ Nav   │ Get help with tasks, reports, and more      │
│ ─     ├─────────────────────────────────────────────┤
│       │ ┌────────────────────────────────────────┐ │
│       │ │ WorkforceOS AI                    [···]│ │
│       │ ├────────────────────────────────────────┤ │
│       │ │                                        │ │
│       │ │ [AI] 🤖                                │ │
│       │ │ Hello! I'm your AI assistant.         │ │
│       │ │ How can I help you today?             │ │
│       │ │                                        │ │
│       │ │                            [USER] 👤   │ │
│       │ │                Can you explain my task?│ │
│       │ │                                        │ │
│       │ │ [AI] 🤖                                │ │
│       │ │ Sure! The task "Fix authentication    │ │
│       │ │ bug" involves investigating the       │ │
│       │ │ login flow and...                     │ │
│       │ │                                        │ │
│       │ │                                        │ │
│       │ ├────────────────────────────────────────┤ │
│       │ │ [Type your message...     ] [Send →]  │ │
│       │ └────────────────────────────────────────┘ │
│       │                                             │
│       │ Quick Actions:                              │
│       │ [Rewrite Text] [Generate Report]            │
│       │ [Explain Task] [Suggest Breakdown]          │
└───────┴─────────────────────────────────────────────┘
```

**Components:**
- Chat window:
  - Message bubbles (user vs AI)
  - Avatars/icons
  - Timestamps
  - Typing indicator (...)
- Input bar:
  - Text input (multi-line)
  - Send button
- Quick actions:
  - Pre-defined action buttons
  - Context-aware (based on user role)

**States:**
- Empty: Welcome message + suggestions
- Chatting: Message history
- Loading: Typing indicator
- Error: "Failed to send message. Retry?"

**Interactions:**
- Type message + Enter → Send
- Click quick action → Pre-fill input or execute
- Scroll up → Load history

---

# 6. ENTERPRISE UI SYSTEM SPECIFICATION

## 6.1 Typography Scale

### Font Families
```css
--font-heading: 'Space Grotesk', sans-serif;
--font-body: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
```

### Type Scale
```
H1: 36px / 44px (3rem / 1.2)
H2: 30px / 38px (2.5rem / 1.27)
H3: 24px / 32px (2rem / 1.33)
H4: 20px / 28px (1.67rem / 1.4)
H5: 18px / 26px (1.5rem / 1.44)
H6: 16px / 24px (1.33rem / 1.5)

Body Large: 18px / 28px
Body: 16px / 24px
Body Small: 14px / 20px
Caption: 12px / 16px
```

### Font Weights
```
Light: 300
Regular: 400
Medium: 500
Semibold: 600
Bold: 700
```

## 6.2 Color System

### Primary Palette
```
Primary: #8B5CF6 (Purple)
Primary Light: #A78BFA
Primary Dark: #7C3AED
Primary Foreground: #FFFFFF

Secondary: #F3F4F6 (Gray)
Secondary Foreground: #1F2937
```

### Semantic Colors
```
Success: #10B981 (Green)
Warning: #F59E0B (Amber)
Error: #EF4444 (Red)
Info: #3B82F6 (Blue)
```

### Neutral Scale
```
Gray 50: #F9FAFB
Gray 100: #F3F4F6
Gray 200: #E5E7EB
Gray 300: #D1D5DB
Gray 400: #9CA3AF
Gray 500: #6B7280
Gray 600: #4B5563
Gray 700: #374151
Gray 800: #1F2937
Gray 900: #111827
```

### Background & Surfaces
```
Background: #FFFFFF
Surface: #F9FAFB
Surface Elevated: #FFFFFF (shadow)
Border: #E5E7EB
```

### Status Colors
```
Status Pending: #F59E0B (Amber)
Status In Progress: #3B82F6 (Blue)
Status Completed: #10B981 (Green)
Status Blocked: #EF4444 (Red)
Status Cancelled: #6B7280 (Gray)
```

## 6.3 Spacing Scale

```
xs: 4px (0.25rem)
sm: 8px (0.5rem)
md: 16px (1rem)
lg: 24px (1.5rem)
xl: 32px (2rem)
2xl: 48px (3rem)
3xl: 64px (4rem)
4xl: 96px (6rem)
```

## 6.4 Elevation (Shadows)

```
Elevation 1: 0 1px 2px rgba(0,0,0,0.05)
Elevation 2: 0 2px 4px rgba(0,0,0,0.06)
Elevation 3: 0 4px 6px rgba(0,0,0,0.07)
Elevation 4: 0 8px 16px rgba(0,0,0,0.08)
Elevation 5: 0 16px 32px rgba(0,0,0,0.1)
```

## 6.5 Border Radius

```
None: 0
sm: 4px
md: 8px
lg: 12px
xl: 16px
Full: 9999px (pill)
```

## 6.6 Component Tokens

### Button
```
Height: 40px (md), 32px (sm), 48px (lg)
Padding: 16px 24px (md)
Border Radius: 8px
Font Weight: 500
Transition: all 0.2s ease
```

### Input
```
Height: 40px (md)
Padding: 8px 12px
Border: 1px solid Gray 300
Border Radius: 8px
Focus: Primary border + ring
```

### Card
```
Background: Surface
Border: 1px solid Border
Border Radius: 12px
Padding: 24px
Shadow: Elevation 2
Hover: Elevation 3
```

### Badge
```
Padding: 2px 8px
Font Size: 12px
Border Radius: 9999px (pill)
Font Weight: 500
```

## 6.7 Iconography

**Library:** Lucide React

**Sizes:**
```
Small: 16px
Medium: 20px
Large: 24px
XLarge: 32px
```

**Common Icons:**
- Dashboard: LayoutDashboard
- Tasks: CheckSquare
- Users: Users
- Attendance: Calendar
- Leave: FileText
- Announcements: MessageCircle
- AI: Briefcase
- Settings: Settings
- Logout: LogOut
- Edit: Edit
- Delete: Trash
- Add: Plus
- Search: Search
- Filter: Filter
- Sort: ArrowUpDown

## 6.8 Motion & Animation

### Transitions
```
Fast: 150ms
Normal: 200ms
Slow: 300ms
Easing: cubic-bezier(0.4, 0, 0.2, 1)
```

### Animations
```
Fade In: opacity 0 → 1 (200ms)
Slide In: translateY(10px) → 0 (200ms)
Scale: scale(0.95) → 1 (200ms)
Spin: rotate(0deg) → 360deg (1000ms loop)
```

### Hover States
```
Button: scale(1.02) + shadow elevation
Card: translateY(-2px) + shadow elevation
Link: color change (200ms)
```

## 6.9 Responsive Breakpoints

```
Mobile: 0-639px
Tablet: 640px-1023px
Desktop: 1024px-1279px
Desktop HD: 1280px+
```

### Grid System
```
Mobile: 1 column
Tablet: 2 columns
Desktop: 3-4 columns
Desktop HD: 4-6 columns
```

---

# 7. COMPONENT LIBRARY SPECIFICATION

## 7.1 Core Components

### Button

**Props:**
- `variant`: 'default' | 'secondary' | 'outline' | 'ghost' | 'destructive'
- `size`: 'sm' | 'md' | 'lg'
- `disabled`: boolean
- `loading`: boolean
- `icon`: ReactNode (optional)
- `onClick`: () => void

**States:**
- Default
- Hover
- Active
- Disabled
- Loading

**Usage:**
```jsx
<Button variant="default" size="md">
  <Plus className="mr-2 h-4 w-4" />
  Create Task
</Button>
```

### Card

**Props:**
- `className`: string
- `children`: ReactNode
- `hoverable`: boolean

**Slots:**
- CardHeader
- CardTitle
- CardDescription
- CardContent
- CardFooter

**States:**
- Default
- Hover (if hoverable)

**Usage:**
```jsx
<Card hoverable>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

### Input

**Props:**
- `type`: 'text' | 'email' | 'password' | 'number' | 'date'
- `placeholder`: string
- `value`: string
- `onChange`: (e) => void
- `disabled`: boolean
- `error`: boolean
- `helperText`: string

**States:**
- Default
- Focus
- Error
- Disabled

**Usage:**
```jsx
<Input
  type="email"
  placeholder="john@company.com"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={!!emailError}
  helperText={emailError}
/>
```

### Select

**Props:**
- `options`: Array<{value: string, label: string}>
- `value`: string
- `onValueChange`: (value: string) => void
- `placeholder`: string
- `disabled`: boolean

**States:**
- Closed
- Open
- Selected

**Usage:**
```jsx
<Select value={priority} onValueChange={setPriority}>
  <SelectTrigger>
    <SelectValue placeholder="Select priority" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="low">Low</SelectItem>
    <SelectItem value="medium">Medium</SelectItem>
    <SelectItem value="high">High</SelectItem>
  </SelectContent>
</Select>
```

### Badge

**Props:**
- `variant`: 'default' | 'success' | 'warning' | 'error' | 'info'
- `children`: ReactNode

**Usage:**
```jsx
<Badge variant="success">Approved</Badge>
<Badge variant="warning">Pending</Badge>
```

### Progress

**Props:**
- `value`: number (0-100)
- `className`: string

**Usage:**
```jsx
<Progress value={60} className="h-2" />
```

### Dialog/Modal

**Props:**
- `open`: boolean
- `onOpenChange`: (open: boolean) => void
- `children`: ReactNode

**Slots:**
- DialogTrigger
- DialogContent
- DialogHeader
- DialogTitle
- DialogDescription
- DialogFooter

**Usage:**
```jsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogTrigger asChild>
    <Button>Open Modal</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
    <div>Content</div>
    <DialogFooter>
      <Button>Save</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## 7.2 Custom Components

### StatCard

**Props:**
- `title`: string
- `value`: string | number
- `subtitle`: string
- `icon`: ReactNode
- `onClick`: () => void

**Usage:**
```jsx
<StatCard
  title="Total Tasks"
  value={892}
  subtitle="All tasks"
  icon={<CheckSquare />}
  onClick={() => navigate('/tasks')}
/>
```

### TaskCard

**Props:**
- `task`: Task object
- `onUpdate`: (task: Task) => void
- `canEdit`: boolean

**Slots:**
- Title
- Status badge
- Priority badge
- Progress bar
- Actions

**Usage:**
```jsx
<TaskCard
  task={task}
  onUpdate={handleUpdate}
  canEdit={user.role === 'hr'}
/>
```

### AttendanceRecord

**Props:**
- `record`: Attendance object
- `onCorrect`: (id: string) => void
- `canCorrect`: boolean

**Usage:**
```jsx
<AttendanceRecord
  record={attendance}
  onCorrect={handleCorrect}
  canCorrect={true}
/>
```

### LeaveRequestCard

**Props:**
- `leave`: Leave object
- `onApprove`: (id: string) => void
- `onReject`: (id: string, reason: string) => void
- `canApprove`: boolean

**Usage:**
```jsx
<LeaveRequestCard
  leave={leaveRequest}
  onApprove={handleApprove}
  onReject={handleReject}
  canApprove={user.role === 'hr'}
/>
```

### ChatMessage

**Props:**
- `role`: 'user' | 'assistant'
- `content`: string
- `timestamp`: Date

**Usage:**
```jsx
<ChatMessage
  role="user"
  content="Can you help me?"
  timestamp={new Date()}
/>
```

### NotificationItem

**Props:**
- `notification`: Notification object
- `onRead`: (id: string) => void
- `onDismiss`: (id: string) => void

**Usage:**
```jsx
<NotificationItem
  notification={notif}
  onRead={handleRead}
  onDismiss={handleDismiss}
/>
```

---

# 8. FULL DATA MODEL & ER DIAGRAM

## 8.1 Collections/Tables

### Users
```
Collection: users

Fields:
- id: String (UUID, PK)
- email: String (unique, indexed)
- password: String (hashed)
- name: String
- role: Enum [admin, hr, team_lead, employee, intern]
- department_id: String (FK → departments.id, nullable)
- manager_id: String (FK → users.id, nullable)
- is_active: Boolean (default: true)
- phone: String (nullable)
- avatar_url: String (nullable)
- created_at: DateTime
- updated_at: DateTime

Indexes:
- email (unique)
- role
- department_id
- is_active

Constraints:
- email must be valid format
- role must be valid enum value
- manager_id must reference existing user
```

### Departments
```
Collection: departments

Fields:
- id: String (UUID, PK)
- name: String (unique)
- description: String (nullable)
- head_id: String (FK → users.id, nullable)
- created_at: DateTime
- updated_at: DateTime

Indexes:
- name (unique)

Constraints:
- name required
```

### Tasks
```
Collection: tasks

Fields:
- id: String (UUID, PK)
- title: String
- description: String (nullable)
- assigned_to: String (FK → users.id, indexed)
- created_by: String (FK → users.id, indexed)
- status: Enum [todo, in_progress, completed, blocked]
- priority: Enum [low, medium, high, urgent]
- progress: Integer (0-100)
- deadline: DateTime (nullable)
- notes: String (nullable)
- parent_task_id: String (FK → tasks.id, nullable)
- created_at: DateTime
- updated_at: DateTime

Indexes:
- assigned_to
- created_by
- status
- deadline
- priority

Constraints:
- progress between 0-100
- status valid enum
- priority valid enum
```

### Attendance
```
Collection: attendance

Fields:
- id: String (UUID, PK)
- user_id: String (FK → users.id, indexed)
- date: String (YYYY-MM-DD, indexed)
- check_in: DateTime (nullable)
- check_out: DateTime (nullable)
- status: Enum [present, absent, half_day, late, wfh]
- work_mode: Enum [wfo, wfh, hybrid]
- notes: String (nullable)
- correction_requested: Boolean (default: false)
- correction_reason: String (nullable)
- corrected_by: String (FK → users.id, nullable)
- created_at: DateTime
- updated_at: DateTime

Indexes:
- user_id + date (compound, unique)
- date
- status

Constraints:
- date required
- user_id required
- unique per user per date
```

### Leave
```
Collection: leaves

Fields:
- id: String (UUID, PK)
- user_id: String (FK → users.id, indexed)
- leave_type: Enum [sick, casual, earned, unpaid]
- start_date: String (YYYY-MM-DD)
- end_date: String (YYYY-MM-DD)
- reason: String
- status: Enum [pending, approved, rejected, cancelled]
- approved_by: String (FK → users.id, nullable)
- rejection_reason: String (nullable)
- created_at: DateTime
- updated_at: DateTime

Indexes:
- user_id
- status
- start_date
- end_date

Constraints:
- end_date >= start_date
- reason required
```

### Announcements
```
Collection: announcements

Fields:
- id: String (UUID, PK)
- title: String
- content: String (text, not limited)
- created_by: String (FK → users.id, indexed)
- target_roles: Array<String> (empty = all roles)
- is_pinned: Boolean (default: false)
- created_at: DateTime
- updated_at: DateTime

Indexes:
- created_by
- is_pinned
- created_at (descending)

Constraints:
- title required
- content required
```

### AI_Messages
```
Collection: ai_messages

Fields:
- id: String (UUID, PK)
- user_id: String (FK → users.id, indexed)
- session_id: String (indexed)
- message: String (user's message)
- response: String (AI response)
- action_type: String (nullable) [rewrite, explain, breakdown, report]
- context: JSON (nullable, stores context data)
- created_at: DateTime

Indexes:
- user_id
- session_id
- created_at

Constraints:
- message required
- response required
```

### Notifications
```
Collection: notifications

Fields:
- id: String (UUID, PK)
- user_id: String (FK → users.id, indexed)
- type: Enum [task, leave, attendance, announcement, system]
- title: String
- message: String
- link: String (nullable, URL to relevant resource)
- is_read: Boolean (default: false)
- created_at: DateTime

Indexes:
- user_id + is_read (compound)
- created_at (descending)

Constraints:
- user_id required
- type required
```

### Audit_Logs
```
Collection: audit_logs

Fields:
- id: String (UUID, PK)
- user_id: String (FK → users.id, indexed, nullable)
- action: String (e.g., 'user.created', 'leave.approved')
- resource_type: String (e.g., 'user', 'task', 'leave')
- resource_id: String (ID of affected resource)
- old_value: JSON (nullable)
- new_value: JSON (nullable)
- ip_address: String (nullable)
- user_agent: String (nullable)
- created_at: DateTime

Indexes:
- user_id
- action
- resource_type
- created_at

Constraints:
- action required
- resource_type required
```

## 8.2 Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ PK  id          │
│     email       │
│     role        │
│ FK  dept_id     │──┐
│ FK  manager_id  │──┘
└─────────────────┘
         │
         │ 1:N
         │
    ┌────┴────┬────────┬────────┬──────────┬──────────┐
    │         │        │        │          │          │
    ▼         ▼        ▼        ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐
│ Tasks  │ │Leave │ │Attend. │ │Announc.│ │AI_Msgs   │ │Notifs    │
├────────┤ ├──────┤ ├────────┤ ├────────┤ ├──────────┤ ├──────────┤
│PK id   │ │PK id │ │PK id   │ │PK id   │ │PK id     │ │PK id     │
│FK user │ │FK user│ │FK user │ │FK user │ │FK user   │ │FK user   │
└────────┘ └──────┘ └────────┘ └────────┘ └──────────┘ └──────────┘

┌─────────────────┐
│  Departments    │
├─────────────────┤
│ PK  id          │
│     name        │
│ FK  head_id     │───→ Users
└─────────────────┘
```

## 8.3 Data Model Notes

**Audit Trail:**
- All tables have `created_at` and `updated_at`
- Critical actions logged in `audit_logs`

**Soft Deletes:**
- Users: `is_active` flag instead of deletion
- Tasks: Status changed to 'cancelled' instead of deletion

**Multi-Tenancy (Phase 2):**
- Add `tenant_id` to all collections
- Compound index: `tenant_id + other_indexes`
- Row-level security in queries

---

# 9. BACKEND API CONTRACT

## 9.1 Authentication APIs

### POST /api/auth/register
**Description:** Register new user

**Request:**
```json
{
  "email": "john@company.com",
  "name": "John Doe",
  "password": "password123",
  "role": "employee",
  "department_id": "uuid" (optional)
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "john@company.com",
  "name": "John Doe",
  "role": "employee",
  "created_at": "2025-01-10T10:00:00Z"
}
```

**Errors:**
- 400: Email already exists
- 400: Invalid email format
- 400: Invalid role

---

### POST /api/auth/login
**Description:** Login user

**Request:**
```json
{
  "email": "john@company.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "jwt_token",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "john@company.com",
    "name": "John Doe",
    "role": "employee"
  }
}
```

**Errors:**
- 401: Invalid credentials
- 403: Account inactive

---

### GET /api/auth/me
**Description:** Get current user profile

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "john@company.com",
  "name": "John Doe",
  "role": "employee",
  "department_id": "uuid",
  "created_at": "2025-01-10T10:00:00Z"
}
```

**Errors:**
- 401: Invalid/expired token

---

## 9.2 User Management APIs

### GET /api/users
**Description:** Get all users (HR/Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Params:**
- `role`: Filter by role
- `department_id`: Filter by department
- `is_active`: Filter by active status
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 50)

**Response (200):**
```json
{
  "users": [
    {
      "id": "uuid",
      "email": "john@company.com",
      "name": "John Doe",
      "role": "employee",
      "department_id": "uuid",
      "is_active": true,
      "created_at": "2025-01-10T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 245
  }
}
```

**Errors:**
- 403: Insufficient permissions

---

### GET /api/users/{user_id}
**Description:** Get user by ID

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "john@company.com",
  "name": "John Doe",
  "role": "employee",
  "department_id": "uuid",
  "manager_id": "uuid",
  "created_at": "2025-01-10T10:00:00Z"
}
```

**Errors:**
- 404: User not found

---

## 9.3 Task Management APIs

### POST /api/tasks
**Description:** Create task (HR/Team Lead only)

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "Fix bug",
  "description": "Description here",
  "assigned_to": "user_uuid",
  "priority": "high",
  "deadline": "2025-01-15T00:00:00Z" (optional)
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "title": "Fix bug",
  "assigned_to": "user_uuid",
  "created_by": "user_uuid",
  "status": "todo",
  "priority": "high",
  "progress": 0,
  "deadline": "2025-01-15T00:00:00Z",
  "created_at": "2025-01-10T10:00:00Z"
}
```

**Errors:**
- 403: Insufficient permissions
- 400: Invalid assignee
- 400: Invalid priority

---

### GET /api/tasks
**Description:** Get tasks (filtered by role)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Params:**
- `status`: Filter by status
- `priority`: Filter by priority
- `assigned_to`: Filter by assignee (HR/Team Lead)
- `page`: Page number
- `limit`: Items per page

**Response (200):**
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "Fix bug",
      "assigned_to": "user_uuid",
      "status": "in_progress",
      "priority": "high",
      "progress": 60,
      "deadline": "2025-01-15T00:00:00Z"
    }
  ],
  "pagination": {...}
}
```

---

### PATCH /api/tasks/{task_id}
**Description:** Update task

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "status": "in_progress" (optional),
  "progress": 60 (optional),
  "notes": "Progress update" (optional)
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "title": "Fix bug",
  "status": "in_progress",
  "progress": 60,
  "updated_at": "2025-01-10T11:00:00Z"
}
```

**Errors:**
- 403: Insufficient permissions
- 404: Task not found

---

## 9.4 Attendance APIs

### POST /api/attendance/check-in
**Description:** Check in for the day

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "work_mode": "wfo"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "date": "2025-01-10",
  "check_in": "2025-01-10T09:00:00Z",
  "status": "present",
  "work_mode": "wfo"
}
```

**Errors:**
- 400: Already checked in today

---

### POST /api/attendance/check-out
**Description:** Check out

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "notes": "Completed work" (optional)
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "check_in": "2025-01-10T09:00:00Z",
  "check_out": "2025-01-10T18:00:00Z"
}
```

**Errors:**
- 400: Not checked in yet
- 400: Already checked out

---

### GET /api/attendance
**Description:** Get attendance records

**Headers:**
```
Authorization: Bearer <token>
```

**Query Params:**
- `user_id`: Filter by user (HR/Team Lead)
- `start_date`: Date range start
- `end_date`: Date range end
- `page`: Page number
- `limit`: Items per page

**Response (200):**
```json
{
  "attendance": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "date": "2025-01-10",
      "check_in": "2025-01-10T09:00:00Z",
      "check_out": "2025-01-10T18:00:00Z",
      "status": "present",
      "work_mode": "wfo"
    }
  ],
  "pagination": {...}
}
```

---

## 9.5 Leave Management APIs

### POST /api/leave
**Description:** Apply for leave

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "leave_type": "casual",
  "start_date": "2025-01-15",
  "end_date": "2025-01-17",
  "reason": "Family event"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "leave_type": "casual",
  "start_date": "2025-01-15",
  "end_date": "2025-01-17",
  "reason": "Family event",
  "status": "pending",
  "created_at": "2025-01-10T10:00:00Z"
}
```

**Errors:**
- 400: Invalid date range
- 400: Overlapping leave exists

---

### GET /api/leave
**Description:** Get leave requests

**Headers:**
```
Authorization: Bearer <token>
```

**Query Params:**
- `user_id`: Filter by user (HR/Team Lead)
- `status`: Filter by status
- `page`: Page number
- `limit`: Items per page

**Response (200):**
```json
{
  "leaves": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "leave_type": "casual",
      "start_date": "2025-01-15",
      "end_date": "2025-01-17",
      "status": "pending",
      "created_at": "2025-01-10T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

---

### PATCH /api/leave/{leave_id}
**Description:** Approve/reject leave (HR/Team Lead only)

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "status": "approved",
  "rejection_reason": "Not approved" (optional, if rejected)
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "status": "approved",
  "approved_by": "uuid",
  "updated_at": "2025-01-10T11:00:00Z"
}
```

**Errors:**
- 403: Insufficient permissions
- 404: Leave not found

---

## 9.6 Announcement APIs

### POST /api/announcements
**Description:** Create announcement (HR/Admin only)

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "title": "Company Update",
  "content": "Content here...",
  "target_roles": ["employee", "intern"] (optional, empty = all)
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "title": "Company Update",
  "content": "Content here...",
  "created_by": "uuid",
  "target_roles": [],
  "created_at": "2025-01-10T10:00:00Z"
}
```

**Errors:**
- 403: Insufficient permissions

---

### GET /api/announcements
**Description:** Get announcements (filtered by role)

**Headers:**
```
Authorization: Bearer <token>
```

**Query Params:**
- `page`: Page number
- `limit`: Items per page

**Response (200):**
```json
{
  "announcements": [
    {
      "id": "uuid",
      "title": "Company Update",
      "content": "Content...",
      "created_at": "2025-01-10T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

---

## 9.7 AI APIs

### POST /api/ai/chat
**Description:** Send message to AI assistant

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "message": "Can you help me?",
  "session_id": "session_uuid" (optional),
  "action_type": "explain" (optional)
}
```

**Response (200):**
```json
{
  "response": "AI generated response...",
  "session_id": "session_uuid"
}
```

**Errors:**
- 500: AI service error

---

### GET /api/ai/history
**Description:** Get AI chat history

**Headers:**
```
Authorization: Bearer <token>
```

**Query Params:**
- `session_id`: Filter by session
- `page`: Page number
- `limit`: Items per page

**Response (200):**
```json
{
  "history": [
    {
      "id": "uuid",
      "message": "User message",
      "response": "AI response",
      "created_at": "2025-01-10T10:00:00Z"
    }
  ],
  "pagination": {...}
}
```

---

## 9.8 Dashboard APIs

### GET /api/dashboard/stats
**Description:** Get dashboard statistics (role-based)

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200) - HR:**
```json
{
  "total_employees": 245,
  "total_tasks": 892,
  "pending_leaves": 12,
  "present_today": 231
}
```

**Response (200) - Employee:**
```json
{
  "my_tasks": 8,
  "pending_tasks": 3,
  "completed_tasks": 5,
  "my_leaves": 2
}
```

---

# 10. STATE MACHINES

## 10.1 Task State Machine

```
States: [TODO, IN_PROGRESS, COMPLETED, BLOCKED]

Transitions:
  TODO → IN_PROGRESS (employee starts)
  TODO → BLOCKED (employee reports blocker)
  IN_PROGRESS → COMPLETED (employee finishes)
  IN_PROGRESS → BLOCKED (employee reports blocker)
  BLOCKED → IN_PROGRESS (blocker resolved)
  BLOCKED → TODO (reset)
  COMPLETED → IN_PROGRESS (reopen by HR/Team Lead)

Rules:
- Only assigned user can change status
- HR/Team Lead can change any status
- COMPLETED tasks cannot be deleted
- Progress must be 100% to mark COMPLETED

Events:
- on_status_change → notify creator
- on_blocked → notify team lead
- on_completed → notify creator + team lead
```

## 10.2 Leave State Machine

```
States: [PENDING, APPROVED, REJECTED, CANCELLED]

Transitions:
  PENDING → APPROVED (HR/Team Lead approves)
  PENDING → REJECTED (HR/Team Lead rejects)
  PENDING → CANCELLED (employee cancels)
  APPROVED → CANCELLED (employee cancels before start date)

Rules:
- Only HR/Team Lead can approve/reject
- Employee can cancel PENDING or APPROVED (before start date)
- REJECTED/CANCELLED leaves cannot change status
- Auto-approve if:
  * Leave < 2 days
  * No conflicts
  * Within balance

Events:
- on_approved → notify employee
- on_rejected → notify employee with reason
- on_cancelled → notify HR/Team Lead
```

## 10.3 Attendance State Machine

```
States: [ABSENT, PRESENT, HALF_DAY, LATE, WFH]

Transitions:
  ABSENT → PRESENT (check-in before deadline)
  ABSENT → LATE (check-in after deadline)
  PRESENT → HALF_DAY (early checkout)
  LATE → PRESENT (worked full hours)

Rules:
- Auto-mark ABSENT if no check-in by EOD
- LATE if check-in after 10:00 AM (configurable)
- HALF_DAY if < 4 hours worked
- WFH status set at check-in

Events:
- on_late → notify employee + team lead
- on_absent → AI flags for review (if pattern detected)
- on_correction_request → notify HR
```

## 10.4 AI Escalation State Machine

```
States: [MONITORING, FLAGGED, ESCALATED, RESOLVED]

Transitions:
  MONITORING → FLAGGED (AI detects issue)
  FLAGGED → ESCALATED (issue persists)
  FLAGGED → RESOLVED (issue fixed)
  ESCALATED → RESOLVED (manual resolution)

Rules:
- AI monitors all workflows
- FLAGGED if:
  * Task overdue > 2 days
  * Attendance anomaly (3+ late in week)
  * Leave conflicts
- ESCALATED if no action in 24 hours

Events:
- on_flagged → notify user
- on_escalated → notify manager + HR
- on_resolved → log resolution
```

---

# 11. AI/LLM INTEGRATION FRAMEWORK

## 11.1 AI Actions

### 1. Apply Leave (Auto)
**Trigger:** User submits leave request

**AI Steps:**
1. Check leave balance
2. Check date conflicts (with own leaves, holidays)
3. Check team coverage (how many on leave same dates)
4. Check policy compliance (notice period, min/max days)

**Decision:**
- Auto-approve if all checks pass
- Pending if team coverage < 50%
- Reject if conflict or insufficient balance

**Prompt Template:**
```
System: You are an AI HR assistant for leave management.
Context: {user_role}, {leave_balance}, {team_leaves}, {policy}
User Request: Leave from {start_date} to {end_date}, type: {leave_type}
Task: Analyze and decide: auto-approve, pending, or reject with reason.
```

---

### 2. Rewrite Announcement
**Trigger:** User requests rewrite

**AI Steps:**
1. Parse original content
2. Identify tone (formal, casual, urgent)
3. Rewrite with clarity + professional tone
4. Suggest improvements

**Prompt Template:**
```
System: You are a corporate communications expert.
User Request: Rewrite this announcement: "{original}"
Task: Rewrite in professional, clear language. Keep key info intact.
Output: Rewritten announcement.
```

---

### 3. Generate Report
**Trigger:** User requests report (e.g., "Generate weekly attendance report")

**AI Steps:**
1. Parse report type (attendance, tasks, leave)
2. Fetch relevant data
3. Analyze data (trends, anomalies)
4. Generate markdown report

**Prompt Template:**
```
System: You are a data analyst for workforce management.
Context: Data: {attendance_data}
User Request: Generate {report_type} report
Task: Analyze data, identify trends, create summary report in markdown.
Output: Report with sections: Summary, Trends, Anomalies, Recommendations.
```

---

### 4. Explain Task
**Trigger:** User asks "Explain my task"

**AI Steps:**
1. Fetch task details
2. Break down into sub-tasks
3. Suggest approach
4. Identify blockers

**Prompt Template:**
```
System: You are a task breakdown expert.
Context: Task: {task_title}, Description: {description}
User Request: Explain this task and suggest how to approach it.
Task: Break down into steps, suggest approach, warn of potential blockers.
```

---

### 5. Auto-Assign Task
**Trigger:** HR/Team Lead creates task without assignee

**AI Steps:**
1. Fetch team members
2. Check workload (pending tasks count)
3. Check skills (match task type)
4. Suggest best assignee

**Prompt Template:**
```
System: You are a task assignment optimizer.
Context: Team: {team_members}, Workload: {workload_data}, Task: {task_details}
Task: Suggest best assignee based on workload and skills.
Output: Assignee ID + reason.
```

---

## 11.2 AI Reasoning & Decision Trees

### Leave Approval Decision Tree
```
START
  ↓
Check Leave Balance
  ├─ Insufficient → REJECT ("Insufficient leave balance")
  └─ Sufficient → Continue
  ↓
Check Date Conflicts
  ├─ Conflict exists → REJECT ("You have leave/holiday on these dates")
  └─ No conflict → Continue
  ↓
Check Team Coverage
  ├─ > 50% team on leave → PENDING ("Requires manager approval")
  └─ < 50% team on leave → Continue
  ↓
Check Policy Compliance
  ├─ Notice period not met → PENDING ("Less than required notice")
  └─ Compliant → AUTO-APPROVE
```

### Task Assignment Decision Tree
```
START
  ↓
Get Team Members
  ↓
For each member:
  ├─ Calculate workload score
  ├─ Check skill match
  └─ Check availability
  ↓
Sort by:
  1. Lowest workload
  2. Highest skill match
  3. Available
  ↓
Return Top 3 Suggestions
```

## 11.3 AI Context Windows

### Context by Role

**HR:**
```json
{
  "role": "hr",
  "permissions": ["view_all", "approve_all", "create_all"],
  "data_access": {
    "users": "all",
    "tasks": "all",
    "attendance": "all",
    "leave": "all",
    "analytics": "all"
  },
  "ai_capabilities": [
    "generate_reports",
    "predict_attrition",
    "detect_anomalies",
    "suggest_policies"
  ]
}
```

**Team Lead:**
```json
{
  "role": "team_lead",
  "permissions": ["view_team", "approve_team_leave", "assign_tasks"],
  "data_access": {
    "users": "team_only",
    "tasks": "team_only",
    "attendance": "team_only",
    "leave": "team_only"
  },
  "ai_capabilities": [
    "suggest_task_assignment",
    "predict_team_burnout",
    "generate_team_report"
  ]
}
```

**Employee:**
```json
{
  "role": "employee",
  "permissions": ["view_own", "update_own"],
  "data_access": {
    "tasks": "own_only",
    "attendance": "own_only",
    "leave": "own_only"
  },
  "ai_capabilities": [
    "explain_task",
    "suggest_breakdown",
    "check_leave_eligibility"
  ]
}
```

## 11.4 Workflow Automation Logic

### Auto-Nudge Intern Workflow
```python
# Pseudo-code
async def auto_nudge_intern():
  # Find tasks assigned to interns
  tasks = await Task.find({
    assigned_to_role: "intern",
    status: ["todo", "in_progress"],
    deadline: { $lte: now + 24_hours }
  })
  
  for task in tasks:
    if task.progress < 50:
      # Send nudge notification
      await send_notification(
        user_id=task.assigned_to,
        type="task_reminder",
        message=f"Your task '{task.title}' is due soon. Current progress: {task.progress}%"
      )
      
      # Wait 4 hours
      await sleep(4 * 3600)
      
      # Check if progress updated
      updated_task = await Task.get(task.id)
      if updated_task.progress < 60:
        # Escalate to team lead
        await send_notification(
          user_id=updated_task.team_lead_id,
          type="task_escalation",
          message=f"Intern needs help with task '{task.title}'"
        )
```

### Auto-Correct Attendance Workflow
```python
async def auto_correct_attendance():
  # Find attendance records with minor issues
  records = await Attendance.find({
    status: "late",
    check_in_time: { $gte: "09:30", $lte: "10:00" }  # 30 min late window
  })
  
  for record in records:
    # Check if total hours >= 8
    if record.total_hours >= 8:
      # Auto-correct to present
      await Attendance.update(record.id, {
        status: "present",
        notes: "Auto-corrected by AI (worked full hours)"
      })
      
      # Notify employee
      await send_notification(
        user_id=record.user_id,
        type="attendance_corrected",
        message="Your late attendance was auto-corrected as you worked full hours."
      )
```

### Auto-Approve Micro-Leaves Workflow
```python
async def auto_approve_micro_leaves():
  # Find leaves <= 1 day, no conflicts
  leaves = await Leave.find({
    status: "pending",
    days: { $lte: 1 },
    leave_type: "casual"
  })
  
  for leave in leaves:
    # Check conflicts
    conflicts = await check_conflicts(leave)
    
    if not conflicts:
      # Check team coverage
      team_on_leave = await count_team_leaves(leave.user_id, leave.start_date)
      
      if team_on_leave < 3:  # Less than 3 team members on leave
        # Auto-approve
        await Leave.update(leave.id, {
          status: "approved",
          approved_by: "AI_AUTO_APPROVE"
        })
        
        # Notify employee
        await send_notification(
          user_id=leave.user_id,
          type="leave_approved",
          message="Your leave request was auto-approved."
        )
```

## 11.5 Predictive Analytics

### Attrition Risk Prediction

**Data Required:**
- Attendance patterns (last 3 months)
- Task completion rate
- Leave frequency
- Performance reviews
- Tenure
- Team satisfaction scores

**Model:**
```python
# Simplified scoring
def calculate_attrition_risk(employee):
  score = 0
  
  # Attendance pattern (weight: 30%)
  if employee.late_days_last_month > 5:
    score += 30
  
  # Task completion (weight: 25%)
  if employee.task_completion_rate < 70:
    score += 25
  
  # Leave frequency (weight: 20%)
  if employee.sick_leaves_last_quarter > 5:
    score += 20
  
  # Tenure (weight: 15%)
  if employee.tenure_months < 6:
    score += 15
  
  # Performance (weight: 10%)
  if employee.last_review_score < 3:
    score += 10
  
  # Risk levels
  if score > 70:
    return "high"
  elif score > 40:
    return "medium"
  else:
    return "low"
```

**Output:**
```json
{
  "employee_id": "uuid",
  "risk_level": "high",
  "score": 75,
  "factors": [
    "High absenteeism (6 late days last month)",
    "Low task completion (65%)",
    "Frequent sick leaves"
  ],
  "recommendations": [
    "Schedule 1-on-1 with manager",
    "Review workload",
    "Check for burnout signs"
  ]
}
```

---

### Burnout Detection

**Data Required:**
- Working hours (avg per week)
- Task load (pending tasks count)
- Leave taken (last 3 months)
- Response time to messages
- Weekend work frequency

**Model:**
```python
def detect_burnout(employee):
  burnout_score = 0
  
  # Overwork (weight: 35%)
  if employee.avg_hours_per_week > 50:
    burnout_score += 35
  
  # Task overload (weight: 25%)
  if employee.pending_tasks > 10:
    burnout_score += 25
  
  # No leave (weight: 20%)
  if employee.days_since_last_leave > 90:
    burnout_score += 20
  
  # Weekend work (weight: 15%)
  if employee.weekend_work_frequency > 0.5:
    burnout_score += 15
  
  # Delayed responses (weight: 5%)
  if employee.avg_response_time > 24_hours:
    burnout_score += 5
  
  if burnout_score > 60:
    return "high_risk"
  elif burnout_score > 35:
    return "medium_risk"
  else:
    return "low_risk"
```

**Output:**
```json
{
  "employee_id": "uuid",
  "burnout_risk": "high_risk",
  "score": 75,
  "indicators": [
    "Working 55 hours/week (avg)",
    "15 pending tasks",
    "No leave in last 4 months",
    "Working 3 out of 4 weekends"
  ],
  "recommendations": [
    "Mandatory leave within 2 weeks",
    "Redistribute 5 tasks to team",
    "Block calendar on weekends",
    "Schedule wellness check"
  ]
}
```

---

### Attendance Anomaly Detection

**Data Required:**
- Check-in times (last 30 days)
- Check-out times (last 30 days)
- Work mode patterns
- Team attendance patterns

**Model:**
```python
def detect_attendance_anomaly(employee):
  anomalies = []
  
  # Late pattern (3+ late in last week)
  if employee.late_days_last_week >= 3:
    anomalies.append({
      "type": "frequent_late",
      "severity": "medium",
      "message": "Late 3+ times this week"
    })
  
  # Early checkout pattern
  if employee.early_checkout_count > 3:
    anomalies.append({
      "type": "early_checkout",
      "severity": "low",
      "message": "Frequent early checkouts"
    })
  
  # Inconsistent work mode
  if employee.work_mode_switches > 5:
    anomalies.append({
      "type": "inconsistent_mode",
      "severity": "low",
      "message": "Switching WFO/WFH frequently"
    })
  
  # Sudden change (was always on time, now late)
  if employee.late_days_last_week > 0 and employee.late_days_last_month == 0:
    anomalies.append({
      "type": "sudden_change",
      "severity": "high",
      "message": "Sudden attendance change detected"
    })
  
  return anomalies
```

**Output:**
```json
{
  "employee_id": "uuid",
  "anomalies": [
    {
      "type": "sudden_change",
      "severity": "high",
      "message": "Sudden attendance change detected",
      "action": "Schedule wellness check"
    }
  ],
  "ai_recommendation": "Talk to employee about recent changes"
}
```

---

# 12. NOTIFICATION SYSTEM ARCHITECTURE

## 12.1 Notification Types

| Type | Trigger | Recipients | Channels |
|------|---------|-----------|----------|
| Task Assigned | Task created | Assignee | In-app, Email |
| Task Updated | Task status/progress changed | Creator, Assignee | In-app |
| Task Overdue | Deadline passed | Assignee, Team Lead | In-app, Email |
| Leave Applied | Leave submitted | HR, Team Lead | In-app |
| Leave Approved | Leave approved | Employee | In-app, Email |
| Leave Rejected | Leave rejected | Employee | In-app, Email |
| Attendance Late | Check-in after deadline | Employee, Team Lead | In-app |
| Attendance Anomaly | AI detects pattern | Employee, HR | In-app |
| Announcement | New announcement | All (filtered by role) | In-app |
| AI Insight | AI detects issue | Relevant role | In-app |
| System | System updates | All | In-app |

## 12.2 Notification Templates

### Task Assigned
```
Title: New Task Assigned
Message: You have been assigned a task: "{task_title}"
Priority: {task_priority}
Deadline: {task_deadline}
Link: /tasks/{task_id}
```

### Leave Approved
```
Title: Leave Request Approved
Message: Your {leave_type} leave from {start_date} to {end_date} has been approved.
Approved by: {approver_name}
Link: /leave/{leave_id}
```

### AI Alert (Burnout)
```
Title: Burnout Risk Detected
Message: AI has detected burnout risk for {employee_name}.
Risk Level: {risk_level}
Recommendations: {ai_recommendations}
Link: /employees/{employee_id}
```

## 12.3 Escalation Paths

### Task Overdue Escalation
```
Day 0 (Deadline): Notify assignee
Day 1: Notify assignee + team lead
Day 2: Notify assignee + team lead + HR
Day 3+: Flag in HR dashboard
```

### Leave Pending Escalation
```
Day 0 (Submitted): Notify HR/Team Lead
Day 2: Reminder to HR/Team Lead
Day 5: Escalate to admin
Day 7+: Auto-approve if policy allows
```

### Attendance Issue Escalation
```
1st Late: Notify employee
3rd Late (in week): Notify employee + team lead
5th Late (in month): Notify HR + team lead
Pattern (3 consecutive weeks): Flag for review
```

## 12.4 Notification Delivery Logic

```python
async def send_notification(
  user_id: str,
  type: str,
  title: str,
  message: str,
  link: str = None,
  channels: List[str] = ["in_app"]
):
  # Create in-app notification
  if "in_app" in channels:
    await Notification.create({
      user_id: user_id,
      type: type,
      title: title,
      message: message,
      link: link,
      is_read: False
    })
  
  # Send email if channel enabled
  if "email" in channels:
    user = await User.get(user_id)
    await send_email(
      to=user.email,
      subject=title,
      body=message
    )
  
  # Real-time push via websocket
  if "push" in channels:
    await push_to_websocket(user_id, {
      title: title,
      message: message
    })
```

## 12.5 Notification Preferences (Phase 2)

```json
{
  "user_id": "uuid",
  "preferences": {
    "task_assigned": {
      "in_app": true,
      "email": true,
      "push": false
    },
    "leave_approved": {
      "in_app": true,
      "email": true,
      "push": true
    },
    "quiet_hours": {
      "enabled": true,
      "start": "22:00",
      "end": "08:00"
    }
  }
}
```

---

# 13. ANALYTICS & DASHBOARDS FRAMEWORK

## 13.1 Key Metrics by Role

### HR/Admin Dashboard

**Workforce Metrics:**
- Total employees (by role, department)
- Employee growth (month-over-month)
- Attrition rate (monthly, quarterly)
- New hires (this month)

**Attendance Metrics:**
- Present today (count + percentage)
- Attendance rate (last 30 days)
- Late arrivals (count, trend)
- Work mode distribution (WFO vs WFH)

**Leave Metrics:**
- Pending approvals (count)
- Leave utilization rate
- Most common leave type
- Leave balance distribution

**Task Metrics:**
- Total tasks (by status)
- Task completion rate
- Average time to complete
- Overdue tasks (count)

**AI Insights:**
- Attrition risk alerts
- Burnout risk employees
- Attendance anomalies
- Productivity trends

### Team Lead Dashboard

**Team Metrics:**
- Team size
- Team attendance (today)
- Team on leave (today)
- Team task load

**Task Metrics:**
- Tasks assigned by me
- Task completion rate (team)
- Overdue tasks (team)
- Average progress

**Performance Metrics:**
- Top performers (this month)
- Struggling employees (low completion)
- Workload distribution

**AI Insights:**
- Suggested task assignments
- Burnout risk (team members)
- Performance anomalies

### Employee/Intern Dashboard

**Personal Metrics:**
- My tasks (by status)
- Task completion rate (personal)
- Attendance this month (days present)
- Leave balance

**Timeline:**
- Upcoming deadlines
- Recent activity
- Announcements

## 13.2 Widget Types

### Stat Card
```
┌──────────────┐
│ 245          │
│ Total Emp.   │
│ ↑ 5% vs last │
└──────────────┘
```

### Trend Chart (Line)
```
Attendance Rate (Last 30 days)
┌────────────────────┐
│     ╱╲  ╱╲         │
│   ╱    ╲  ╲        │
│ ╱          ╲  ╱    │
└────────────────────┘
```

### Pie Chart
```
Work Mode Distribution
┌─────────────┐
│  ███ 60% WFO│
│  ▓▓▓ 35% WFH│
│  ░░░  5% Hyb│
└─────────────┘
```

### Bar Chart
```
Tasks by Status
TODO        ████████ 45
IN_PROG     █████ 23
COMPLETED   ████████████ 67
BLOCKED     ██ 8
```

### Heatmap (Attendance)
```
    M  T  W  T  F
W1  ✓  ✓  ✓  ✓  ✓
W2  ✓  ✓  ✗  ✓  ✓
W3  ✓  ✓  ✓  ✓  ✗
W4  ✓  ✓  ✓  ✓  ✓
```

### List Widget
```
┌────────────────────┐
│ Pending Approvals  │
│ • Leave: John Doe  │
│ • Attend: Jane S.  │
└────────────────────┘
```

## 13.3 Data Freshness

| Metric | Refresh Rate | Cache |
|--------|-------------|-------|
| Present Today | Real-time | No |
| Task Count | 5 minutes | Yes |
| Attendance Rate | 1 hour | Yes |
| Attrition Risk | Daily | Yes |
| AI Insights | Real-time | No |
| Leave Balance | 1 hour | Yes |

## 13.4 Export Capabilities

**Export Formats:**
- PDF (reports with charts)
- CSV (raw data)
- Excel (formatted tables)

**Exportable Reports:**
- Attendance Report (date range)
- Task Report (by status, assignee)
- Leave Report (by type, status)
- Employee Report (with performance data)
- AI Insights Report

---

# 14. SECURITY MODEL

## 14.1 RBAC Matrix

| Resource | Admin | HR | Team Lead | Employee | Intern |
|----------|-------|-----|-----------|----------|--------|
| **Users** | | | | | |
| View all | ✓ | ✓ | Team only | Self | Self |
| Create | ✓ | ✓ | ✗ | ✗ | ✗ |
| Edit | ✓ | ✓ | ✗ | Self | Self |
| Delete | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Tasks** | | | | | |
| View all | ✓ | ✓ | Team only | Assigned | Assigned |
| Create | ✓ | ✓ | ✓ | ✗ | ✗ |
| Edit | ✓ | ✓ | ✓ | Assigned | Assigned |
| Delete | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Attendance** | | | | | |
| View all | ✓ | ✓ | Team only | Self | Self |
| Check-in/out | ✓ | ✓ | ✓ | ✓ | ✓ |
| Correct | ✓ | ✓ | Team only | Self (req) | Self (req) |
| **Leave** | | | | | |
| View all | ✓ | ✓ | Team only | Self | Self |
| Apply | ✓ | ✓ | ✓ | ✓ | ✓ |
| Approve | ✓ | ✓ | ✓ | ✗ | ✗ |
| **Announcements** | | | | | |
| View | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create | ✓ | ✓ | ✗ | ✗ | ✗ |
| Edit | ✓ | ✓ | Own | ✗ | ✗ |
| Delete | ✓ | ✓ | Own | ✗ | ✗ |
| **Analytics** | | | | | |
| View all | ✓ | ✓ | Team only | Self | Self |
| Export | ✓ | ✓ | Team only | ✗ | ✗ |

## 14.2 Token Lifecycle

**Access Token:**
- Expiry: 60 minutes
- Stored: Client-side (localStorage)
- Usage: Every API request

**Refresh Token:**
- Expiry: 7 days
- Stored: Client-side (localStorage)
- Usage: Refresh access token

**Token Refresh Flow:**
```
Access token expired
  ↓
Frontend sends refresh token to /auth/refresh
  ↓
Backend validates refresh token
  ├─ Invalid/Expired → 401 Unauthorized → Redirect to login
  └─ Valid → Generate new access + refresh tokens
  ↓
Return tokens
  ↓
Frontend stores new tokens
```

## 14.3 Sensitive Data Handling

**Passwords:**
- Hashed with bcrypt (cost: 12)
- Never returned in API responses
- Reset via secure token (email)

**Personal Data:**
- Phone numbers (masked in logs)
- Email (visible to user + HR only)
- Address (Phase 2, encrypted at rest)

**Documents:**
- Stored with access control
- Audit log for all access
- Download requires authentication

## 14.4 Access-Based Filtering

**Automatic Query Filtering:**
```python
# Example: Get tasks
async def get_tasks(user: User):
  if user.role in ["admin", "hr"]:
    # HR sees all tasks
    return await Task.find({})
  
  elif user.role == "team_lead":
    # Team lead sees team tasks
    team_members = await User.find({"manager_id": user.id})
    return await Task.find({
      "assigned_to": {"$in": [m.id for m in team_members]}
    })
  
  else:
    # Employee/Intern sees own tasks
    return await Task.find({"assigned_to": user.id})
```

## 14.5 Audit Logging

**Logged Actions:**
- User login/logout
- User creation/update/deletion
- Task creation/update/deletion
- Leave approval/rejection
- Attendance corrections
- Announcement creation
- Settings changes

**Audit Log Entry:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "action": "task.created",
  "resource_type": "task",
  "resource_id": "uuid",
  "old_value": null,
  "new_value": {
    "title": "Fix bug",
    "assigned_to": "uuid"
  },
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "created_at": "2025-01-10T10:00:00Z"
}
```

---

# 15. PERFORMANCE OPTIMIZATION LAYER

## 15.1 Caching Strategy

**Redis Cache Layers:**

| Data | TTL | Invalidation |
|------|-----|--------------|
| User profile | 1 hour | On update |
| Dashboard stats | 5 minutes | On related change |
| Task counts | 5 minutes | On task create/update |
| Department list | 1 hour | On dept create/update |
| Announcements | 15 minutes | On announcement create |

**Cache Keys:**
```
user:{user_id}
stats:{user_id}:{role}
tasks:count:{user_id}
departments:list
announcements:list
```

## 15.2 Database Optimization

**Indexes:**
```javascript
// Users
users.createIndex({ email: 1 }, { unique: true })
users.createIndex({ role: 1 })
users.createIndex({ department_id: 1 })

// Tasks
tasks.createIndex({ assigned_to: 1, status: 1 })
tasks.createIndex({ created_by: 1 })
tasks.createIndex({ deadline: 1 })

// Attendance
attendance.createIndex({ user_id: 1, date: 1 }, { unique: true })
attendance.createIndex({ date: 1 })

// Leave
leaves.createIndex({ user_id: 1, status: 1 })
leaves.createIndex({ start_date: 1, end_date: 1 })
```

**Query Optimization:**
- Projection: Only fetch required fields
- Limit: Paginate large result sets
- Aggregation: Use for complex analytics

## 15.3 Frontend Optimization

**Code Splitting:**
```javascript
// Lazy load pages
const HRDashboard = lazy(() => import('./pages/HRDashboard'))
const TasksPage = lazy(() => import('./pages/TasksPage'))
```

**Virtualized Lists:**
```javascript
// For long lists (e.g., 1000+ tasks)
<VirtualList
  items={tasks}
  itemHeight={100}
  height={600}
/>
```

**Debounced Search:**
```javascript
const debouncedSearch = debounce(searchTasks, 300)
```

**Lazy Image Loading:**
```javascript
<img src={avatar} loading="lazy" />
```

## 15.4 API Rate Limiting

**Rate Limits:**
- General: 100 requests/minute per user
- AI chat: 20 requests/minute per user
- Login: 5 attempts/minute per IP
- Export: 10 requests/hour per user

**Implementation:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_user_id)

@app.post("/api/tasks")
@limiter.limit("100/minute")
async def create_task(...):
  ...
```

## 15.5 AI Call Optimization

**Deduplication:**
- Cache AI responses for 1 hour
- Same query + context → Return cached response

**Batching:**
- Group similar AI requests
- Process in batch for efficiency

**Model Selection:**
- Use Gemini 2.5 Flash (fast, cheap)
- Upgrade to Pro for complex analysis (Phase 2)

---

# 16. PHASE 1 → PHASE 2 ROADMAP

## Phase 1 (Current MVP) ✓

**Delivered:**
- Authentication (JWT)
- Role-based dashboards (5 roles)
- Task management
- Attendance tracking
- Leave management
- Announcements
- AI Assistant (Gemini 2.5 Flash)
- Real-time notifications
- Basic analytics

**Timeline:** Completed

---

## Phase 2 (Enhanced Features)

**Q1 2025 (Jan-Mar):**

**1. Advanced Task Management**
- Subtasks
- Task dependencies
- Kanban board view
- Task templates
- Recurring tasks
- Time tracking

**2. Performance Management**
- Goal setting (OKRs)
- 1-on-1 notes
- Performance reviews
- 360-degree feedback
- Continuous feedback

**3. Enhanced Analytics**
- Custom reports builder
- Scheduled reports (email)
- Data visualization (charts)
- Predictive dashboards
- Export to Excel/PDF

**4. Document Management**
- Document upload/storage
- Version control
- Access control
- E-signatures
- Document templates

---

**Q2 2025 (Apr-Jun):**

**5. Advanced AI Features**
- Predictive attrition model
- Burnout detection
- Skill gap analysis
- Automated performance insights
- AI-generated development plans

**6. Shift Management**
- Shift scheduling
- Shift swapping
- Shift conflicts detection
- Rotating shifts
- Shift reports

**7. Mobile App**
- iOS app
- Android app
- Push notifications
- Offline mode
- GPS attendance (optional)

**8. Integrations**
- Slack integration
- Microsoft Teams integration
- Google Calendar sync
- Zoom integration
- Payroll systems

---

**Q3 2025 (Jul-Sep):**

**9. Multi-Tenancy**
- Organization management
- Department hierarchies
- Cross-department visibility
- Tenant isolation
- White-labeling

**10. Finance Module**
- Payroll management
- Salary slips
- Tax calculations
- Expense management
- Reimbursements

**11. Compliance & Policies**
- Policy builder
- Compliance tracking
- Certification management
- Training records
- Audit trails

**12. Advanced Notifications**
- Multi-channel (email, SMS, push)
- Notification preferences
- Escalation rules
- Notification templates
- Quiet hours

---

**Q4 2025 (Oct-Dec):**

**13. Workforce Planning**
- Headcount planning
- Recruitment tracking
- Onboarding workflows
- Offboarding workflows
- Succession planning

**14. Learning & Development**
- Course management
- Learning paths
- Certifications
- Skill assessments
- E-learning integration

**15. Advanced Security**
- MFA (2FA)
- SSO (SAML, OAuth)
- IP whitelisting
- Session management
- Data encryption at rest

**16. Enterprise Features**
- Custom workflows
- Advanced RBAC
- API access
- Webhooks
- Custom integrations

---

## Architecture Milestones

**Phase 1 → 2 Transition:**
1. Database migration (add new collections)
2. API versioning (/api/v2)
3. Frontend refactoring (module separation)
4. Performance optimization (caching, indexing)
5. Security hardening (encryption, MFA)

**Infrastructure:**
- Migrate to Kubernetes (auto-scaling)
- Add Redis for caching
- CDN for static assets
- Backup & disaster recovery
- Monitoring (Prometheus, Grafana)

---

# 17. CONCLUSION & IMPLEMENTATION NOTES

## 17.1 Development Priority

**Week 1-2:**
- ✓ Authentication & RBAC
- ✓ Core navigation
- ✓ Dashboard layouts

**Week 3-4:**
- ✓ Task management
- ✓ Attendance tracking
- ✓ Leave management

**Week 5-6:**
- ✓ AI integration (Gemini)
- ✓ Notifications
- ✓ Analytics

**Week 7-8:**
- Testing & bug fixes
- UI/UX polish
- Documentation
- Deployment

## 17.2 Tech Stack Summary

**Backend:**
- FastAPI (Python 3.11+)
- MongoDB (with Motor async driver)
- JWT authentication
- Gemini 2.5 Flash (via emergentintegrations)

**Frontend:**
- React 19
- Tailwind CSS
- Shadcn UI components
- React Router
- Axios
- Sonner (toasts)

**Infrastructure:**
- Kubernetes (auto-scaling)
- MongoDB (replica set)
- Redis (caching, Phase 2)
- Nginx (reverse proxy)

## 17.3 Key Success Metrics

**Product Metrics:**
- User adoption rate (% of employees using daily)
- Task completion rate
- Leave approval time (target: < 24 hours)
- AI auto-approval rate (target: > 60%)
- User satisfaction score (NPS)

**Technical Metrics:**
- API response time (< 200ms p95)
- Uptime (99.9%)
- Error rate (< 0.1%)
- AI response time (< 3s)

## 17.4 Documentation Deliverables

**For Developers:**
- API documentation (OpenAPI/Swagger)
- Component library (Storybook)
- Database schema
- Deployment guide

**For Users:**
- User manual (per role)
- Video tutorials
- FAQ
- Support portal

---

# END OF DOCUMENT

**Document Version:** 1.0  
**Total Sections:** 17  
**Total Pages:** ~80 equivalent  
**Completeness:** Enterprise-grade blueprint  
**Ready for:** Development, Review, Stakeholder Presentation

This specification covers every aspect of OperAI from vision to implementation, providing a complete roadmap for building an enterprise-grade, AI-native workforce management platform.

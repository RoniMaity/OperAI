# OperAI - Workforce Management System

OperAI is a comprehensive workforce management platform with AI-powered assistance, designed for modern organizations to manage tasks, attendance, leaves, and team collaboration.

## 🚀 Features

- **Multi-Role Access**: Admin, HR, Team Lead, Employee, and Intern roles with specific permissions
- **Task Management**: Create, assign, track, and update tasks with progress monitoring
- **Attendance Tracking**: Check-in/check-out with WFO, WFH, and hybrid work mode support
- **Leave Management**: Apply, approve, and track leave requests
- **Deadline Requests**: Request deadline extensions with approval workflow
- **Announcements**: Company-wide and role-specific announcements
- **Real-time Notifications**: Get notified about important events
- **AI Assistant**: Chat with AI and execute actions using natural language (Hindi-English supported)

## 📋 Demo Accounts

For testing and demonstration purposes, use these pre-configured accounts:

| Role       | Email                | Password     | Description                          |
|------------|----------------------|--------------|--------------------------------------|
| Admin      | admin@operai.demo    | Password123! | Full system access and management    |
| HR         | hr@operai.demo       | Password123! | Employee and leave management        |
| Team Lead  | lead@operai.demo     | Password123! | Team task management and approvals   |
| Employee   | emp1@operai.demo     | Password123! | Alice Employee - Regular employee    |
| Employee   | emp2@operai.demo     | Password123! | Bob Employee - Regular employee      |
| Intern     | intern@operai.demo   | Password123! | Charlie Intern - Intern access       |

### Demo Data Includes:
- ✅ 8 tasks with various statuses (todo, in-progress, completed, blocked)
- ✅ 5 leave applications (pending, approved, rejected)
- ✅ 18 attendance records across the team
- ✅ 3 deadline extension requests
- ✅ 5 company announcements
- ✅ 7 notifications (task updates, announcements, deadline changes)
- ✅ AI conversation history

## 🌱 Seeding Demo Data

To reset and reseed the database with fresh demo data:

```bash
cd /app/backend
python seed_demo_data.py
```

This will:
1. Clear existing demo data (users, tasks, leaves, etc.)
2. Create 6 demo users with all roles
3. Populate realistic tasks, leaves, attendance, and other data
4. Generate notifications and AI conversation history

**Note**: Run this whenever you want to reset to a clean demo state.

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database with Motor (async driver)
- **JWT**: Token-based authentication
- **Emergent Integrations**: AI integration with Gemini 2.5 Flash
- **Bcrypt**: Password hashing

### Frontend
- **React**: UI framework
- **Tailwind CSS**: Utility-first styling
- **Context API**: State management
- **Axios**: HTTP client

## 📁 Project Structure

```
/app/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── seed_demo_data.py      # Demo data seeding script
│   ├── services/
│   │   └── ai_actions.py      # AI action executor
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Backend configuration
├── frontend/
│   ├── src/
│   │   ├── pages/             # React page components
│   │   ├── components/        # Reusable UI components
│   │   ├── context/           # Context providers
│   │   ├── services/          # API service layer
│   │   └── App.js             # Main app component
│   ├── package.json           # Node dependencies
│   └── .env                   # Frontend configuration
└── README.md                  # This file
```

## 🎯 Quick Start

### Backend Setup

1. Install dependencies:
```bash
cd /app/backend
pip install -r requirements.txt
```

2. Seed demo data:
```bash
python seed_demo_data.py
```

3. Start backend server (runs automatically via supervisor):
```bash
sudo supervisorctl restart backend
```

Backend runs on: `http://localhost:8001`

### Frontend Setup

1. Install dependencies:
```bash
cd /app/frontend
yarn install
```

2. Start frontend (runs automatically via supervisor):
```bash
sudo supervisorctl restart frontend
```

Frontend runs on: `http://localhost:3000`

### Check Services Status

```bash
sudo supervisorctl status
```

## 🔐 Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=workforceos_db
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EMERGENT_LLM_KEY=your_emergent_key
```

### Frontend (.env)
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🤖 AI Features

OperAI includes an AI assistant powered by Gemini 2.5 Flash that understands:

- **Mixed Hindi-English**: "kal ka leave laga do", "aaj WFH mark kar do"
- **Natural commands**: "show my tasks", "summarize notifications"
- **Context awareness**: Knows your role, tasks, and work context

### AI Actions Available:
- Apply leave
- Mark attendance
- List tasks
- Update task status
- Create announcements (HR/Admin)
- Generate team reports (Team Lead)

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Tasks
- `GET /api/tasks` - List tasks (role-filtered)
- `POST /api/tasks` - Create task (Team Lead+)
- `PATCH /api/tasks/{id}` - Update task
- `POST /api/tasks/{id}/deadline-requests` - Request deadline extension

### Attendance
- `POST /api/attendance/check-in` - Check in
- `POST /api/attendance/check-out` - Check out
- `GET /api/attendance` - View attendance records

### Leave
- `POST /api/leave` - Apply for leave
- `GET /api/leave` - View leaves
- `PATCH /api/leave/{id}` - Approve/reject leave (HR)

### Announcements
- `POST /api/announcements` - Create announcement (HR/Admin)
- `GET /api/announcements` - View announcements

### Notifications
- `GET /api/notifications` - View notifications
- `PATCH /api/notifications/{id}/read` - Mark as read
- `PATCH /api/notifications/mark-all-read` - Mark all as read

### AI Assistant
- `POST /api/ai/chat` - Chat with AI
- `POST /api/ai/execute` - Execute AI actions
- `GET /api/ai/history` - View chat history

## 🧪 Testing

### Backend QA
Comprehensive backend testing has been completed with 100% success rate.

See `/app/QA_SESSION_SUMMARY.md` for detailed test results.

### Test Credentials
Use the demo accounts listed above for testing all features.

## 📝 Development Notes

- All passwords are hashed using bcrypt
- JWT tokens expire after 60 minutes
- MongoDB indexes are preserved during demo data seeding
- RBAC is enforced at the API level
- AI assistant requires EMERGENT_LLM_KEY to be configured

## 🐛 Known Issues

All major bugs have been fixed. See `/app/QA_SESSION_SUMMARY.md` for details.

## 📄 License

Proprietary - OperAI Workforce Management System

---

**Need Help?** Check the demo accounts above and use the AI assistant for guidance!

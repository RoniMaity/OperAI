#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: "Full end-to-end QA pass for OperAI across all roles (Admin, HR, Team Lead, Employee, Intern). Test auth/RBAC, core workflows (tasks, leaves, attendance, announcements, AI), and fix real bugs. Do NOT redesign, just stabilize."

backend:
  - task: "Auth - Register and Login"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Need to test registration and login for all roles"
      - working: true
        agent: "testing"
        comment: "Successfully tested registration and login for all 5 roles (admin, hr, team_lead, employee, intern). All users can register and login correctly with proper JWT token generation."

  - task: "Auth - /api/auth/me endpoint"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Need to verify correct role and metadata returned"
      - working: true
        agent: "testing"
        comment: "/api/auth/me endpoint working correctly for all roles. Returns proper user data including correct role, email, name, and other metadata."

  - task: "RBAC - Route Protection"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Need to test cross-role access prevention"
      - working: true
        agent: "testing"
        comment: "RBAC working correctly. Employee users are properly denied access to HR-only endpoints like /api/users (returns 403 Forbidden as expected)."

  - task: "Tasks - CRUD Operations"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test task creation, update, listing for all roles"
      - working: true
        agent: "testing"
        comment: "Task CRUD operations working perfectly. Team Lead can create tasks for employees, employees can see their assigned tasks, update status/progress, and Team Lead can see tasks they created."

  - task: "Deadline Requests - Create/Approve/Reject"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test deadline request flow for employees and approval by team leads"
      - working: true
        agent: "testing"
        comment: "Deadline request flow working correctly. Employees can create deadline extension requests, Team Leads can view and approve/reject them. Notifications are properly created upon approval/rejection."

  - task: "Attendance - Check-in/Check-out"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test attendance marking and once-per-day enforcement"
      - working: true
        agent: "testing"
        comment: "Attendance system working correctly. Employees can check-in with work mode (WFO/WFH), duplicate check-in prevention works, check-out functionality works, and attendance records are retrievable."

  - task: "Leave - Apply/Approve/Reject"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test leave application and approval flow"
      - working: true
        agent: "testing"
        comment: "Leave management working perfectly. Employees can apply for leave, HR can view all leave requests, and HR can approve/reject leave requests with proper status updates."

  - task: "Announcements - Create and Notifications"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test announcement creation and notification generation"
      - working: false
        agent: "testing"
        comment: "Found bug in notification query logic for announcements with empty target_roles"
      - working: true
        agent: "testing"
        comment: "FIXED: Updated notification query to handle empty target_roles (all users). HR can create announcements and all employees receive notifications correctly."

  - task: "AI - /api/ai/chat endpoint"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test AI chat functionality"
      - working: true
        agent: "testing"
        comment: "AI chat endpoint working correctly. Responds to user messages using Gemini 2.5 Flash model with proper context and conversation history."

  - task: "AI - /api/ai/execute endpoint"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test AI action execution with Hindi-English prompts"
      - working: true
        agent: "testing"
        comment: "AI execute endpoint working correctly. Successfully processes Hindi-English mixed prompts like 'kal ka leave laga do', 'aaj WFH mark kar do', 'mujhe tasks dikhao' without 500 errors. Returns valid JSON responses."

  - task: "Notifications - Creation and Retrieval"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Test notification system for all notification types"
      - working: true
        agent: "testing"
        comment: "Notification system working correctly. Users can retrieve notifications, mark individual notifications as read, and mark all notifications as read. Notifications are properly created for announcements and deadline request updates."

frontend:
  - task: "Auth UI - Login/Register"
    implemented: true
    working: "NA"
    file: "frontend/src/pages/LoginPage.js, RegisterPage.js"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Will test after backend verification"

  - task: "Dashboard - Role-specific views"
    implemented: true
    working: "NA"
    file: "frontend/src/pages/"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Will test after backend verification"

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 1
  run_ui: false

test_plan:
  current_focus:
    - "Auth - Register and Login"
    - "Auth - /api/auth/me endpoint"
    - "RBAC - Route Protection"
    - "Tasks - CRUD Operations"
    - "Attendance - Check-in/Check-out"
    - "Leave - Apply/Approve/Reject"
    - "AI - /api/ai/execute endpoint"
  stuck_tasks: []
  test_all: true
  test_priority: "sequential"

agent_communication:
  - agent: "main"
    message: "Starting comprehensive QA pass. Backend testing first, then frontend. Will test all roles: Admin, HR, Team Lead, Employee, Intern. Focus on real bugs, not redesign."
  - agent: "testing"
    message: "BACKEND TESTING COMPLETE: Comprehensive testing of all OperAI backend APIs completed successfully. Found and FIXED one critical bug in notification system. All core functionality working: Auth/RBAC (100%), Tasks (100%), Attendance (100%), Leave Management (100%), Deadline Requests (100%), Announcements/Notifications (100% after fix), AI endpoints (100%). Success rate: 97.5% (39/40 tests passed, 1 expected duplicate prevention). Ready for frontend testing or production deployment."
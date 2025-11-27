#!/usr/bin/env python3
"""
Comprehensive Backend Testing for OperAI WorkforceOS
Tests all backend APIs systematically across all user roles
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configuration
BASE_URL = "https://role-test-operai.preview.emergentagent.com/api"
HEADERS = {"Content-Type": "application/json"}

class OperAITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS.copy()
        self.tokens = {}  # Store tokens for different users
        self.users = {}   # Store user data
        self.test_results = []
        
    def log_result(self, test_name: str, success: bool, message: str, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def make_request(self, method: str, endpoint: str, data: dict = None, auth_token: str = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=headers, json=data, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}, 0
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
            
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}, 0
    
    def test_auth_register_and_login(self):
        """Test user registration and login for all roles"""
        print("\n=== Testing Authentication & Registration ===")
        
        # Test users for different roles
        test_users = [
            {"email": "admin@operai.com", "name": "Admin User", "password": "admin123", "role": "admin"},
            {"email": "hr@operai.com", "name": "HR Manager", "password": "hr123", "role": "hr"},
            {"email": "teamlead@operai.com", "name": "Team Lead", "password": "lead123", "role": "team_lead"},
            {"email": "employee@operai.com", "name": "John Employee", "password": "emp123", "role": "employee"},
            {"email": "intern@operai.com", "name": "Jane Intern", "password": "intern123", "role": "intern"}
        ]
        
        # Register users
        for user_data in test_users:
            success, response, status_code = self.make_request("POST", "/auth/register", user_data)
            
            if success:
                self.users[user_data["role"]] = response
                self.log_result(
                    f"Register {user_data['role']}",
                    True,
                    f"Successfully registered {user_data['name']}"
                )
            else:
                # Check if user already exists
                if status_code == 400 and "already registered" in str(response):
                    self.log_result(
                        f"Register {user_data['role']}",
                        True,
                        f"User {user_data['name']} already exists (expected)"
                    )
                else:
                    self.log_result(
                        f"Register {user_data['role']}",
                        False,
                        f"Failed to register {user_data['name']}",
                        f"Status: {status_code}, Response: {response}"
                    )
        
        # Login users
        for user_data in test_users:
            login_data = {"email": user_data["email"], "password": user_data["password"]}
            success, response, status_code = self.make_request("POST", "/auth/login", login_data)
            
            if success and "access_token" in response:
                self.tokens[user_data["role"]] = response["access_token"]
                self.users[user_data["role"]] = response["user"]
                self.log_result(
                    f"Login {user_data['role']}",
                    True,
                    f"Successfully logged in {user_data['name']}"
                )
            else:
                self.log_result(
                    f"Login {user_data['role']}",
                    False,
                    f"Failed to login {user_data['name']}",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_auth_me_endpoint(self):
        """Test /api/auth/me endpoint for all roles"""
        print("\n=== Testing /api/auth/me Endpoint ===")
        
        for role, token in self.tokens.items():
            success, response, status_code = self.make_request("GET", "/auth/me", auth_token=token)
            
            if success and response.get("role") == role:
                self.log_result(
                    f"Auth/me {role}",
                    True,
                    f"Correctly returned role: {role}"
                )
            else:
                self.log_result(
                    f"Auth/me {role}",
                    False,
                    f"Failed to get correct user info for {role}",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_rbac_route_protection(self):
        """Test role-based access control"""
        print("\n=== Testing RBAC Route Protection ===")
        
        # Test employee trying to access HR-only endpoint
        if "employee" in self.tokens:
            success, response, status_code = self.make_request(
                "GET", "/users", auth_token=self.tokens["employee"]
            )
            
            if not success and status_code == 403:
                self.log_result(
                    "RBAC Employee->Users",
                    True,
                    "Employee correctly denied access to /users"
                )
            else:
                self.log_result(
                    "RBAC Employee->Users",
                    False,
                    "Employee should not have access to /users",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_user_management(self):
        """Test user management endpoints"""
        print("\n=== Testing User Management ===")
        
        # HR/Admin should see all users
        for role in ["hr", "admin"]:
            if role in self.tokens:
                success, response, status_code = self.make_request(
                    "GET", "/users", auth_token=self.tokens[role]
                )
                
                if success and isinstance(response, list):
                    self.log_result(
                        f"Users list {role}",
                        True,
                        f"{role.upper()} can see {len(response)} users"
                    )
                else:
                    self.log_result(
                        f"Users list {role}",
                        False,
                        f"{role.upper()} failed to get users list",
                        f"Status: {status_code}, Response: {response}"
                    )
        
        # Team Lead should see only employees/interns
        if "team_lead" in self.tokens:
            success, response, status_code = self.make_request(
                "GET", "/users", auth_token=self.tokens["team_lead"]
            )
            
            if success and isinstance(response, list):
                # Check if only employees/interns are returned
                roles_seen = [user.get("role") for user in response]
                valid_roles = all(role in ["employee", "intern"] for role in roles_seen if role)
                
                self.log_result(
                    "Users list team_lead",
                    valid_roles,
                    f"Team Lead sees {len(response)} users with roles: {set(roles_seen)}"
                )
            else:
                self.log_result(
                    "Users list team_lead",
                    False,
                    "Team Lead failed to get users list",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_tasks_crud(self):
        """Test task CRUD operations"""
        print("\n=== Testing Tasks CRUD ===")
        
        # Team Lead creates task for employee
        if "team_lead" in self.tokens and "employee" in self.users:
            task_data = {
                "title": "Test Task for Employee",
                "description": "This is a test task created by team lead",
                "assigned_to": self.users["employee"]["id"],
                "priority": "high",
                "deadline": (datetime.now() + timedelta(days=7)).isoformat()
            }
            
            success, response, status_code = self.make_request(
                "POST", "/tasks", task_data, auth_token=self.tokens["team_lead"]
            )
            
            if success and "id" in response:
                task_id = response["id"]
                self.log_result(
                    "Create Task",
                    True,
                    f"Team Lead created task: {response['title']}"
                )
                
                # Employee gets their tasks
                success, tasks_response, status_code = self.make_request(
                    "GET", "/tasks", auth_token=self.tokens["employee"]
                )
                
                if success and isinstance(tasks_response, list):
                    employee_task_ids = [task.get("id") for task in tasks_response]
                    if task_id in employee_task_ids:
                        self.log_result(
                            "Employee Get Tasks",
                            True,
                            f"Employee can see their assigned task"
                        )
                        
                        # Employee updates task status and progress
                        update_data = {
                            "status": "in_progress",
                            "progress": 50,
                            "notes": "Working on this task"
                        }
                        
                        success, update_response, status_code = self.make_request(
                            "PATCH", f"/tasks/{task_id}", update_data, auth_token=self.tokens["employee"]
                        )
                        
                        if success:
                            self.log_result(
                                "Update Task",
                                True,
                                f"Employee updated task status to {update_response.get('status')}"
                            )
                        else:
                            self.log_result(
                                "Update Task",
                                False,
                                "Employee failed to update task",
                                f"Status: {status_code}, Response: {update_response}"
                            )
                    else:
                        self.log_result(
                            "Employee Get Tasks",
                            False,
                            "Employee cannot see their assigned task"
                        )
                else:
                    self.log_result(
                        "Employee Get Tasks",
                        False,
                        "Employee failed to get tasks",
                        f"Status: {status_code}, Response: {tasks_response}"
                    )
                
                # Team Lead gets tasks they created
                success, lead_tasks, status_code = self.make_request(
                    "GET", "/tasks", auth_token=self.tokens["team_lead"]
                )
                
                if success and isinstance(lead_tasks, list):
                    lead_task_ids = [task.get("id") for task in lead_tasks]
                    if task_id in lead_task_ids:
                        self.log_result(
                            "Team Lead Get Tasks",
                            True,
                            f"Team Lead can see tasks they created"
                        )
                    else:
                        self.log_result(
                            "Team Lead Get Tasks",
                            False,
                            "Team Lead cannot see tasks they created"
                        )
                else:
                    self.log_result(
                        "Team Lead Get Tasks",
                        False,
                        "Team Lead failed to get tasks",
                        f"Status: {status_code}, Response: {lead_tasks}"
                    )
            else:
                self.log_result(
                    "Create Task",
                    False,
                    "Team Lead failed to create task",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_attendance_flow(self):
        """Test attendance check-in/check-out flow"""
        print("\n=== Testing Attendance Flow ===")
        
        if "employee" in self.tokens:
            # Check-in with WFO mode
            checkin_data = {"work_mode": "wfo"}
            success, response, status_code = self.make_request(
                "POST", "/attendance/check-in", checkin_data, auth_token=self.tokens["employee"]
            )
            
            if success:
                self.log_result(
                    "Attendance Check-in",
                    True,
                    f"Employee checked in with mode: {response.get('work_mode')}"
                )
                
                # Try to check-in again (should fail)
                success, response2, status_code2 = self.make_request(
                    "POST", "/attendance/check-in", checkin_data, auth_token=self.tokens["employee"]
                )
                
                if not success and status_code2 == 400:
                    self.log_result(
                        "Duplicate Check-in Prevention",
                        True,
                        "Correctly prevented duplicate check-in"
                    )
                else:
                    self.log_result(
                        "Duplicate Check-in Prevention",
                        False,
                        "Should prevent duplicate check-in",
                        f"Status: {status_code2}, Response: {response2}"
                    )
                
                # Check-out
                checkout_data = {"notes": "End of work day"}
                success, checkout_response, status_code = self.make_request(
                    "POST", "/attendance/check-out", checkout_data, auth_token=self.tokens["employee"]
                )
                
                if success:
                    self.log_result(
                        "Attendance Check-out",
                        True,
                        "Employee successfully checked out"
                    )
                else:
                    self.log_result(
                        "Attendance Check-out",
                        False,
                        "Employee failed to check out",
                        f"Status: {status_code}, Response: {checkout_response}"
                    )
                
                # Get attendance records
                success, attendance_records, status_code = self.make_request(
                    "GET", "/attendance", auth_token=self.tokens["employee"]
                )
                
                if success and isinstance(attendance_records, list):
                    self.log_result(
                        "Get Attendance",
                        True,
                        f"Employee retrieved {len(attendance_records)} attendance records"
                    )
                else:
                    self.log_result(
                        "Get Attendance",
                        False,
                        "Employee failed to get attendance records",
                        f"Status: {status_code}, Response: {attendance_records}"
                    )
            else:
                self.log_result(
                    "Attendance Check-in",
                    False,
                    "Employee failed to check in",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_leave_management(self):
        """Test leave application and approval flow"""
        print("\n=== Testing Leave Management ===")
        
        if "employee" in self.tokens:
            # Employee applies for leave
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            day_after = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
            
            leave_data = {
                "leave_type": "casual",
                "start_date": tomorrow,
                "end_date": day_after,
                "reason": "Personal work"
            }
            
            success, response, status_code = self.make_request(
                "POST", "/leave", leave_data, auth_token=self.tokens["employee"]
            )
            
            if success and "id" in response:
                leave_id = response["id"]
                self.log_result(
                    "Apply Leave",
                    True,
                    f"Employee applied for {response['leave_type']} leave"
                )
                
                # HR gets all leaves
                if "hr" in self.tokens:
                    success, leaves_response, status_code = self.make_request(
                        "GET", "/leave", auth_token=self.tokens["hr"]
                    )
                    
                    if success and isinstance(leaves_response, list):
                        leave_ids = [leave.get("id") for leave in leaves_response]
                        if leave_id in leave_ids:
                            self.log_result(
                                "HR Get Leaves",
                                True,
                                f"HR can see employee leave requests"
                            )
                            
                            # HR approves leave
                            approval_data = {"status": "approved"}
                            success, approval_response, status_code = self.make_request(
                                "PATCH", f"/leave/{leave_id}", approval_data, auth_token=self.tokens["hr"]
                            )
                            
                            if success:
                                self.log_result(
                                    "Approve Leave",
                                    True,
                                    f"HR approved leave request"
                                )
                            else:
                                self.log_result(
                                    "Approve Leave",
                                    False,
                                    "HR failed to approve leave",
                                    f"Status: {status_code}, Response: {approval_response}"
                                )
                        else:
                            self.log_result(
                                "HR Get Leaves",
                                False,
                                "HR cannot see employee leave requests"
                            )
                    else:
                        self.log_result(
                            "HR Get Leaves",
                            False,
                            "HR failed to get leave requests",
                            f"Status: {status_code}, Response: {leaves_response}"
                        )
            else:
                self.log_result(
                    "Apply Leave",
                    False,
                    "Employee failed to apply for leave",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_deadline_requests(self):
        """Test deadline request flow"""
        print("\n=== Testing Deadline Requests ===")
        
        # First, create a task if we have the necessary tokens
        if "team_lead" in self.tokens and "employee" in self.users:
            # Create a task with a deadline
            task_data = {
                "title": "Task with Deadline",
                "description": "Task for deadline extension testing",
                "assigned_to": self.users["employee"]["id"],
                "priority": "medium",
                "deadline": (datetime.now() + timedelta(days=3)).isoformat()
            }
            
            success, task_response, status_code = self.make_request(
                "POST", "/tasks", task_data, auth_token=self.tokens["team_lead"]
            )
            
            if success and "id" in task_response:
                task_id = task_response["id"]
                
                # Employee requests deadline extension
                if "employee" in self.tokens:
                    new_deadline = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
                    request_data = {
                        "requested_new_deadline": new_deadline,
                        "reason": "Need more time to complete quality work"
                    }
                    
                    success, request_response, status_code = self.make_request(
                        "POST", f"/tasks/{task_id}/deadline-requests", request_data, 
                        auth_token=self.tokens["employee"]
                    )
                    
                    if success and "id" in request_response:
                        request_id = request_response["id"]
                        self.log_result(
                            "Create Deadline Request",
                            True,
                            "Employee created deadline extension request"
                        )
                        
                        # Team Lead gets deadline requests
                        success, requests_response, status_code = self.make_request(
                            "GET", "/deadline-requests", auth_token=self.tokens["team_lead"]
                        )
                        
                        if success and isinstance(requests_response, list):
                            request_ids = [req.get("id") for req in requests_response]
                            if request_id in request_ids:
                                self.log_result(
                                    "Team Lead Get Deadline Requests",
                                    True,
                                    "Team Lead can see deadline requests"
                                )
                                
                                # Team Lead approves request
                                approval_data = {
                                    "status": "approved",
                                    "response_note": "Approved due to valid reason"
                                }
                                
                                success, approval_response, status_code = self.make_request(
                                    "PATCH", f"/deadline-requests/{request_id}", approval_data,
                                    auth_token=self.tokens["team_lead"]
                                )
                                
                                if success:
                                    self.log_result(
                                        "Approve Deadline Request",
                                        True,
                                        "Team Lead approved deadline request"
                                    )
                                    
                                    # Check if notification was created (we'll test this in notifications)
                                else:
                                    self.log_result(
                                        "Approve Deadline Request",
                                        False,
                                        "Team Lead failed to approve deadline request",
                                        f"Status: {status_code}, Response: {approval_response}"
                                    )
                            else:
                                self.log_result(
                                    "Team Lead Get Deadline Requests",
                                    False,
                                    "Team Lead cannot see deadline requests"
                                )
                        else:
                            self.log_result(
                                "Team Lead Get Deadline Requests",
                                False,
                                "Team Lead failed to get deadline requests",
                                f"Status: {status_code}, Response: {requests_response}"
                            )
                    else:
                        self.log_result(
                            "Create Deadline Request",
                            False,
                            "Employee failed to create deadline request",
                            f"Status: {status_code}, Response: {request_response}"
                        )
    
    def test_announcements_and_notifications(self):
        """Test announcements and notification creation"""
        print("\n=== Testing Announcements & Notifications ===")
        
        if "hr" in self.tokens:
            # HR creates announcement
            announcement_data = {
                "title": "Company Update",
                "content": "This is an important company-wide announcement for all employees.",
                "target_roles": []  # Empty means all roles
            }
            
            success, response, status_code = self.make_request(
                "POST", "/announcements", announcement_data, auth_token=self.tokens["hr"]
            )
            
            if success:
                self.log_result(
                    "Create Announcement",
                    True,
                    f"HR created announcement: {response.get('title')}"
                )
                
                # Wait a moment for notification to be created
                time.sleep(1)
                
                # Employee gets notifications
                if "employee" in self.tokens:
                    success, notifications, status_code = self.make_request(
                        "GET", "/notifications", auth_token=self.tokens["employee"]
                    )
                    
                    if success and isinstance(notifications, list):
                        announcement_notifications = [
                            n for n in notifications 
                            if n.get("type") == "announcement" and announcement_data["title"] in n.get("title", "")
                        ]
                        
                        if announcement_notifications:
                            self.log_result(
                                "Announcement Notification",
                                True,
                                "Employee received announcement notification"
                            )
                        else:
                            self.log_result(
                                "Announcement Notification",
                                False,
                                "Employee did not receive announcement notification"
                            )
                    else:
                        self.log_result(
                            "Get Notifications",
                            False,
                            "Employee failed to get notifications",
                            f"Status: {status_code}, Response: {notifications}"
                        )
            else:
                self.log_result(
                    "Create Announcement",
                    False,
                    "HR failed to create announcement",
                    f"Status: {status_code}, Response: {response}"
                )
    
    def test_ai_endpoints(self):
        """Test AI chat and execute endpoints"""
        print("\n=== Testing AI Endpoints ===")
        
        if "employee" in self.tokens:
            # Test AI chat
            chat_data = {
                "message": "hello",
                "session_id": "test_session_123"
            }
            
            success, response, status_code = self.make_request(
                "POST", "/ai/chat", chat_data, auth_token=self.tokens["employee"]
            )
            
            if success and "response" in response:
                self.log_result(
                    "AI Chat",
                    True,
                    "AI chat responded successfully"
                )
            else:
                self.log_result(
                    "AI Chat",
                    False,
                    "AI chat failed",
                    f"Status: {status_code}, Response: {response}"
                )
            
            # Test AI execute with various prompts
            test_prompts = [
                "kal ka leave laga do",
                "aaj WFH mark kar do", 
                "mujhe aaj ke tasks dikhao",
                "summarize my notifications"
            ]
            
            for prompt in test_prompts:
                execute_data = {
                    "message": prompt,
                    "session_id": "test_execute_session"
                }
                
                success, response, status_code = self.make_request(
                    "POST", "/ai/execute", execute_data, auth_token=self.tokens["employee"]
                )
                
                # Check if response is valid JSON without 500 errors
                if success and status_code != 500:
                    self.log_result(
                        f"AI Execute: '{prompt[:20]}...'",
                        True,
                        "AI execute processed request without 500 error"
                    )
                else:
                    self.log_result(
                        f"AI Execute: '{prompt[:20]}...'",
                        False,
                        "AI execute failed or returned 500 error",
                        f"Status: {status_code}, Response: {response}"
                    )
    
    def test_notifications_management(self):
        """Test notification management endpoints"""
        print("\n=== Testing Notification Management ===")
        
        if "employee" in self.tokens:
            # Get notifications
            success, notifications, status_code = self.make_request(
                "GET", "/notifications", auth_token=self.tokens["employee"]
            )
            
            if success and isinstance(notifications, list):
                self.log_result(
                    "Get Notifications",
                    True,
                    f"Employee retrieved {len(notifications)} notifications"
                )
                
                # Mark a notification as read if any exist
                if notifications:
                    notification_id = notifications[0].get("id")
                    if notification_id:
                        success, response, status_code = self.make_request(
                            "PATCH", f"/notifications/{notification_id}/read", 
                            auth_token=self.tokens["employee"]
                        )
                        
                        if success:
                            self.log_result(
                                "Mark Notification Read",
                                True,
                                "Successfully marked notification as read"
                            )
                        else:
                            self.log_result(
                                "Mark Notification Read",
                                False,
                                "Failed to mark notification as read",
                                f"Status: {status_code}, Response: {response}"
                            )
                
                # Mark all notifications as read
                success, response, status_code = self.make_request(
                    "PATCH", "/notifications/mark-all-read", 
                    auth_token=self.tokens["employee"]
                )
                
                if success:
                    self.log_result(
                        "Mark All Notifications Read",
                        True,
                        "Successfully marked all notifications as read"
                    )
                else:
                    self.log_result(
                        "Mark All Notifications Read",
                        False,
                        "Failed to mark all notifications as read",
                        f"Status: {status_code}, Response: {response}"
                    )
            else:
                self.log_result(
                    "Get Notifications",
                    False,
                    "Employee failed to get notifications",
                    f"Status: {status_code}, Response: {notifications}"
                )
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive OperAI Backend Testing")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run tests in logical order
        self.test_auth_register_and_login()
        self.test_auth_me_endpoint()
        self.test_rbac_route_protection()
        self.test_user_management()
        self.test_tasks_crud()
        self.test_attendance_flow()
        self.test_leave_management()
        self.test_deadline_requests()
        self.test_announcements_and_notifications()
        self.test_ai_endpoints()
        self.test_notifications_management()
        
        # Summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   ❌ {result['test']}: {result['message']}")
                    if result["details"]:
                        print(f"      Details: {result['details']}")
        
        return self.test_results

if __name__ == "__main__":
    tester = OperAITester()
    results = tester.run_all_tests()
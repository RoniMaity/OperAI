from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Callable
import logging
import uuid

logger = logging.getLogger(__name__)


class AIActionExecutor:
    def __init__(self, db, user_id: str, user_role: str, user_email: str = None):
        self.db = db
        self.user_id = user_id
        self.user_role = user_role
        self.user_email = user_email
        self.action_registry = self._build_action_registry()
    
    def _build_action_registry(self) -> Dict[str, Callable]:
        """Build registry of all available actions"""
        return {
            "create_task": self._create_task,
            "update_task_status": self._update_task_status,
            "reassign_task": self._reassign_task,
            "list_user_tasks": self._list_user_tasks,
            "apply_leave": self._apply_leave,
            "cancel_leave": self._cancel_leave,
            "approve_leave": self._approve_leave,
            "reject_leave": self._reject_leave,
            "list_pending_leaves": self._list_pending_leaves,
            "mark_attendance": self._mark_attendance,
            "update_work_mode": self._update_work_mode,
            "create_announcement": self._create_announcement,
            "list_team_tasks": self._list_team_tasks,
            "generate_team_summary": self._generate_team_summary,
            "generate_employee_report": self._generate_employee_report,
            "generate_intern_evaluation": self._generate_intern_evaluation,
        }
    
    async def execute_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an AI action with RBAC checks"""
        try:
            action_func = self.action_registry.get(action)
            if not action_func:
                return {"success": False, "error": f"Unknown action: {action}", "action": action}
            
            return await action_func(params)
        except Exception as e:
            logger.error(f"Action execution error for {action}: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e), "action": action}
    
    async def _create_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {
                "success": False,
                "action": "create_task",
                "error": "Only HR, Admin, and Team Leads can create tasks"
            }
        
        task_id = str(uuid.uuid4())
        assigned_to = params.get("assigned_to", self.user_id)
        
        # Verify assignee exists
        assignee = await self.db.users.find_one({"id": assigned_to})
        if not assignee and assigned_to != self.user_id:
            return {
                "success": False,
                "action": "create_task",
                "error": f"User not found: {assigned_to}"
            }
        
        task = {
            "id": task_id,
            "title": params.get("title"),
            "description": params.get("description", ""),
            "assigned_to": assigned_to,
            "created_by": self.user_id,
            "status": "todo",
            "priority": params.get("priority", "medium"),
            "progress": 0,
            "deadline": params.get("deadline"),
            "notes": "",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.db.tasks.insert_one(task)
        
        return {
            "success": True,
            "action": "create_task",
            "details": {
                "task_id": task_id,
                "title": params.get("title"),
                "assigned_to": assigned_to,
                "priority": params.get("priority", "medium"),
                "deadline": params.get("deadline")
            }
        }
    
    async def _update_task_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update task status"""
        task_id = params.get("task_id")
        new_status = params.get("status")
        progress = params.get("progress")
        
        if not task_id:
            return {"success": False, "action": "update_task_status", "error": "task_id required"}
        
        task = await self.db.tasks.find_one({"id": task_id})
        if not task:
            return {"success": False, "action": "update_task_status", "error": "Task not found"}
        
        if self.user_role not in ["admin", "hr", "team_lead"] and task["assigned_to"] != self.user_id:
            return {"success": False, "action": "update_task_status", "error": "Insufficient permissions"}
        
        update_fields = {"updated_at": datetime.now(timezone.utc).isoformat()}
        
        if new_status:
            update_fields["status"] = new_status
            if new_status == "completed" and progress != 100:
                update_fields["progress"] = 100
        
        if progress is not None:
            update_fields["progress"] = min(100, max(0, int(progress)))
        
        await self.db.tasks.update_one({"id": task_id}, {"$set": update_fields})
        
        return {
            "success": True,
            "action": "update_task_status",
            "details": {
                "task_id": task_id,
                "task_title": task.get("title"),
                "new_status": new_status,
                "progress": update_fields.get("progress", task.get("progress"))
            }
        }
    
    async def _reassign_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Reassign task to another user"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "reassign_task", "error": "Only HR/Team Lead can reassign tasks"}
        
        task_id = params.get("task_id")
        new_assignee_email = params.get("new_assignee_email")
        new_assignee_id = params.get("new_assignee_id")
        
        if not task_id:
            return {"success": False, "action": "reassign_task", "error": "task_id required"}
        
        task = await self.db.tasks.find_one({"id": task_id})
        if not task:
            return {"success": False, "action": "reassign_task", "error": "Task not found"}
        
        # Find new assignee
        if new_assignee_email:
            new_user = await self.db.users.find_one({"email": new_assignee_email})
            if new_user:
                new_assignee_id = new_user["id"]
        
        if not new_assignee_id:
            return {"success": False, "action": "reassign_task", "error": "New assignee not found"}
        
        await self.db.tasks.update_one(
            {"id": task_id},
            {"$set": {
                "assigned_to": new_assignee_id,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        new_user = await self.db.users.find_one({"id": new_assignee_id})
        
        return {
            "success": True,
            "action": "reassign_task",
            "details": {
                "task_id": task_id,
                "task_title": task.get("title"),
                "new_assignee": new_user.get("name") if new_user else new_assignee_id
            }
        }
    
    async def _list_user_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List tasks for current user or specified user"""
        user_id = params.get("user_id", self.user_id)
        status_filter = params.get("status")
        
        # Permission check
        if user_id != self.user_id and self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "list_user_tasks", "error": "Cannot view other users' tasks"}
        
        query = {"assigned_to": user_id}
        if status_filter:
            query["status"] = status_filter
        
        tasks = await self.db.tasks.find(query).to_list(100)
        
        task_summaries = []
        for task in tasks:
            task_summaries.append({
                "id": task["id"],
                "title": task["title"],
                "status": task["status"],
                "priority": task["priority"],
                "progress": task.get("progress", 0),
                "deadline": task.get("deadline")
            })
        
        return {
            "success": True,
            "action": "list_user_tasks",
            "details": {
                "count": len(task_summaries),
                "tasks": task_summaries
            }
        }
    
    async def _apply_leave(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply for leave"""
        leave_id = str(uuid.uuid4())
        
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        
        if not start_date or not end_date:
            return {"success": False, "action": "apply_leave", "error": "start_date and end_date required"}
        
        leave = {
            "id": leave_id,
            "user_id": self.user_id,
            "leave_type": params.get("leave_type", "casual"),
            "start_date": start_date,
            "end_date": end_date,
            "reason": params.get("reason", "Personal"),
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.db.leaves.insert_one(leave)
        
        return {
            "success": True,
            "action": "apply_leave",
            "details": {
                "leave_id": leave_id,
                "leave_type": params.get("leave_type", "casual"),
                "start_date": start_date,
                "end_date": end_date,
                "status": "pending"
            }
        }
    
    async def _cancel_leave(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cancel own pending leave"""
        leave_id = params.get("leave_id")
        
        if not leave_id:
            return {"success": False, "action": "cancel_leave", "error": "leave_id required"}
        
        leave = await self.db.leaves.find_one({"id": leave_id, "user_id": self.user_id})
        if not leave:
            return {"success": False, "action": "cancel_leave", "error": "Leave not found or not yours"}
        
        if leave["status"] != "pending":
            return {"success": False, "action": "cancel_leave", "error": f"Cannot cancel {leave['status']} leave"}
        
        await self.db.leaves.update_one(
            {"id": leave_id},
            {"$set": {
                "status": "cancelled",
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {
            "success": True,
            "action": "cancel_leave",
            "details": {
                "leave_id": leave_id,
                "status": "cancelled"
            }
        }
    
    async def _approve_leave(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Approve leave request"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "approve_leave", "error": "Only HR/Team Lead can approve leave"}
        
        leave_id = params.get("leave_id")
        
        if not leave_id:
            return {"success": False, "action": "approve_leave", "error": "leave_id required"}
        
        leave = await self.db.leaves.find_one({"id": leave_id})
        if not leave:
            return {"success": False, "action": "approve_leave", "error": "Leave request not found"}
        
        if leave["status"] != "pending":
            return {"success": False, "action": "approve_leave", "error": f"Leave is {leave['status']}, cannot approve"}
        
        await self.db.leaves.update_one(
            {"id": leave_id},
            {"$set": {
                "status": "approved",
                "approved_by": self.user_id,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        user = await self.db.users.find_one({"id": leave["user_id"]})
        
        return {
            "success": True,
            "action": "approve_leave",
            "details": {
                "leave_id": leave_id,
                "user": user.get("name") if user else leave["user_id"],
                "dates": f"{leave['start_date']} to {leave['end_date']}",
                "status": "approved"
            }
        }
    
    async def _reject_leave(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Reject leave request"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "reject_leave", "error": "Only HR/Team Lead can reject leave"}
        
        leave_id = params.get("leave_id")
        reason = params.get("reason", "Not approved")
        
        if not leave_id:
            return {"success": False, "action": "reject_leave", "error": "leave_id required"}
        
        leave = await self.db.leaves.find_one({"id": leave_id})
        if not leave:
            return {"success": False, "action": "reject_leave", "error": "Leave request not found"}
        
        await self.db.leaves.update_one(
            {"id": leave_id},
            {"$set": {
                "status": "rejected",
                "approved_by": self.user_id,
                "rejection_reason": reason,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        user = await self.db.users.find_one({"id": leave["user_id"]})
        
        return {
            "success": True,
            "action": "reject_leave",
            "details": {
                "leave_id": leave_id,
                "user": user.get("name") if user else leave["user_id"],
                "status": "rejected",
                "reason": reason
            }
        }
    
    async def _list_pending_leaves(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all pending leave requests (HR/Team Lead only)"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "list_pending_leaves", "error": "Insufficient permissions"}
        
        leaves = await self.db.leaves.find({"status": "pending"}).to_list(100)
        
        leave_summaries = []
        for leave in leaves:
            user = await self.db.users.find_one({"id": leave["user_id"]})
            leave_summaries.append({
                "leave_id": leave["id"],
                "user": user.get("name") if user else leave["user_id"],
                "user_email": user.get("email") if user else "",
                "leave_type": leave["leave_type"],
                "start_date": leave["start_date"],
                "end_date": leave["end_date"],
                "reason": leave["reason"]
            })
        
        return {
            "success": True,
            "action": "list_pending_leaves",
            "details": {
                "count": len(leave_summaries),
                "leaves": leave_summaries
            }
        }
    
    async def _mark_attendance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mark attendance"""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        existing = await self.db.attendance.find_one({"user_id": self.user_id, "date": today})
        if existing:
            return {"success": False, "action": "mark_attendance", "error": "Already marked attendance for today"}
        
        work_mode = params.get("work_mode", "wfo")
        
        attendance = {
            "id": str(uuid.uuid4()),
            "user_id": self.user_id,
            "date": today,
            "check_in": datetime.now(timezone.utc).isoformat(),
            "check_out": None,
            "status": "present" if work_mode == "wfo" else "wfh",
            "work_mode": work_mode,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.db.attendance.insert_one(attendance)
        
        return {
            "success": True,
            "action": "mark_attendance",
            "details": {
                "date": today,
                "work_mode": work_mode,
                "status": attendance["status"],
                "check_in": datetime.now(timezone.utc).strftime("%H:%M")
            }
        }
    
    async def _update_work_mode(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update work mode for today"""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        work_mode = params.get("work_mode")
        
        if not work_mode:
            return {"success": False, "action": "update_work_mode", "error": "work_mode required (wfo/wfh/hybrid)"}
        
        attendance = await self.db.attendance.find_one({"user_id": self.user_id, "date": today})
        if not attendance:
            return {"success": False, "action": "update_work_mode", "error": "No attendance record for today. Mark attendance first"}
        
        await self.db.attendance.update_one(
            {"user_id": self.user_id, "date": today},
            {"$set": {
                "work_mode": work_mode,
                "status": "present" if work_mode == "wfo" else "wfh"
            }}
        )
        
        return {
            "success": True,
            "action": "update_work_mode",
            "details": {
                "date": today,
                "work_mode": work_mode
            }
        }
    
    async def _create_announcement(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create announcement"""
        if self.user_role not in ["admin", "hr"]:
            return {"success": False, "action": "create_announcement", "error": "Only HR/Admin can create announcements"}
        
        title = params.get("title")
        content = params.get("content")
        
        if not title or not content:
            return {"success": False, "action": "create_announcement", "error": "title and content required"}
        
        announcement_id = str(uuid.uuid4())
        
        announcement = {
            "id": announcement_id,
            "title": title,
            "content": content,
            "created_by": self.user_id,
            "target_roles": params.get("target_roles", []),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.db.announcements.insert_one(announcement)
        
        return {
            "success": True,
            "action": "create_announcement",
            "details": {
                "announcement_id": announcement_id,
                "title": title,
                "target_audience": "All employees" if not params.get("target_roles") else ", ".join(params.get("target_roles"))
            }
        }
    
    async def _list_team_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all tasks for the team (Team Lead only)"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "list_team_tasks", "error": "Only Team Leads can view team tasks"}
        
        # Get all tasks created by this team lead
        tasks = await self.db.tasks.find({"created_by": self.user_id}).to_list(100)
        
        task_summaries = []
        for task in tasks:
            assignee = await self.db.users.find_one({"id": task["assigned_to"]})
            task_summaries.append({
                "task_id": task["id"],
                "title": task["title"],
                "assignee": assignee.get("name") if assignee else task["assigned_to"],
                "status": task["status"],
                "priority": task["priority"],
                "progress": task.get("progress", 0)
            })
        
        return {
            "success": True,
            "action": "list_team_tasks",
            "details": {
                "count": len(task_summaries),
                "tasks": task_summaries
            }
        }
    
    async def _generate_team_summary(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate team summary (Team Lead only)"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "action": "generate_team_summary", "error": "Only Team Leads can generate team summaries"}
        
        # Get team tasks
        tasks = await self.db.tasks.find({"created_by": self.user_id}).to_list(1000)
        
        total_tasks = len(tasks)
        completed = len([t for t in tasks if t["status"] == "completed"])
        in_progress = len([t for t in tasks if t["status"] == "in_progress"])
        pending = len([t for t in tasks if t["status"] == "todo"])
        blocked = len([t for t in tasks if t["status"] == "blocked"])
        
        return {
            "success": True,
            "action": "generate_team_summary",
            "details": {
                "total_tasks": total_tasks,
                "completed": completed,
                "in_progress": in_progress,
                "pending": pending,
                "blocked": blocked,
                "completion_rate": f"{(completed/total_tasks*100):.1f}%" if total_tasks > 0 else "0%"
            }
        }
    
    async def _generate_employee_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate employee report (HR only)"""
        if self.user_role not in ["admin", "hr"]:
            return {"success": False, "action": "generate_employee_report", "error": "Only HR can generate employee reports"}
        
        employee_email = params.get("employee_email")
        if not employee_email:
            return {"success": False, "action": "generate_employee_report", "error": "employee_email required"}
        
        employee = await self.db.users.find_one({"email": employee_email})
        if not employee:
            return {"success": False, "action": "generate_employee_report", "error": "Employee not found"}
        
        employee_id = employee["id"]
        
        # Get tasks
        tasks = await self.db.tasks.find({"assigned_to": employee_id}).to_list(1000)
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t["status"] == "completed"])
        
        # Get attendance (last 30 days)
        end_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        start_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')
        attendance = await self.db.attendance.find({
            "user_id": employee_id,
            "date": {"$gte": start_date, "$lte": end_date}
        }).to_list(100)
        
        present_days = len([a for a in attendance if a["status"] in ["present", "wfh"]])
        
        # Get leaves
        leaves = await self.db.leaves.find({"user_id": employee_id}).to_list(100)
        total_leaves = len(leaves)
        
        return {
            "success": True,
            "action": "generate_employee_report",
            "details": {
                "employee": employee.get("name"),
                "email": employee_email,
                "role": employee.get("role"),
                "tasks": {
                    "total": total_tasks,
                    "completed": completed_tasks,
                    "completion_rate": f"{(completed_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "0%"
                },
                "attendance": {
                    "present_days": present_days,
                    "period": "last_30_days",
                    "attendance_rate": f"{(present_days/30*100):.1f}%"
                },
                "leaves": {
                    "total_requests": total_leaves
                }
            }
        }
    
    async def _generate_intern_evaluation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intern evaluation (HR only)"""
        if self.user_role not in ["admin", "hr"]:
            return {"success": False, "action": "generate_intern_evaluation", "error": "Only HR can generate intern evaluations"}
        
        intern_email = params.get("intern_email")
        if not intern_email:
            return {"success": False, "action": "generate_intern_evaluation", "error": "intern_email required"}
        
        intern = await self.db.users.find_one({"email": intern_email, "role": "intern"})
        if not intern:
            return {"success": False, "action": "generate_intern_evaluation", "error": "Intern not found"}
        
        intern_id = intern["id"]
        
        # Get tasks
        tasks = await self.db.tasks.find({"assigned_to": intern_id}).to_list(1000)
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t["status"] == "completed"])
        avg_progress = sum([t.get("progress", 0) for t in tasks]) / total_tasks if total_tasks > 0 else 0
        
        # Get attendance
        attendance = await self.db.attendance.find({"user_id": intern_id}).to_list(1000)
        total_days = len(attendance)
        present_days = len([a for a in attendance if a["status"] in ["present", "wfh"]])
        
        # Simple evaluation
        performance_score = (completed_tasks / total_tasks * 50 + avg_progress * 0.3 + present_days / total_days * 20) if total_tasks > 0 and total_days > 0 else 0
        
        return {
            "success": True,
            "action": "generate_intern_evaluation",
            "details": {
                "intern": intern.get("name"),
                "email": intern_email,
                "tasks": {
                    "total": total_tasks,
                    "completed": completed_tasks,
                    "avg_progress": f"{avg_progress:.1f}%"
                },
                "attendance": {
                    "total_days": total_days,
                    "present_days": present_days,
                    "rate": f"{(present_days/total_days*100):.1f}%" if total_days > 0 else "0%"
                },
                "performance_score": f"{performance_score:.1f}/100",
                "recommendation": "Good performance" if performance_score > 70 else "Needs improvement"
            }
        }


def get_action_definitions() -> List[Dict[str, Any]]:
    """Return available actions with descriptions"""
    return [
        {
            "name": "create_task",
            "description": "Create a new task",
            "parameters": {
                "title": "Task title (required)",
                "description": "Task description (optional)",
                "assigned_to": "User ID to assign task to (optional, defaults to self)",
                "priority": "Priority: low, medium, high, urgent (optional, default: medium)",
                "deadline": "Deadline in ISO format YYYY-MM-DD (optional)"
            },
            "permissions": ["admin", "hr", "team_lead"]
        },
        {
            "name": "update_task_status",
            "description": "Update task status",
            "parameters": {
                "task_id": "Task ID (required)",
                "status": "New status: todo, in_progress, completed, blocked (required)"
            },
            "permissions": ["admin", "hr", "team_lead", "employee", "intern"]
        },
        {
            "name": "reassign_task",
            "description": "Reassign task to another user",
            "parameters": {
                "task_id": "Task ID (required)",
                "new_assignee": "New assignee user ID (required)"
            },
            "permissions": ["admin", "hr", "team_lead"]
        },
        {
            "name": "apply_leave",
            "description": "Apply for leave",
            "parameters": {
                "leave_type": "Leave type: sick, casual, earned, unpaid (required)",
                "start_date": "Start date YYYY-MM-DD (required)",
                "end_date": "End date YYYY-MM-DD (required)",
                "reason": "Reason for leave (required)"
            },
            "permissions": ["admin", "hr", "team_lead", "employee", "intern"]
        },
        {
            "name": "approve_leave",
            "description": "Approve a leave request",
            "parameters": {
                "leave_id": "Leave request ID (required)"
            },
            "permissions": ["admin", "hr", "team_lead"]
        },
        {
            "name": "reject_leave",
            "description": "Reject a leave request",
            "parameters": {
                "leave_id": "Leave request ID (required)",
                "reason": "Reason for rejection (required)"
            },
            "permissions": ["admin", "hr", "team_lead"]
        },
        {
            "name": "mark_attendance",
            "description": "Mark attendance for today",
            "parameters": {
                "work_mode": "Work mode: wfo, wfh, hybrid (required)"
            },
            "permissions": ["admin", "hr", "team_lead", "employee", "intern"]
        },
        {
            "name": "update_work_mode",
            "description": "Update work mode for today's attendance",
            "parameters": {
                "work_mode": "New work mode: wfo, wfh, hybrid (required)"
            },
            "permissions": ["admin", "hr", "team_lead", "employee", "intern"]
        },
        {
            "name": "create_announcement",
            "description": "Create a company announcement",
            "parameters": {
                "title": "Announcement title (required)",
                "content": "Announcement content (required)",
                "target_roles": "Target roles array (optional, empty means all)"
            },
            "permissions": ["admin", "hr"]
        },
        {
            "name": "generate_report",
            "description": "Generate various reports",
            "parameters": {
                "report_type": "Report type: tasks, attendance, summary (required)"
            },
            "permissions": ["admin", "hr", "team_lead", "employee", "intern"]
        }
    ]

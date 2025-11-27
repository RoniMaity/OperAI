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
            return {"success": False, "error": "Insufficient permissions to approve leave"}
        
        leave_id = params.get("leave_id")
        
        leave = await self.db.leaves.find_one({"id": leave_id})
        if not leave:
            return {"success": False, "error": "Leave request not found"}
        
        await self.db.leaves.update_one(
            {"id": leave_id},
            {"$set": {
                "status": "approved",
                "approved_by": self.user_id,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {
            "success": True,
            "action": "approve_leave",
            "details": {
                "leave_id": leave_id,
                "status": "approved"
            }
        }
    
    async def _reject_leave(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Reject leave request"""
        if self.user_role not in ["admin", "hr", "team_lead"]:
            return {"success": False, "error": "Insufficient permissions to reject leave"}
        
        leave_id = params.get("leave_id")
        reason = params.get("reason", "Not approved")
        
        leave = await self.db.leaves.find_one({"id": leave_id})
        if not leave:
            return {"success": False, "error": "Leave request not found"}
        
        await self.db.leaves.update_one(
            {"id": leave_id},
            {"$set": {
                "status": "rejected",
                "approved_by": self.user_id,
                "rejection_reason": reason,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        return {
            "success": True,
            "action": "reject_leave",
            "details": {
                "leave_id": leave_id,
                "status": "rejected",
                "reason": reason
            }
        }
    
    async def _mark_attendance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mark attendance"""
        import uuid
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        existing = await self.db.attendance.find_one({"user_id": self.user_id, "date": today})
        if existing:
            return {"success": False, "error": "Already marked attendance for today"}
        
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
                "status": attendance["status"]
            }
        }
    
    async def _update_work_mode(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update work mode for today"""
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        work_mode = params.get("work_mode")
        
        attendance = await self.db.attendance.find_one({"user_id": self.user_id, "date": today})
        if not attendance:
            return {"success": False, "error": "No attendance record for today"}
        
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
            return {"success": False, "error": "Insufficient permissions to create announcements"}
        
        import uuid
        announcement_id = str(uuid.uuid4())
        
        announcement = {
            "id": announcement_id,
            "title": params.get("title"),
            "content": params.get("content"),
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
                "title": params.get("title"),
                "target_roles": params.get("target_roles", [])
            }
        }
    
    async def _generate_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report"""
        report_type = params.get("report_type", "summary")
        
        if report_type == "tasks":
            tasks = await self.db.tasks.find({"assigned_to": self.user_id}).to_list(1000)
            total = len(tasks)
            completed = len([t for t in tasks if t["status"] == "completed"])
            pending = len([t for t in tasks if t["status"] in ["todo", "in_progress"]])
            
            return {
                "success": True,
                "action": "generate_report",
                "details": {
                    "report_type": "tasks",
                    "total_tasks": total,
                    "completed": completed,
                    "pending": pending
                }
            }
        
        elif report_type == "attendance":
            from datetime import timedelta
            end_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            start_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')
            
            records = await self.db.attendance.find({
                "user_id": self.user_id,
                "date": {"$gte": start_date, "$lte": end_date}
            }).to_list(1000)
            
            present_days = len([r for r in records if r["status"] in ["present", "wfh"]])
            
            return {
                "success": True,
                "action": "generate_report",
                "details": {
                    "report_type": "attendance",
                    "period": "last_30_days",
                    "present_days": present_days,
                    "total_days": 30
                }
            }
        
        return {
            "success": True,
            "action": "generate_report",
            "details": {
                "report_type": report_type,
                "message": "Report generated successfully"
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

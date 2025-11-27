from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt
from emergentintegrations.llm.chat import LlmChat, UserMessage


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = os.environ['JWT_ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 60))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get('REFRESH_TOKEN_EXPIRE_DAYS', 7))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ===== MODELS =====
class TokenData(BaseModel):
    user_id: str
    email: str
    role: str


class UserRole:
    ADMIN = "admin"
    HR = "hr"
    TEAM_LEAD = "team_lead"
    EMPLOYEE = "employee"
    INTERN = "intern"


class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    name: str
    role: str
    department_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str
    department_id: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User


class Department(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TaskStatus:
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    assigned_to: str  # user_id
    created_by: str  # user_id
    status: str = TaskStatus.TODO
    priority: str = TaskPriority.MEDIUM
    progress: int = 0  # 0-100
    deadline: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: str
    priority: str = TaskPriority.MEDIUM
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    progress: Optional[int] = None
    notes: Optional[str] = None
    deadline: Optional[datetime] = None


class AttendanceStatus:
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LATE = "late"
    WFH = "wfh"


class WorkMode:
    WFO = "wfo"  # Work from office
    WFH = "wfh"  # Work from home
    HYBRID = "hybrid"


class Attendance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    date: str  # YYYY-MM-DD
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: str = AttendanceStatus.ABSENT
    work_mode: str = WorkMode.WFO
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AttendanceCheckIn(BaseModel):
    work_mode: str = WorkMode.WFO


class AttendanceCheckOut(BaseModel):
    notes: Optional[str] = None


class LeaveType:
    SICK = "sick"
    CASUAL = "casual"
    EARNED = "earned"
    UNPAID = "unpaid"


class LeaveStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class Leave(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    leave_type: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    reason: str
    status: str = LeaveStatus.PENDING
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LeaveCreate(BaseModel):
    leave_type: str
    start_date: str
    end_date: str
    reason: str


class LeaveUpdate(BaseModel):
    status: str
    rejection_reason: Optional[str] = None


class Announcement(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    created_by: str  # user_id
    target_roles: List[str] = []  # Empty means all roles
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    target_roles: Optional[List[str]] = []


class AIMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_id: str
    message: str
    response: str
    action_type: Optional[str] = None  # rewrite, explain, breakdown, report
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AIRequest(BaseModel):
    message: str
    session_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    action_type: Optional[str] = None


# ===== HELPER FUNCTIONS =====
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return TokenData(
            user_id=payload.get("user_id"),
            email=payload.get("email"),
            role=payload.get("role")
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    token = credentials.credentials
    return decode_token(token)


def require_role(*allowed_roles: str):
    async def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker


# ===== AUTH ENDPOINTS =====
@api_router.post("/auth/register", response_model=User)
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user
    user = User(
        email=user_data.email,
        name=user_data.name,
        role=user_data.role,
        department_id=user_data.department_id
    )
    
    doc = user.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['password'] = hashed_password
    
    await db.users.insert_one(doc)
    return user


@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    # Find user
    user_doc = await db.users.find_one({"email": credentials.email})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(credentials.password, user_doc['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Check if user is active
    if not user_doc.get('is_active', True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    
    # Create tokens
    token_data = {
        "user_id": user_doc['id'],
        "email": user_doc['email'],
        "role": user_doc['role']
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Convert user doc to User model
    user_doc.pop('password')
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    user = User(**user_doc)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )


@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: TokenData = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": current_user.user_id}, {"_id": 0, "password": 0})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    return User(**user_doc)


# ===== USER MANAGEMENT (HR/Admin only) =====
@api_router.get("/users", response_model=List[User])
async def get_users(current_user: TokenData = Depends(require_role(UserRole.ADMIN, UserRole.HR))):
    users = await db.users.find({}, {"_id": 0, "password": 0}).to_list(1000)
    for user in users:
        if isinstance(user.get('created_at'), str):
            user['created_at'] = datetime.fromisoformat(user['created_at'])
    return users


@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, current_user: TokenData = Depends(get_current_user)):
    user_doc = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if isinstance(user_doc.get('created_at'), str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    return User(**user_doc)


# ===== DEPARTMENTS =====
@api_router.post("/departments", response_model=Department)
async def create_department(
    dept_data: DepartmentCreate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN, UserRole.HR))
):
    department = Department(
        name=dept_data.name,
        description=dept_data.description
    )
    
    doc = department.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.departments.insert_one(doc)
    return department


@api_router.get("/departments", response_model=List[Department])
async def get_departments(current_user: TokenData = Depends(get_current_user)):
    departments = await db.departments.find({}, {"_id": 0}).to_list(1000)
    for dept in departments:
        if isinstance(dept.get('created_at'), str):
            dept['created_at'] = datetime.fromisoformat(dept['created_at'])
    return departments


# ===== TASKS =====
@api_router.post("/tasks", response_model=Task)
async def create_task(
    task_data: TaskCreate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN, UserRole.HR, UserRole.TEAM_LEAD))
):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        assigned_to=task_data.assigned_to,
        created_by=current_user.user_id,
        priority=task_data.priority,
        deadline=task_data.deadline
    )
    
    doc = task.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    if doc['deadline']:
        doc['deadline'] = doc['deadline'].isoformat()
    
    await db.tasks.insert_one(doc)
    return task


@api_router.get("/tasks", response_model=List[Task])
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[str] = None,
    created_by: Optional[str] = None,
    current_user: TokenData = Depends(get_current_user)
):
    query = {}
    
    # Access control
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        # Can see all tasks
        if assigned_to:
            query["assigned_to"] = assigned_to
        if created_by:
            query["created_by"] = created_by
    elif current_user.role == UserRole.TEAM_LEAD:
        # Can see tasks they created or tasks assigned to them
        query["$or"] = [
            {"created_by": current_user.user_id},
            {"assigned_to": current_user.user_id}
        ]
    else:
        # Can only see their own tasks
        query["assigned_to"] = current_user.user_id
    
    # Filters
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    
    tasks = await db.tasks.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for task in tasks:
        if isinstance(task.get('created_at'), str):
            task['created_at'] = datetime.fromisoformat(task['created_at'])
        if isinstance(task.get('updated_at'), str):
            task['updated_at'] = datetime.fromisoformat(task['updated_at'])
        if isinstance(task.get('deadline'), str):
            task['deadline'] = datetime.fromisoformat(task['deadline'])
    
    return tasks


@api_router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, current_user: TokenData = Depends(get_current_user)):
    task_doc = await db.tasks.find_one({"id": task_id}, {"_id": 0})
    if not task_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # Check access
    if current_user.role not in [UserRole.ADMIN, UserRole.HR, UserRole.TEAM_LEAD]:
        if task_doc["assigned_to"] != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    if isinstance(task_doc.get('created_at'), str):
        task_doc['created_at'] = datetime.fromisoformat(task_doc['created_at'])
    if isinstance(task_doc.get('updated_at'), str):
        task_doc['updated_at'] = datetime.fromisoformat(task_doc['updated_at'])
    if isinstance(task_doc.get('deadline'), str):
        task_doc['deadline'] = datetime.fromisoformat(task_doc['deadline'])
    
    return Task(**task_doc)


@api_router.patch("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: TokenData = Depends(get_current_user)
):
    task_doc = await db.tasks.find_one({"id": task_id})
    if not task_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.HR, UserRole.TEAM_LEAD]:
        if task_doc["assigned_to"] != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only update your own tasks")
    
    update_data = {"updated_at": datetime.now(timezone.utc).isoformat()}
    
    if task_update.title is not None:
        update_data["title"] = task_update.title
    if task_update.description is not None:
        update_data["description"] = task_update.description
    if task_update.status is not None:
        update_data["status"] = task_update.status
    if task_update.priority is not None:
        update_data["priority"] = task_update.priority
    if task_update.progress is not None:
        update_data["progress"] = min(100, max(0, task_update.progress))
    if task_update.notes is not None:
        update_data["notes"] = task_update.notes
    if task_update.deadline is not None:
        update_data["deadline"] = task_update.deadline.isoformat()
    
    await db.tasks.update_one({"id": task_id}, {"$set": update_data})
    
    updated_task = await db.tasks.find_one({"id": task_id}, {"_id": 0})
    
    if isinstance(updated_task.get('created_at'), str):
        updated_task['created_at'] = datetime.fromisoformat(updated_task['created_at'])
    if isinstance(updated_task.get('updated_at'), str):
        updated_task['updated_at'] = datetime.fromisoformat(updated_task['updated_at'])
    if isinstance(updated_task.get('deadline'), str):
        updated_task['deadline'] = datetime.fromisoformat(updated_task['deadline'])
    
    return Task(**updated_task)


# ===== ATTENDANCE =====
@api_router.post("/attendance/check-in", response_model=Attendance)
async def check_in(
    attendance_data: AttendanceCheckIn,
    current_user: TokenData = Depends(get_current_user)
):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    # Check if already checked in today
    existing = await db.attendance.find_one({"user_id": current_user.user_id, "date": today})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already checked in today")
    
    attendance = Attendance(
        user_id=current_user.user_id,
        date=today,
        check_in=datetime.now(timezone.utc),
        work_mode=attendance_data.work_mode,
        status=AttendanceStatus.PRESENT if attendance_data.work_mode == WorkMode.WFO else AttendanceStatus.WFH
    )
    
    doc = attendance.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    if doc['check_in']:
        doc['check_in'] = doc['check_in'].isoformat()
    
    await db.attendance.insert_one(doc)
    return attendance


@api_router.post("/attendance/check-out", response_model=Attendance)
async def check_out(
    checkout_data: AttendanceCheckOut,
    current_user: TokenData = Depends(get_current_user)
):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    # Find today's attendance record
    attendance_doc = await db.attendance.find_one({"user_id": current_user.user_id, "date": today})
    
    if not attendance_doc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not checked in yet")
    
    if attendance_doc.get('check_out'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already checked out")
    
    update_data = {
        "check_out": datetime.now(timezone.utc).isoformat()
    }
    
    if checkout_data.notes:
        update_data["notes"] = checkout_data.notes
    
    await db.attendance.update_one(
        {"user_id": current_user.user_id, "date": today},
        {"$set": update_data}
    )
    
    updated_attendance = await db.attendance.find_one({"user_id": current_user.user_id, "date": today}, {"_id": 0})
    
    if isinstance(updated_attendance.get('created_at'), str):
        updated_attendance['created_at'] = datetime.fromisoformat(updated_attendance['created_at'])
    if isinstance(updated_attendance.get('check_in'), str):
        updated_attendance['check_in'] = datetime.fromisoformat(updated_attendance['check_in'])
    if isinstance(updated_attendance.get('check_out'), str):
        updated_attendance['check_out'] = datetime.fromisoformat(updated_attendance['check_out'])
    
    return Attendance(**updated_attendance)


@api_router.get("/attendance", response_model=List[Attendance])
async def get_attendance(
    user_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: TokenData = Depends(get_current_user)
):
    # Build query
    query = {}
    
    # Access control
    if current_user.role in [UserRole.ADMIN, UserRole.HR, UserRole.TEAM_LEAD]:
        if user_id:
            query["user_id"] = user_id
    else:
        query["user_id"] = current_user.user_id
    
    # Date range filter
    if start_date and end_date:
        query["date"] = {"$gte": start_date, "$lte": end_date}
    elif start_date:
        query["date"] = {"$gte": start_date}
    elif end_date:
        query["date"] = {"$lte": end_date}
    
    attendance_records = await db.attendance.find(query, {"_id": 0}).sort("date", -1).to_list(1000)
    
    for record in attendance_records:
        if isinstance(record.get('created_at'), str):
            record['created_at'] = datetime.fromisoformat(record['created_at'])
        if isinstance(record.get('check_in'), str):
            record['check_in'] = datetime.fromisoformat(record['check_in'])
        if isinstance(record.get('check_out'), str):
            record['check_out'] = datetime.fromisoformat(record['check_out'])
    
    return attendance_records


# ===== LEAVE MANAGEMENT =====
@api_router.post("/leave", response_model=Leave)
async def apply_leave(
    leave_data: LeaveCreate,
    current_user: TokenData = Depends(get_current_user)
):
    leave = Leave(
        user_id=current_user.user_id,
        leave_type=leave_data.leave_type,
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
        reason=leave_data.reason
    )
    
    doc = leave.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    await db.leaves.insert_one(doc)
    return leave


@api_router.get("/leave", response_model=List[Leave])
async def get_leaves(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user: TokenData = Depends(get_current_user)
):
    query = {}
    
    # Access control
    if current_user.role in [UserRole.ADMIN, UserRole.HR, UserRole.TEAM_LEAD]:
        if user_id:
            query["user_id"] = user_id
        if status:
            query["status"] = status
    else:
        query["user_id"] = current_user.user_id
        if status:
            query["status"] = status
    
    leaves = await db.leaves.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for leave in leaves:
        if isinstance(leave.get('created_at'), str):
            leave['created_at'] = datetime.fromisoformat(leave['created_at'])
        if isinstance(leave.get('updated_at'), str):
            leave['updated_at'] = datetime.fromisoformat(leave['updated_at'])
    
    return leaves


@api_router.patch("/leave/{leave_id}", response_model=Leave)
async def update_leave_status(
    leave_id: str,
    leave_update: LeaveUpdate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN, UserRole.HR, UserRole.TEAM_LEAD))
):
    # FIXED: Changed db.leave to db.leaves
    leave_doc = await db.leaves.find_one({"id": leave_id})
    if not leave_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")
    
    update_data = {
        "status": leave_update.status,
        "approved_by": current_user.user_id,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    if leave_update.rejection_reason:
        update_data["rejection_reason"] = leave_update.rejection_reason
    
    await db.leaves.update_one({"id": leave_id}, {"$set": update_data})
    
    updated_leave = await db.leaves.find_one({"id": leave_id}, {"_id": 0})
    
    if isinstance(updated_leave.get('created_at'), str):
        updated_leave['created_at'] = datetime.fromisoformat(updated_leave['created_at'])
    if isinstance(updated_leave.get('updated_at'), str):
        updated_leave['updated_at'] = datetime.fromisoformat(updated_leave['updated_at'])
    
    return Leave(**updated_leave)


# ===== ANNOUNCEMENTS =====
@api_router.post("/announcements", response_model=Announcement)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    current_user: TokenData = Depends(require_role(UserRole.ADMIN, UserRole.HR))
):
    announcement = Announcement(
        title=announcement_data.title,
        content=announcement_data.content,
        created_by=current_user.user_id,
        target_roles=announcement_data.target_roles if announcement_data.target_roles else []
    )
    
    doc = announcement.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.announcements.insert_one(doc)
    return announcement


@api_router.get("/announcements", response_model=List[Announcement])
async def get_announcements(current_user: TokenData = Depends(get_current_user)):
    # Show announcements targeted to user's role or to all roles
    query = {
        "$or": [
            {"target_roles": []},
            {"target_roles": current_user.role}
        ]
    }
    
    announcements = await db.announcements.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    
    for announcement in announcements:
        if isinstance(announcement.get('created_at'), str):
            announcement['created_at'] = datetime.fromisoformat(announcement['created_at'])
    
    return announcements


# ===== AI ASSISTANT =====
@api_router.post("/ai/chat")
async def ai_chat(
    ai_request: AIRequest,
    current_user: TokenData = Depends(get_current_user)
):
    try:
        # Check if EMERGENT_LLM_KEY is available
        llm_key = os.environ.get('EMERGENT_LLM_KEY')
        if not llm_key:
            return {
                "response": "AI service is temporarily unavailable. Please ensure EMERGENT_LLM_KEY is configured.",
                "session_id": ai_request.session_id,
                "error": "EMERGENT_LLM_KEY not configured"
            }
        
        # Initialize AI chat
        chat = LlmChat(
            api_key=llm_key,
            session_id=ai_request.session_id,
            system_message="You are a helpful AI assistant for WorkforceOS. Help users with task explanations, report generation, announcement rewriting, and general workforce management queries. Be concise and professional."
        )
        
        # Use Gemini 2.5 Flash
        chat.with_model("gemini", "gemini-2.5-flash")
        
        # Send message
        user_message = UserMessage(text=ai_request.message)
        response = await chat.send_message(user_message)
        
        # Save to database
        ai_message = AIMessage(
            user_id=current_user.user_id,
            session_id=ai_request.session_id,
            message=ai_request.message,
            response=response,
            action_type=ai_request.action_type
        )
        
        doc = ai_message.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.ai_messages.insert_one(doc)
        
        return {"response": response, "session_id": ai_request.session_id}
    
    except Exception as e:
        logger.error(f"AI chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "response": "I'm experiencing technical difficulties. Please try again later.",
            "session_id": ai_request.session_id,
            "error": str(e)
        }


@api_router.post("/ai/execute")
async def ai_execute(
    ai_request: AIRequest,
    current_user: TokenData = Depends(get_current_user)
):
    try:
        from services.ai_actions import AIActionExecutor, get_action_definitions
        import json
        from datetime import datetime, timedelta
        
        # Get current user details
        user_doc = await db.users.find_one({"id": current_user.user_id})
        user_email = user_doc.get("email") if user_doc else current_user.email
        
        # Get available actions for user's role
        all_actions = get_action_definitions()
        allowed_actions = [
            a for a in all_actions 
            if current_user.role in a["permissions"]
        ]
        
        # Build actions documentation
        actions_doc = []
        for a in allowed_actions:
            params_str = ", ".join([f"{k}: {v}" for k, v in a["parameters"].items()])
            actions_doc.append(f"  {a['name']}({params_str})")
            actions_doc.append(f"    Purpose: {a['description']}")
        
        actions_list = "\n".join(actions_doc)
        
        # Calculate dates for context
        today = datetime.now(timezone.utc)
        tomorrow = today + timedelta(days=1)
        next_monday = today + timedelta(days=(7 - today.weekday()))
        next_friday = today + timedelta(days=(4 - today.weekday()) if today.weekday() <= 4 else (11 - today.weekday()))
        
        system_prompt = f"""You are OperAI Intelligence - the operational AI for OperAI workforce platform.
You can EXECUTE ACTIONS in the system through natural language commands.

CURRENT CONTEXT:
User: {user_email}
Role: {current_user.role}
Today: {today.strftime('%Y-%m-%d')} ({today.strftime('%A')})
Tomorrow: {tomorrow.strftime('%Y-%m-%d')}
Next Monday: {next_monday.strftime('%Y-%m-%d')}
Next Friday: {next_friday.strftime('%Y-%m-%d')}

AVAILABLE ACTIONS:
{actions_list}

IMPORTANT GUIDELINES:
- When user mentions an email address for task assignment, use the "assigned_to_email" parameter.
- When user asks "show my tasks" or "list my tasks", call list_user_tasks WITHOUT any user_id parameter.
- For date-based queries, use the dates provided in CURRENT CONTEXT.

OUTPUT FORMAT (MUST BE VALID JSON):
{{
  "thought": "What I understood from the user's request",
  "actions": [
    {{
      "name": "action_name",
      "params": {{
        "param1": "value1"
      }}
    }}
  ],
  "response": "Natural language response to user"
}}

IMPORTANT:
- Always return valid JSON
- actions array can have multiple actions
- If no action needed, use empty actions array: []
- Be specific and helpful in your response
"""
        
        # Call AI to determine actions
        chat = LlmChat(
            api_key=os.environ['EMERGENT_LLM_KEY'],
            session_id=ai_request.session_id,
            system_message=system_prompt
        )
        
        chat.with_model("gemini", "gemini-2.5-flash")
        user_message = UserMessage(text=ai_request.message)
        ai_response = await chat.send_message(user_message)
        
        # Parse AI response
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in ai_response:
                json_start = ai_response.find("```json") + 7
                json_end = ai_response.find("```", json_start)
                ai_response = ai_response[json_start:json_end].strip()
            elif "```" in ai_response:
                json_start = ai_response.find("```") + 3
                json_end = ai_response.find("```", json_start)
                ai_response = ai_response[json_start:json_end].strip()
            
            parsed = json.loads(ai_response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {ai_response}")
            return {
                "response": ai_response,
                "actions_executed": [],
                "session_id": ai_request.session_id
            }
        
        # Execute actions
        executor = AIActionExecutor(db, current_user.user_id, current_user.role, user_email)
        
        results = []
        for action in parsed.get("actions", []):
            action_name = action.get("name")
            params = action.get("params", {})
            result = await executor.execute_action(action_name, params)
            results.append(result)
        
        # Save to database
        ai_message = AIMessage(
            user_id=current_user.user_id,
            session_id=ai_request.session_id,
            message=ai_request.message,
            response=parsed.get("response", ""),
            action_type="execute"
        )
        
        doc = ai_message.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.ai_messages.insert_one(doc)
        
        return {
            "response": parsed.get("response", ""),
            "thought": parsed.get("thought", ""),
            "actions_executed": results,
            "session_id": ai_request.session_id
        }
    
    except Exception as e:
        logger.error(f"AI execute error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AI service error: {str(e)}")


@api_router.get("/ai/history")
async def get_ai_history(
    session_id: Optional[str] = None,
    current_user: TokenData = Depends(get_current_user)
):
    query = {"user_id": current_user.user_id}
    if session_id:
        query["session_id"] = session_id
    
    history = await db.ai_messages.find(query, {"_id": 0}).sort("created_at", -1).limit(100).to_list(100)
    
    for msg in history:
        if isinstance(msg.get('created_at'), str):
            msg['created_at'] = datetime.fromisoformat(msg['created_at'])
    
    return history


# ===== DASHBOARD STATS =====
@api_router.get("/dashboard/stats")
async def get_dashboard_stats(current_user: TokenData = Depends(get_current_user)):
    if current_user.role in [UserRole.ADMIN, UserRole.HR]:
        # HR Dashboard stats
        total_employees = await db.users.count_documents({})
        total_tasks = await db.tasks.count_documents({})
        pending_leaves = await db.leaves.count_documents({"status": LeaveStatus.PENDING})
        
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        present_today = await db.attendance.count_documents({
            "date": today,
            "status": {"$in": [AttendanceStatus.PRESENT, AttendanceStatus.WFH]}
        })
        
        return {
            "total_employees": total_employees,
            "total_tasks": total_tasks,
            "pending_leaves": pending_leaves,
            "present_today": present_today
        }
    
    elif current_user.role == UserRole.TEAM_LEAD:
        # Team Lead Dashboard stats
        my_tasks = await db.tasks.count_documents({"assigned_to": current_user.user_id})
        team_tasks = await db.tasks.count_documents({"created_by": current_user.user_id})
        team_tasks_completed = await db.tasks.count_documents({
            "created_by": current_user.user_id,
            "status": TaskStatus.COMPLETED
        })
        team_tasks_pending = await db.tasks.count_documents({
            "created_by": current_user.user_id,
            "status": TaskStatus.TODO
        })
        
        return {
            "my_tasks": my_tasks,
            "team_tasks": team_tasks,
            "team_tasks_completed": team_tasks_completed,
            "team_tasks_pending": team_tasks_pending
        }
    
    else:
        # Employee/Intern Dashboard stats
        my_tasks = await db.tasks.count_documents({"assigned_to": current_user.user_id})
        pending_tasks = await db.tasks.count_documents({
            "assigned_to": current_user.user_id,
            "status": {"$in": [TaskStatus.TODO, TaskStatus.IN_PROGRESS]}
        })
        completed_tasks = await db.tasks.count_documents({
            "assigned_to": current_user.user_id,
            "status": TaskStatus.COMPLETED
        })
        my_leaves = await db.leaves.count_documents({"user_id": current_user.user_id})
        
        return {
            "my_tasks": my_tasks,
            "pending_tasks": pending_tasks,
            "completed_tasks": completed_tasks,
            "my_leaves": my_leaves
        }


# Mount API router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "OperAI WorkforceOS API", "version": "1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

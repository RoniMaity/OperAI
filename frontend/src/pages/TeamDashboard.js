import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Badge } from '../components/ui/badge';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';
import { CheckSquare, TrendingUp, Clock, Users, Plus, UserCheck } from 'lucide-react';

export default function TeamDashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [teamTasks, setTeamTasks] = useState([]);
  const [teamMembers, setTeamMembers] = useState([]);
  const [availableUsers, setAvailableUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    assigned_to: '',
    priority: 'medium',
    deadline: ''
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch stats
      const statsResponse = await api.get('/dashboard/stats');
      setStats(statsResponse.data);
      
      // Fetch all tasks created by current user (team lead)
      const tasksResponse = await api.get('/tasks');
      const allTasks = tasksResponse.data;
      const myTeamTasks = allTasks.filter(task => task.created_by === user.id);
      setTeamTasks(myTeamTasks);
      
      // Extract unique team members from assigned tasks
      const assignedUserIds = [...new Set(myTeamTasks.map(task => task.assigned_to))];
      
      // Fetch all available users (employees/interns)
      const usersResponse = await api.get('/users');
      const users = usersResponse.data;
      setAvailableUsers(users);
      
      // Build team member summary
      const teamMembersSummary = assignedUserIds.map(userId => {
        const userInfo = users.find(u => u.id === userId);
        const userTasks = myTeamTasks.filter(t => t.assigned_to === userId);
        const completed = userTasks.filter(t => t.status === 'completed').length;
        const pending = userTasks.filter(t => t.status === 'todo').length;
        const inProgress = userTasks.filter(t => t.status === 'in_progress').length;
        
        return {
          id: userId,
          name: userInfo?.name || 'Unknown',
          email: userInfo?.email || 'N/A',
          role: userInfo?.role || 'N/A',
          totalTasks: userTasks.length,
          completed,
          pending,
          inProgress
        };
      });
      
      setTeamMembers(teamMembersSummary);
    } catch (error) {
      console.error('Failed to fetch dashboard data', error);
      toast.error('Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/tasks', formData);
      toast.success('Task assigned successfully');
      setOpen(false);
      fetchDashboardData();
      setFormData({ title: '', description: '', assigned_to: '', priority: 'medium', deadline: '' });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create task');
    }
  };

  const getTaskStats = () => {
    const total = teamTasks.length;
    const todo = teamTasks.filter(t => t.status === 'todo').length;
    const inProgress = teamTasks.filter(t => t.status === 'in_progress').length;
    const completed = teamTasks.filter(t => t.status === 'completed').length;
    return { total, todo, inProgress, completed };
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </DashboardLayout>
    );
  }

  const taskStats = getTaskStats();

  return (
    <DashboardLayout>
      <div className="space-y-6" data-testid="team-dashboard">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-foreground" data-testid="dashboard-title">Team Lead Dashboard</h1>
            <p className="text-muted-foreground">Monitor team performance and assign tasks</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Assign Task
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Assign New Task</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Task Title</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    required
                    placeholder="Enter task title"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    placeholder="Describe the task"
                    rows={3}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="assigned_to">Assign To</Label>
                  <Select
                    value={formData.assigned_to}
                    onValueChange={(value) => setFormData({...formData, assigned_to: value})}
                    required
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select team member" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableUsers.map(u => (
                        <SelectItem key={u.id} value={u.id}>
                          {u.name} ({u.email})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="priority">Priority</Label>
                  <Select
                    value={formData.priority}
                    onValueChange={(value) => setFormData({...formData, priority: value})}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="urgent">Urgent</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="deadline">Deadline</Label>
                  <Input
                    id="deadline"
                    type="date"
                    value={formData.deadline}
                    onChange={(e) => setFormData({...formData, deadline: e.target.value})}
                  />
                </div>
                <Button type="submit" className="w-full">
                  Assign Task
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Task Stats */}
        <div className="dashboard-grid">
          <Card className="stat-card bg-card border-border" data-testid="stat-my-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">My Tasks</CardTitle>
              <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{stats?.my_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Assigned to me</p>
            </CardContent>
          </Card>

          <Card 
            className="stat-card bg-card border-border cursor-pointer hover:shadow-lg transition-shadow" 
            data-testid="stat-team-tasks"
            onClick={() => navigate('/tasks')}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">Team Tasks</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{taskStats.total}</div>
              <p className="text-xs text-muted-foreground">Created by me</p>
            </CardContent>
          </Card>

          <Card 
            className="stat-card bg-card border-border cursor-pointer hover:shadow-lg transition-shadow" 
            data-testid="stat-team-pending"
            onClick={() => {
              // Filter client-side by navigating to tasks page
              navigate('/tasks?status=todo');
            }}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">To Do</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{taskStats.todo}</div>
              <p className="text-xs text-muted-foreground">Pending tasks</p>
            </CardContent>
          </Card>

          <Card 
            className="stat-card bg-card border-border cursor-pointer hover:shadow-lg transition-shadow" 
            data-testid="stat-team-completed"
            onClick={() => navigate('/tasks?status=completed')}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">Completed</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{taskStats.completed}</div>
              <p className="text-xs text-muted-foreground">Successfully done</p>
            </CardContent>
          </Card>
        </div>

        {/* My Team Section */}
        <Card className="bg-card border-border">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2 text-card-foreground">
                <UserCheck className="h-5 w-5" />
                My Team
              </CardTitle>
              <Badge variant="outline">{teamMembers.length} members</Badge>
            </div>
          </CardHeader>
          <CardContent>
            {teamMembers.length === 0 ? (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">No team members yet</p>
                <p className="text-xs text-muted-foreground mt-1">Assign tasks to employees or interns to build your team</p>
              </div>
            ) : (
              <div className="space-y-3">
                {teamMembers.map((member) => (
                  <div key={member.id} className="flex items-center justify-between p-4 rounded-lg border border-border hover:bg-muted/50 transition-colors">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-semibold text-foreground">{member.name}</h4>
                        <Badge variant="outline" className="text-xs">
                          {member.role.replace('_', ' ').toUpperCase()}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{member.email}</p>
                    </div>
                    <div className="flex gap-4 text-sm">
                      <div className="text-center">
                        <div className="font-bold text-foreground">{member.totalTasks}</div>
                        <div className="text-xs text-muted-foreground">Total</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold text-blue-600 dark:text-blue-400">{member.inProgress}</div>
                        <div className="text-xs text-muted-foreground">Active</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold text-green-600 dark:text-green-400">{member.completed}</div>
                        <div className="text-xs text-muted-foreground">Done</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold text-gray-600 dark:text-gray-400">{member.pending}</div>
                        <div className="text-xs text-muted-foreground">Pending</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Team Tasks */}
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="text-card-foreground">Recent Team Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            {teamTasks.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No team tasks created yet</p>
            ) : (
              <div className="space-y-3">
                {teamTasks.slice(0, 5).map((task) => {
                  const assignee = availableUsers.find(u => u.id === task.assigned_to);
                  return (
                    <div key={task.id} className="flex items-center justify-between p-4 rounded-lg border border-border hover:bg-muted/50 transition-colors">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h4 className="font-medium text-foreground">{task.title}</h4>
                          <Badge className={`text-xs ${
                            task.status === 'completed' ? 'bg-green-500' :
                            task.status === 'in_progress' ? 'bg-blue-500' :
                            task.status === 'blocked' ? 'bg-red-500' : 'bg-gray-500'
                          } text-white`}>
                            {task.status.replace('_', ' ')}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            {task.priority}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground mt-1">
                          Assigned to: {assignee?.name || 'Unknown'}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-semibold text-foreground">{task.progress}%</div>
                        <div className="text-xs text-muted-foreground">Progress</div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

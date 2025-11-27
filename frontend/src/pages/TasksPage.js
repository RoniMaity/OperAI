import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import { Progress } from '../components/ui/progress';
import { Slider } from '../components/ui/slider';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';
import { Plus, Edit, Loader2 } from 'lucide-react';

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [searchParams] = useSearchParams();
  const statusFilter = searchParams.get('status');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    assigned_to: '',
    priority: 'medium',
    deadline: ''
  });

  const canCreateTask = ['admin', 'hr', 'team_lead'].includes(user?.role);

  useEffect(() => {
    fetchTasks();
    if (canCreateTask) {
      fetchUsers();
    }
  }, [statusFilter]);

  const fetchTasks = async () => {
    try {
      const params = statusFilter ? { status: statusFilter } : {};
      const response = await api.get('/tasks', { params });
      setTasks(response.data);
    } catch (error) {
      toast.error('Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await api.get('/users');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/tasks', formData);
      toast.success('Task created successfully');
      setOpen(false);
      fetchTasks();
      setFormData({ title: '', description: '', assigned_to: '', priority: 'medium', deadline: '' });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create task');
    }
  };

  const handleUpdateProgress = async (taskId, progress) => {
    try {
      await api.patch(`/tasks/${taskId}`, { progress });
      toast.success('Progress updated');
      fetchTasks();
    } catch (error) {
      toast.error('Failed to update progress');
    }
  };

  const handleUpdateStatus = async (taskId, status) => {
    try {
      await api.patch(`/tasks/${taskId}`, { status });
      toast.success('Status updated');
      fetchTasks();
    } catch (error) {
      toast.error('Failed to update status');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6" data-testid="tasks-page">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight" data-testid="tasks-title">Tasks</h1>
            <p className="text-muted-foreground">
              {statusFilter ? `Showing ${statusFilter.replace('_', ' ')} tasks` : 'Manage and track your tasks'}
            </p>
          </div>
          {canCreateTask && (
            <Dialog open={open} onOpenChange={setOpen}>
              <DialogTrigger asChild>
                <Button data-testid="create-task-btn">
                  <Plus className="mr-2 h-4 w-4" />
                  Create Task
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                  <DialogTitle>Create New Task</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="title">Task Title</Label>
                    <Input
                      id="title"
                      value={formData.title}
                      onChange={(e) => setFormData({...formData, title: e.target.value})}
                      required
                      data-testid="task-title-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="description">Description</Label>
                    <Textarea
                      id="description"
                      value={formData.description}
                      onChange={(e) => setFormData({...formData, description: e.target.value})}
                      data-testid="task-description-input"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="assigned_to">Assign To</Label>
                    <Select
                      value={formData.assigned_to}
                      onValueChange={(value) => setFormData({...formData, assigned_to: value})}
                      required
                    >
                      <SelectTrigger data-testid="task-assign-select">
                        <SelectValue placeholder="Select user" />
                      </SelectTrigger>
                      <SelectContent>
                        {users.map(u => (
                          <SelectItem key={u.id} value={u.id}>{u.name}</SelectItem>
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
                      <SelectTrigger data-testid="task-priority-select">
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
                      data-testid="task-deadline-input"
                    />
                  </div>
                  <Button type="submit" className="w-full" data-testid="task-submit-btn">
                    Create Task
                  </Button>
                </form>
              </DialogContent>
            </Dialog>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : tasks.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-muted-foreground">No tasks found</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {tasks.map((task) => (
              <Card key={task.id} data-testid={`task-card-${task.id}`}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle>{task.title}</CardTitle>
                      <div className="flex gap-2 flex-wrap">
                        <span className={`status-badge ${
                          task.status === 'completed' ? 'bg-green-500' :
                          task.status === 'in_progress' ? 'bg-blue-500' :
                          task.status === 'blocked' ? 'bg-red-500' : 'bg-gray-500'
                        } text-white`}>
                          {task.status.replace('_', ' ')}
                        </span>
                        <span className={`status-badge ${
                          task.priority === 'urgent' ? 'bg-red-100 text-red-800' :
                          task.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                          task.priority === 'medium' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {task.priority}
                        </span>
                      </div>
                    </div>
                    <Select value={task.status} onValueChange={(value) => handleUpdateStatus(task.id, value)}>
                      <SelectTrigger className="w-[140px]">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="todo">To Do</SelectItem>
                        <SelectItem value="in_progress">In Progress</SelectItem>
                        <SelectItem value="completed">Completed</SelectItem>
                        <SelectItem value="blocked">Blocked</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {task.description && <p className="text-sm text-muted-foreground">{task.description}</p>}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span>Progress: {task.progress}%</span>
                    </div>
                    <Progress value={task.progress} className="h-2" />
                    <Slider
                      value={[task.progress]}
                      onValueChange={([value]) => handleUpdateProgress(task.id, value)}
                      max={100}
                      step={10}
                      className="w-full"
                    />
                  </div>
                  {task.deadline && (
                    <p className="text-xs text-muted-foreground">
                      Deadline: {new Date(task.deadline).toLocaleDateString()}
                    </p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Progress } from '../components/ui/progress';
import api from '../services/api';
import { CheckSquare, Calendar, FileText, TrendingUp } from 'lucide-react';

export default function EmployeeDashboard() {
  const [stats, setStats] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, tasksRes, announcementsRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/tasks'),
        api.get('/announcements')
      ]);
      
      setStats(statsRes.data);
      setTasks(tasksRes.data.slice(0, 5)); // Top 5 tasks
      setAnnouncements(announcementsRes.data.slice(0, 3));
    } catch (error) {
      console.error('Failed to fetch dashboard data', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      todo: 'bg-gray-500',
      in_progress: 'bg-blue-500',
      completed: 'bg-green-500',
      blocked: 'bg-red-500'
    };
    return colors[status] || 'bg-gray-500';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      low: 'text-gray-500',
      medium: 'text-blue-500',
      high: 'text-orange-500',
      urgent: 'text-red-500'
    };
    return colors[priority] || 'text-gray-500';
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

  return (
    <DashboardLayout>
      <div className="space-y-6" data-testid="employee-dashboard">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight" data-testid="dashboard-title">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back! Here's your overview.</p>
        </div>

        {/* Stats Grid */}
        <div className="dashboard-grid">
          <Card className="stat-card" data-testid="stat-my-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">My Tasks</CardTitle>
              <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.my_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Total assigned tasks</p>
            </CardContent>
          </Card>

          <Card className="stat-card" data-testid="stat-pending-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.pending_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Tasks to do</p>
            </CardContent>
          </Card>

          <Card className="stat-card" data-testid="stat-completed-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.completed_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Tasks done</p>
            </CardContent>
          </Card>

          <Card className="stat-card" data-testid="stat-my-leaves">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Leave Requests</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.my_leaves || 0}</div>
              <p className="text-xs text-muted-foreground">Total requests</p>
            </CardContent>
          </Card>
        </div>

        {/* Recent Tasks */}
        <Card data-testid="recent-tasks-card">
          <CardHeader>
            <CardTitle>Recent Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            {tasks.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No tasks assigned yet</p>
            ) : (
              <div className="space-y-4">
                {tasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-4 rounded-lg border smooth-transition hover:bg-accent" data-testid={`task-${task.id}`}>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium">{task.title}</h4>
                        <span className={`status-badge ${getStatusColor(task.status)} text-white`}>
                          {task.status.replace('_', ' ')}
                        </span>
                        <span className={`text-xs font-medium ${getPriorityColor(task.priority)}`}>
                          {task.priority.toUpperCase()}
                        </span>
                      </div>
                      {task.description && (
                        <p className="text-sm text-muted-foreground mt-1">{task.description}</p>
                      )}
                      <div className="mt-2">
                        <div className="flex items-center gap-2 text-xs text-muted-foreground mb-1">
                          <span>Progress: {task.progress}%</span>
                        </div>
                        <Progress value={task.progress} className="h-2" />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Announcements */}
        <Card data-testid="announcements-card">
          <CardHeader>
            <CardTitle>Announcements</CardTitle>
          </CardHeader>
          <CardContent>
            {announcements.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No announcements</p>
            ) : (
              <div className="space-y-4">
                {announcements.map((announcement) => (
                  <div key={announcement.id} className="p-4 rounded-lg border" data-testid={`announcement-${announcement.id}`}>
                    <h4 className="font-medium">{announcement.title}</h4>
                    <p className="text-sm text-muted-foreground mt-1">{announcement.content}</p>
                    <p className="text-xs text-muted-foreground mt-2">
                      {new Date(announcement.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
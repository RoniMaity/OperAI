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
      setTasks(tasksRes.data.slice(0, 5));
      setAnnouncements(announcementsRes.data.slice(0, 3));
    } catch (error) {
      console.error('Failed to fetch dashboard data', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      todo: 'bg-gray-500 dark:bg-gray-600',
      in_progress: 'bg-blue-500 dark:bg-blue-600',
      completed: 'bg-green-500 dark:bg-green-600',
      blocked: 'bg-red-500 dark:bg-red-600'
    };
    return colors[status] || 'bg-gray-500';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      low: 'text-gray-500 dark:text-gray-400',
      medium: 'text-blue-500 dark:text-blue-400',
      high: 'text-orange-500 dark:text-orange-400',
      urgent: 'text-red-500 dark:text-red-400'
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
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground" data-testid="dashboard-title">Dashboard</h1>
          <p className="text-muted-foreground">Welcome back! Here's your overview.</p>
        </div>

        <div className="dashboard-grid">
          <Card className="stat-card bg-card border-border" data-testid="stat-my-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">My Tasks</CardTitle>
              <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{stats?.my_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Total assigned tasks</p>
            </CardContent>
          </Card>

          <Card className="stat-card bg-card border-border" data-testid="stat-pending-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">Pending</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{stats?.pending_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Tasks to do</p>
            </CardContent>
          </Card>

          <Card className="stat-card bg-card border-border" data-testid="stat-completed-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">Completed</CardTitle>
              <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{stats?.completed_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Tasks done</p>
            </CardContent>
          </Card>

          <Card className="stat-card bg-card border-border" data-testid="stat-my-leaves">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">Leave Requests</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{stats?.my_leaves || 0}</div>
              <p className="text-xs text-muted-foreground">Total requests</p>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-card border-border" data-testid="recent-tasks-card">
          <CardHeader>
            <CardTitle className="text-card-foreground">Recent Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            {tasks.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No tasks assigned yet</p>
            ) : (
              <div className="space-y-4">
                {tasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between p-4 rounded-lg border border-border smooth-transition hover:bg-accent" data-testid={`task-${task.id}`}>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h4 className="font-medium text-foreground">{task.title}</h4>
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

        <Card className="bg-card border-border" data-testid="announcements-card">
          <CardHeader>
            <CardTitle className="text-card-foreground">Announcements</CardTitle>
          </CardHeader>
          <CardContent>
            {announcements.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No announcements</p>
            ) : (
              <div className="space-y-4">
                {announcements.map((announcement) => (
                  <div key={announcement.id} className="p-4 rounded-lg border border-border bg-card" data-testid={`announcement-${announcement.id}`}>
                    <h4 className="font-medium text-card-foreground">{announcement.title}</h4>
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
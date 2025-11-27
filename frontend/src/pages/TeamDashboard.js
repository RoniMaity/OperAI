import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import api from '../services/api';
import { CheckSquare, TrendingUp, Clock, Users } from 'lucide-react';

export default function TeamDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/dashboard/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data', error);
    } finally {
      setLoading(false);
    }
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
      <div className="space-y-6" data-testid="team-dashboard">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground" data-testid="dashboard-title">Team Lead Dashboard</h1>
          <p className="text-muted-foreground">Monitor team performance and tasks</p>
        </div>

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
              <div className="text-2xl font-bold text-card-foreground">{stats?.team_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Created by me</p>
            </CardContent>
          </Card>

          <Card 
            className="stat-card bg-card border-border cursor-pointer hover:shadow-lg transition-shadow" 
            data-testid="stat-team-pending"
            onClick={() => navigate('/tasks?status=todo')}
          >
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-card-foreground">Pending</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-card-foreground">{stats?.team_tasks_pending || 0}</div>
              <p className="text-xs text-muted-foreground">To be completed</p>
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
              <div className="text-2xl font-bold text-card-foreground">{stats?.team_tasks_completed || 0}</div>
              <p className="text-xs text-muted-foreground">Successfully done</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}

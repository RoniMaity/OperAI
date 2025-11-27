import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import api from '../services/api';
import { CheckSquare, TrendingUp, Clock } from 'lucide-react';

export default function TeamDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

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
          <h1 className="text-3xl font-bold tracking-tight" data-testid="dashboard-title">Team Lead Dashboard</h1>
          <p className="text-muted-foreground">Monitor team performance and tasks</p>
        </div>

        <div className="dashboard-grid">
          <Card className="stat-card" data-testid="stat-total-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
              <CheckSquare className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.total_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Team tasks</p>
            </CardContent>
          </Card>

          <Card className="stat-card" data-testid="stat-pending-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.pending_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">To be completed</p>
            </CardContent>
          </Card>

          <Card className="stat-card" data-testid="stat-completed-tasks">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.completed_tasks || 0}</div>
              <p className="text-xs text-muted-foreground">Successfully done</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
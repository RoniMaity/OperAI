import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import api from '../services/api';
import { toast } from 'sonner';
import { Clock, LogIn, LogOut, Calendar } from 'lucide-react';
import { format } from 'date-fns';

export default function AttendancePage() {
  const [attendance, setAttendance] = useState([]);
  const [todayAttendance, setTodayAttendance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [workMode, setWorkMode] = useState('wfo');

  useEffect(() => {
    fetchAttendance();
  }, []);

  const fetchAttendance = async () => {
    try {
      const response = await api.get('/attendance');
      setAttendance(response.data);
      
      // Check if already checked in today
      const today = format(new Date(), 'yyyy-MM-dd');
      const todayRecord = response.data.find(a => a.date === today);
      setTodayAttendance(todayRecord || null);
    } catch (error) {
      toast.error('Failed to fetch attendance');
    } finally {
      setLoading(false);
    }
  };

  const handleCheckIn = async () => {
    try {
      await api.post('/attendance/check-in', { work_mode: workMode });
      toast.success('Checked in successfully');
      fetchAttendance();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to check in');
    }
  };

  const handleCheckOut = async () => {
    try {
      await api.post('/attendance/check-out', {});
      toast.success('Checked out successfully');
      fetchAttendance();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to check out');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6" data-testid="attendance-page">
        <div>
          <h1 className="text-3xl font-bold tracking-tight" data-testid="attendance-title">Attendance</h1>
          <p className="text-muted-foreground">Track your work hours and attendance</p>
        </div>

        {/* Check In/Out Card */}
        <Card data-testid="check-in-card">
          <CardHeader>
            <CardTitle>Today's Attendance</CardTitle>
          </CardHeader>
          <CardContent>
            {!todayAttendance ? (
              <div className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Work Mode</label>
                  <Select value={workMode} onValueChange={setWorkMode}>
                    <SelectTrigger data-testid="work-mode-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="wfo">Work From Office</SelectItem>
                      <SelectItem value="wfh">Work From Home</SelectItem>
                      <SelectItem value="hybrid">Hybrid</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button onClick={handleCheckIn} className="w-full" data-testid="check-in-btn">
                  <LogIn className="mr-2 h-4 w-4" />
                  Check In
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Check In</p>
                    <p className="text-2xl font-bold">
                      {todayAttendance.check_in ? format(new Date(todayAttendance.check_in), 'HH:mm') : 'N/A'}
                    </p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Check Out</p>
                    <p className="text-2xl font-bold">
                      {todayAttendance.check_out ? format(new Date(todayAttendance.check_out), 'HH:mm') : '-'}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <span className={`status-badge ${todayAttendance.work_mode === 'wfh' ? 'bg-blue-500' : 'bg-green-500'} text-white`}>
                    {todayAttendance.work_mode.toUpperCase()}
                  </span>
                  <span className={`status-badge ${todayAttendance.status === 'present' ? 'bg-green-500' : 'bg-blue-500'} text-white`}>
                    {todayAttendance.status.toUpperCase()}
                  </span>
                </div>
                {!todayAttendance.check_out && (
                  <Button onClick={handleCheckOut} variant="outline" className="w-full" data-testid="check-out-btn">
                    <LogOut className="mr-2 h-4 w-4" />
                    Check Out
                  </Button>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Attendance History */}
        <Card data-testid="attendance-history-card">
          <CardHeader>
            <CardTitle>Attendance History</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : attendance.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No attendance records</p>
            ) : (
              <div className="space-y-4">
                {attendance.map((record) => (
                  <div key={record.id} className="flex items-center justify-between p-4 rounded-lg border" data-testid={`attendance-record-${record.id}`}>
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                        <Calendar className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <p className="font-medium">{format(new Date(record.date), 'MMM dd, yyyy')}</p>
                        <div className="flex gap-2 mt-1">
                          <span className="text-xs text-muted-foreground">
                            In: {record.check_in ? format(new Date(record.check_in), 'HH:mm') : 'N/A'}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            Out: {record.check_out ? format(new Date(record.check_out), 'HH:mm') : '-'}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <span className={`status-badge ${record.work_mode === 'wfh' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                        {record.work_mode.toUpperCase()}
                      </span>
                      <span className={`status-badge ${record.status === 'present' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                        {record.status}
                      </span>
                    </div>
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
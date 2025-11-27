import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import api from '../services/api';
import { toast } from 'sonner';
import { format } from 'date-fns';

export default function AttendanceListPage() {
  const [attendance, setAttendance] = useState([]);
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch attendance records
      const attendanceResponse = await api.get('/attendance');
      const attendanceData = attendanceResponse.data;

      // Fetch all users
      const usersResponse = await api.get('/users');
      const usersMap = {};
      usersResponse.data.forEach(user => {
        usersMap[user.id] = user;
      });

      setAttendance(attendanceData);
      setUsers(usersMap);
    } catch (error) {
      console.error('Failed to fetch attendance', error);
      toast.error('Failed to load attendance records');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      present: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      absent: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
      half_day: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      late: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
      wfh: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
    };
    return variants[status] || variants.present;
  };

  const formatTime = (datetime) => {
    if (!datetime) return 'N/A';
    try {
      return format(new Date(datetime), 'hh:mm a');
    } catch {
      return 'N/A';
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
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Attendance Records</h1>
          <p className="text-muted-foreground">View all employee attendance</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>All Attendance ({attendance.length} records)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-4 font-medium">Employee</th>
                    <th className="text-left p-4 font-medium">Date</th>
                    <th className="text-left p-4 font-medium">Check In</th>
                    <th className="text-left p-4 font-medium">Check Out</th>
                    <th className="text-left p-4 font-medium">Work Mode</th>
                    <th className="text-left p-4 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {attendance.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="text-center p-8 text-muted-foreground">
                        No attendance records found
                      </td>
                    </tr>
                  ) : (
                    attendance.map((record) => {
                      const user = users[record.user_id];
                      return (
                        <tr key={record.id} className="border-b hover:bg-muted/50">
                          <td className="p-4">
                            <div>
                              <div className="font-medium">{user?.name || 'Unknown'}</div>
                              <div className="text-sm text-muted-foreground">{user?.email || 'N/A'}</div>
                            </div>
                          </td>
                          <td className="p-4">{record.date}</td>
                          <td className="p-4">{formatTime(record.check_in)}</td>
                          <td className="p-4">{formatTime(record.check_out)}</td>
                          <td className="p-4">
                            <Badge variant="outline">{record.work_mode.toUpperCase()}</Badge>
                          </td>
                          <td className="p-4">
                            <Badge className={getStatusBadge(record.status)}>
                              {record.status.replace('_', ' ').toUpperCase()}
                            </Badge>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

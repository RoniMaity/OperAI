import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import api from '../services/api';
import { toast } from 'sonner';
import { Check, X } from 'lucide-react';

export default function LeaveListPage() {
  const [leaves, setLeaves] = useState([]);
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const statusFilter = searchParams.get('status');

  useEffect(() => {
    fetchData();
  }, [statusFilter]);

  const fetchData = async () => {
    try {
      // Fetch leaves
      const params = statusFilter ? { status: statusFilter } : {};
      const leavesResponse = await api.get('/leave', { params });
      const leavesData = leavesResponse.data;

      // Fetch all users to get requester details
      const usersResponse = await api.get('/users');
      const usersMap = {};
      usersResponse.data.forEach(user => {
        usersMap[user.id] = user;
      });

      setLeaves(leavesData);
      setUsers(usersMap);
    } catch (error) {
      console.error('Failed to fetch leaves', error);
      toast.error('Failed to load leave requests');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (leaveId) => {
    try {
      await api.patch(`/leave/${leaveId}`, { status: 'approved' });
      toast.success('Leave request approved');
      fetchData();
    } catch (error) {
      console.error('Failed to approve leave', error);
      toast.error('Failed to approve leave request');
    }
  };

  const handleReject = async (leaveId) => {
    try {
      await api.patch(`/leave/${leaveId}`, { 
        status: 'rejected',
        rejection_reason: 'Not approved by HR'
      });
      toast.success('Leave request rejected');
      fetchData();
    } catch (error) {
      console.error('Failed to reject leave', error);
      toast.error('Failed to reject leave request');
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      approved: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      rejected: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
      cancelled: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300'
    };
    return variants[status] || variants.pending;
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
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Leave Requests</h1>
          <p className="text-muted-foreground">
            {statusFilter ? `Showing ${statusFilter} requests` : 'View and manage all leave requests'}
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>All Leave Requests ({leaves.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {leaves.length === 0 ? (
                <p className="text-center text-muted-foreground py-8">No leave requests found</p>
              ) : (
                leaves.map((leave) => {
                  const requester = users[leave.user_id];
                  return (
                    <div key={leave.id} className="border rounded-lg p-4 space-y-3">
                      <div className="flex items-start justify-between">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <h3 className="font-semibold">{requester?.name || 'Unknown User'}</h3>
                            <Badge className={getStatusBadge(leave.status)}>
                              {leave.status.toUpperCase()}
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{requester?.email || 'N/A'}</p>
                        </div>
                        {leave.status === 'pending' && (
                          <div className="flex gap-2">
                            <Button
                              size="sm"
                              variant="default"
                              className="bg-green-600 hover:bg-green-700"
                              onClick={() => handleApprove(leave.id)}
                            >
                              <Check className="h-4 w-4 mr-1" />
                              Approve
                            </Button>
                            <Button
                              size="sm"
                              variant="destructive"
                              onClick={() => handleReject(leave.id)}
                            >
                              <X className="h-4 w-4 mr-1" />
                              Reject
                            </Button>
                          </div>
                        )}
                      </div>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium">Type:</span> {leave.leave_type}
                        </div>
                        <div>
                          <span className="font-medium">Duration:</span> {leave.start_date} to {leave.end_date}
                        </div>
                      </div>
                      <div className="text-sm">
                        <span className="font-medium">Reason:</span> {leave.reason}
                      </div>
                      {leave.rejection_reason && (
                        <div className="text-sm text-red-600">
                          <span className="font-medium">Rejection Reason:</span> {leave.rejection_reason}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

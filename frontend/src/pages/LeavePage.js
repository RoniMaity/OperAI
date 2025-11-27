import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../components/ui/dialog';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { toast } from 'sonner';
import { Plus, Calendar, Clock, CheckCircle, XCircle } from 'lucide-react';
import { format } from 'date-fns';

export default function LeavePage() {
  const { user } = useAuth();
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    leave_type: 'casual',
    start_date: '',
    end_date: '',
    reason: ''
  });

  const canApprove = ['admin', 'hr', 'team_lead'].includes(user?.role);

  useEffect(() => {
    fetchLeaves();
  }, []);

  const fetchLeaves = async () => {
    try {
      const response = await api.get('/leave');
      setLeaves(response.data);
    } catch (error) {
      toast.error('Failed to fetch leave requests');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/leave', formData);
      toast.success('Leave request submitted');
      setOpen(false);
      fetchLeaves();
      setFormData({ leave_type: 'casual', start_date: '', end_date: '', reason: '' });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit leave request');
    }
  };

  const handleUpdateStatus = async (leaveId, status, rejection_reason = null) => {
    try {
      await api.patch(`/leave/${leaveId}`, { status, rejection_reason });
      toast.success(`Leave ${status}`);
      fetchLeaves();
    } catch (error) {
      toast.error('Failed to update leave status');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6" data-testid="leave-page">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight" data-testid="leave-title">Leave Requests</h1>
            <p className="text-muted-foreground">Manage your leave applications</p>
          </div>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button data-testid="apply-leave-btn">
                <Plus className="mr-2 h-4 w-4" />
                Apply Leave
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[500px]">
              <DialogHeader>
                <DialogTitle>Apply for Leave</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="leave_type">Leave Type</Label>
                  <Select
                    value={formData.leave_type}
                    onValueChange={(value) => setFormData({...formData, leave_type: value})}
                  >
                    <SelectTrigger data-testid="leave-type-select">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sick">Sick Leave</SelectItem>
                      <SelectItem value="casual">Casual Leave</SelectItem>
                      <SelectItem value="earned">Earned Leave</SelectItem>
                      <SelectItem value="unpaid">Unpaid Leave</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="start_date">Start Date</Label>
                  <Input
                    id="start_date"
                    type="date"
                    value={formData.start_date}
                    onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                    required
                    data-testid="leave-start-date-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="end_date">End Date</Label>
                  <Input
                    id="end_date"
                    type="date"
                    value={formData.end_date}
                    onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                    required
                    data-testid="leave-end-date-input"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="reason">Reason</Label>
                  <Textarea
                    id="reason"
                    value={formData.reason}
                    onChange={(e) => setFormData({...formData, reason: e.target.value})}
                    required
                    data-testid="leave-reason-input"
                  />
                </div>
                <Button type="submit" className="w-full" data-testid="leave-submit-btn">
                  Submit Leave Request
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <Card data-testid="leave-requests-card">
          <CardHeader>
            <CardTitle>All Leave Requests</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex items-center justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : leaves.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-8">No leave requests</p>
            ) : (
              <div className="space-y-4">
                {leaves.map((leave) => (
                  <div key={leave.id} className="p-4 rounded-lg border space-y-3" data-testid={`leave-card-${leave.id}`}>
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium capitalize">{leave.leave_type.replace('_', ' ')} Leave</span>
                          <span className={`status-badge ${
                            leave.status === 'approved' ? 'bg-green-500' :
                            leave.status === 'rejected' ? 'bg-red-500' :
                            leave.status === 'pending' ? 'bg-yellow-500' : 'bg-gray-500'
                          } text-white`}>
                            {leave.status}
                          </span>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Calendar className="h-4 w-4" />
                            {format(new Date(leave.start_date), 'MMM dd')} - {format(new Date(leave.end_date), 'MMM dd, yyyy')}
                          </span>
                        </div>
                      </div>
                      {canApprove && leave.status === 'pending' && (
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-green-600 hover:text-green-700"
                            onClick={() => handleUpdateStatus(leave.id, 'approved')}
                            data-testid={`approve-leave-${leave.id}`}
                          >
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Approve
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-red-600 hover:text-red-700"
                            onClick={() => handleUpdateStatus(leave.id, 'rejected', 'Not approved')}
                            data-testid={`reject-leave-${leave.id}`}
                          >
                            <XCircle className="h-4 w-4 mr-1" />
                            Reject
                          </Button>
                        </div>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground">{leave.reason}</p>
                    {leave.rejection_reason && (
                      <p className="text-sm text-red-600">Reason: {leave.rejection_reason}</p>
                    )}
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
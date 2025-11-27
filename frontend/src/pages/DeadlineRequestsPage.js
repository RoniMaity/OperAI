import { useEffect, useState } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import api from '../services/api';
import { toast } from 'sonner';
import { Check, X, Calendar, CalendarClock } from 'lucide-react';

export default function DeadlineRequestsPage() {
  const [requests, setRequests] = useState([]);
  const [tasks, setTasks] = useState({});
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);
  const [responseDialog, setResponseDialog] = useState({ open: false, request: null, action: null });
  const [responseNote, setResponseNote] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch deadline requests
      const requestsRes = await api.get('/deadline-requests', { params: { status: 'pending' } });
      const requestsData = requestsRes.data;

      // Fetch tasks to get task details
      const tasksRes = await api.get('/tasks');
      const tasksMap = {};
      tasksRes.data.forEach(task => {
        tasksMap[task.id] = task;
      });

      // Fetch users to get requester details
      const usersRes = await api.get('/users');
      const usersMap = {};
      usersRes.data.forEach(user => {
        usersMap[user.id] = user;
      });

      setRequests(requestsData);
      setTasks(tasksMap);
      setUsers(usersMap);
    } catch (error) {
      console.error('Failed to fetch data', error);
      toast.error('Failed to load deadline requests');
    } finally {
      setLoading(false);
    }
  };

  const openResponseDialog = (request, action) => {
    setResponseDialog({ open: true, request, action });
    setResponseNote('');
  };

  const handleResponse = async () => {
    try {
      await api.patch(`/deadline-requests/${responseDialog.request.id}`, {
        status: responseDialog.action,
        response_note: responseNote || undefined
      });
      
      toast.success(`Request ${responseDialog.action === 'approved' ? 'approved' : 'rejected'}`);
      setResponseDialog({ open: false, request: null, action: null });
      fetchData();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to process request');
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className=\"flex items-center justify-center h-64\">
          <div className=\"animate-spin rounded-full h-12 w-12 border-b-2 border-primary\"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className=\"space-y-6\">
        <div>
          <h1 className=\"text-3xl font-bold tracking-tight text-foreground\">Deadline Requests</h1>
          <p className=\"text-muted-foreground\">Review and approve deadline extension requests</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Pending Requests ({requests.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {requests.length === 0 ? (
              <div className=\"text-center py-12\">
                <CalendarClock className=\"h-12 w-12 text-muted-foreground mx-auto mb-3\" />
                <p className=\"text-sm text-muted-foreground\">No pending deadline requests</p>
              </div>
            ) : (
              <div className=\"space-y-4\">
                {requests.map((request) => {
                  const task = tasks[request.task_id];
                  const requester = users[request.requested_by];
                  
                  return (
                    <div key={request.id} className=\"border rounded-lg p-4 space-y-3\">
                      <div className=\"flex items-start justify-between\">
                        <div className=\"space-y-1 flex-1\">
                          <div className=\"flex items-center gap-2\">
                            <h3 className=\"font-semibold\">{task?.title || 'Unknown Task'}</h3>
                            <Badge variant=\"outline\" className=\"text-xs\">{task?.priority || 'medium'}</Badge>
                          </div>
                          <p className=\"text-sm text-muted-foreground\">
                            Requested by: {requester?.name || 'Unknown'} ({requester?.email || 'N/A'})
                          </p>
                        </div>
                        <div className=\"flex gap-2\">
                          <Button
                            size=\"sm\"
                            variant=\"default\"
                            className=\"bg-green-600 hover:bg-green-700\"
                            onClick={() => openResponseDialog(request, 'approved')}
                          >
                            <Check className=\"h-4 w-4 mr-1\" />
                            Approve
                          </Button>
                          <Button
                            size=\"sm\"
                            variant=\"destructive\"
                            onClick={() => openResponseDialog(request, 'rejected')}
                          >
                            <X className=\"h-4 w-4 mr-1\" />
                            Reject
                          </Button>
                        </div>
                      </div>
                      
                      <div className=\"grid grid-cols-2 gap-4 text-sm\">
                        <div>
                          <span className=\"font-medium\">Current Deadline:</span>{' '}
                          {task?.deadline ? new Date(task.deadline).toLocaleDateString() : 'No deadline'}
                        </div>
                        <div>
                          <span className=\"font-medium\">Requested Deadline:</span>{' '}
                          <span className=\"text-blue-600 dark:text-blue-400 font-semibold\">
                            {new Date(request.requested_new_deadline).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                      
                      <div className=\"text-sm\">
                        <span className=\"font-medium\">Reason:</span>
                        <p className=\"mt-1 text-muted-foreground\">{request.reason}</p>
                      </div>
                      
                      <div className=\"text-xs text-muted-foreground\">
                        Requested on: {new Date(request.created_at).toLocaleString()}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Response Dialog */}
        <Dialog open={responseDialog.open} onOpenChange={(open) => setResponseDialog({ open, request: null, action: null })}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {responseDialog.action === 'approved' ? 'Approve' : 'Reject'} Deadline Request
              </DialogTitle>
            </DialogHeader>
            <div className=\"space-y-4\">
              <div>
                <p className=\"text-sm\">
                  Are you sure you want to <strong>{responseDialog.action === 'approved' ? 'approve' : 'reject'}</strong> this request?
                </p>
                {responseDialog.action === 'approved' && (
                  <p className=\"text-xs text-muted-foreground mt-2\">
                    The task deadline will be automatically updated to the requested date.
                  </p>
                )}
              </div>
              
              <div className=\"space-y-2\">
                <Label htmlFor=\"response_note\">Note (optional)</Label>
                <Input
                  id=\"response_note\"
                  value={responseNote}
                  onChange={(e) => setResponseNote(e.target.value)}
                  placeholder=\"Add a note for the requester...\"
                />
              </div>
              
              <div className=\"flex gap-2 justify-end\">
                <Button variant=\"outline\" onClick={() => setResponseDialog({ open: false, request: null, action: null })}>
                  Cancel
                </Button>
                <Button
                  variant={responseDialog.action === 'approved' ? 'default' : 'destructive'}
                  onClick={handleResponse}
                >
                  {responseDialog.action === 'approved' ? 'Approve' : 'Reject'}
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </DashboardLayout>
  );
}

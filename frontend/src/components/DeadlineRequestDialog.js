import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { CalendarClock } from 'lucide-react';
import api from '../services/api';
import { toast } from 'sonner';

export default function DeadlineRequestDialog({ task, onRequest, children }) {
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    requested_new_deadline: '',
    reason: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post(`/tasks/${task.id}/deadline-requests`, formData);
      toast.success('Deadline extension request submitted');
      setOpen(false);
      setFormData({ requested_new_deadline: '', reason: '' });
      if (onRequest) onRequest();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit request');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button size=\"sm\" variant=\"outline\">
            <CalendarClock className=\"h-3 w-3 mr-1\" />
            Request Extension
          </Button>
        )}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Request Deadline Extension</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className=\"space-y-4\">
          <div>
            <p className=\"text-sm text-muted-foreground mb-2\">
              Task: <span className=\"font-medium text-foreground\">{task.title}</span>
            </p>
            <p className=\"text-xs text-muted-foreground\">
              Current deadline: {task.deadline ? new Date(task.deadline).toLocaleDateString() : 'No deadline set'}
            </p>
          </div>
          <div className=\"space-y-2\">
            <Label htmlFor=\"new_deadline\">Requested New Deadline</Label>
            <Input
              id=\"new_deadline\"
              type=\"date\"
              value={formData.requested_new_deadline}
              onChange={(e) => setFormData({...formData, requested_new_deadline: e.target.value})}
              required
              min={new Date().toISOString().split('T')[0]}
            />
          </div>
          <div className=\"space-y-2\">
            <Label htmlFor=\"reason\">Reason for Extension</Label>
            <Textarea
              id=\"reason\"
              value={formData.reason}
              onChange={(e) => setFormData({...formData, reason: e.target.value})}
              placeholder=\"Explain why you need more time...\"
              rows={4}
              required
            />
          </div>
          <div className=\"flex gap-2 justify-end\">
            <Button type=\"button\" variant=\"outline\" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type=\"submit\" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit Request'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

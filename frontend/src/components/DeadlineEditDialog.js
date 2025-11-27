import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Calendar } from 'lucide-react';
import api from '../services/api';
import { toast } from 'sonner';

export default function DeadlineEditDialog({ task, onUpdate, children }) {
  const [open, setOpen] = useState(false);
  const [newDeadline, setNewDeadline] = useState(
    task.deadline ? new Date(task.deadline).toISOString().split('T')[0] : ''
  );
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.patch(`/tasks/${task.id}`, {
        deadline: newDeadline
      });
      toast.success('Deadline updated successfully');
      setOpen(false);
      if (onUpdate) onUpdate();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update deadline');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button size="sm" variant="outline">
            <Calendar className="h-3 w-3 mr-1" />
            Edit Deadline
          </Button>
        )}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Update Task Deadline</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <p className="text-sm text-muted-foreground mb-4">
              Task: <span className="font-medium text-foreground">{task.title}</span>
            </p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="deadline">New Deadline</Label>
            <Input
              id="deadline"
              type="date"
              value={newDeadline}
              onChange={(e) => setNewDeadline(e.target.value)}
              required
            />
          </div>
          <div className="flex gap-2 justify-end">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Updating...' : 'Update Deadline'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

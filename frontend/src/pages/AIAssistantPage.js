import { useState, useRef, useEffect } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Badge } from '../components/ui/badge';
import api from '../services/api';
import { toast } from 'sonner';
import { Send, Bot, User, Zap, CheckCircle, XCircle, Activity, List } from 'lucide-react';

export default function AIAssistantPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await api.post('/ai/execute', {
        message: userMessage,
        session_id: sessionId
      });
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message || response.data.explanation,
        actions: response.data.actionsExecuted || response.data.actions || []
      }]);
    } catch (error) {
      console.error('AI error:', error);
      toast.error('Failed to process request');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I encountered an error processing your request. Please try again or rephrase your command.',
        actions: []
      }]);
    } finally {
      setLoading(false);
    }
  };

  const renderActionResult = (actionData) => {
    const result = actionData.result || actionData;
    const success = result.success;
    const action = result.action || actionData.name;
    const details = result.details;
    const error = result.error;

    return (
      <div
        className={`p-3 rounded-lg border ${
          success
            ? 'border-green-500/30 bg-green-500/5 dark:bg-green-500/10'
            : 'border-red-500/30 bg-red-500/5 dark:bg-red-500/10'
        }`}
      >
        <div className="flex items-start gap-2">
          {success ? (
            <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0 mt-0.5" />
          ) : (
            <XCircle className="h-4 w-4 text-red-500 flex-shrink-0 mt-0.5" />
          )}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-sm font-semibold text-foreground">
                {action?.replace(/_/g, ' ').toUpperCase() || 'ACTION'}
              </span>
              <Badge
                variant={success ? 'default' : 'destructive'}
                className="text-xs"
              >
                {success ? 'Executed' : 'Failed'}
              </Badge>
            </div>
            
            {details && Object.keys(details).length > 0 && (
              <div className="mt-2 space-y-1">
                {Object.entries(details).map(([key, value]) => {
                  if (key === 'tasks' || key === 'leaves') {
                    return (
                      <div key={key} className="text-xs text-muted-foreground">
                        <span className="font-medium">{key}:</span>
                        <div className="ml-2 mt-1 space-y-1">
                          {Array.isArray(value) && value.map((item, idx) => (
                            <div key={idx} className="pl-2 border-l border-border">
                              {typeof item === 'object' ? JSON.stringify(item, null, 2) : item}
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  }
                  return (
                    <div key={key} className="text-xs text-muted-foreground">
                      <span className="font-medium">{key}:</span>{' '}
                      <span className="text-foreground">
                        {typeof value === 'object' ? JSON.stringify(value) : value}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
            
            {error && (
              <div className="text-xs text-red-600 dark:text-red-400 mt-1">
                {error}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderActions = (actions) => {
    if (!actions || actions.length === 0) return null;

    return (
      <div className="mt-3 space-y-2">
        <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wide">
          <Activity className="h-3 w-3" />
          Actions Executed by OperAI
        </div>
        <div className="space-y-2">
          {actions.map((action, idx) => (
            <div key={idx}>
              {renderActionResult(action)}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <DashboardLayout>
      <div className="space-y-6" data-testid="ai-assistant-page">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground" data-testid="ai-assistant-title">
            OperAI Intelligence
          </h1>
          <p className="text-muted-foreground">Operational AI Engine — Execute workforce actions through natural language</p>
        </div>

        <Card className="h-[600px] flex flex-col bg-card border-border shadow-lg" data-testid="chat-card">
          <CardHeader className="border-b border-border bg-card">
            <CardTitle className="flex items-center gap-2 text-card-foreground">
              <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Zap className="h-4 w-4 text-primary" />
              </div>
              OperAI Intelligence
              <Badge variant="outline" className="ml-auto">Action-Capable</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto p-6 space-y-4 bg-background" data-testid="chat-messages">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center space-y-4 max-w-2xl">
                  <div className="h-16 w-16 mx-auto rounded-full bg-primary/10 flex items-center justify-center">
                    <Zap className="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <p className="text-lg font-semibold text-foreground">OperAI Intelligence System</p>
                    <p className="text-sm text-muted-foreground mt-1">AI-powered operational agent for workforce automation</p>
                  </div>
                  <div className="grid grid-cols-2 gap-3 text-sm text-left">
                    <div className="bg-muted/50 p-3 rounded-lg">
                      <p className="font-semibold text-foreground mb-2">Task Management</p>
                      <p className="text-xs text-muted-foreground">• Create & assign tasks</p>
                      <p className="text-xs text-muted-foreground">• Update task status</p>
                      <p className="text-xs text-muted-foreground">• List & filter tasks</p>
                    </div>
                    <div className="bg-muted/50 p-3 rounded-lg">
                      <p className="font-semibold text-foreground mb-2">Leave Management</p>
                      <p className="text-xs text-muted-foreground">• Apply for leave</p>
                      <p className="text-xs text-muted-foreground">• Approve/reject requests</p>
                      <p className="text-xs text-muted-foreground">• List pending leaves</p>
                    </div>
                    <div className="bg-muted/50 p-3 rounded-lg">
                      <p className="font-semibold text-foreground mb-2">Attendance</p>
                      <p className="text-xs text-muted-foreground">• Mark attendance</p>
                      <p className="text-xs text-muted-foreground">• Update work mode</p>
                      <p className="text-xs text-muted-foreground">• Track presence</p>
                    </div>
                    <div className="bg-muted/50 p-3 rounded-lg">
                      <p className="font-semibold text-foreground mb-2">Reports</p>
                      <p className="text-xs text-muted-foreground">• Team summaries</p>
                      <p className="text-xs text-muted-foreground">• Employee reports</p>
                      <p className="text-xs text-muted-foreground">• Performance data</p>
                    </div>
                  </div>
                  <p className="text-xs text-muted-foreground italic mt-3">
                    Example: "Create a task to review docs by Friday" or "Apply sick leave for tomorrow"
                  </p>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message, index) => (
                  <div key={index} className="space-y-3" data-testid={`message-${index}`}>
                    <div className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      {message.role === 'assistant' && (
                        <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                          <Bot className="h-4 w-4 text-primary" />
                        </div>
                      )}
                      <div className={`max-w-[85%] rounded-lg px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-muted text-muted-foreground'
                      }`}>
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                        {message.role === 'assistant' && renderActions(message.actions)}
                      </div>
                      {message.role === 'user' && (
                        <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                          <User className="h-4 w-4 text-primary-foreground" />
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="flex gap-3">
                    <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Bot className="h-4 w-4 text-primary" />
                    </div>
                    <div className="bg-muted rounded-lg px-4 py-3">
                      <div className="flex gap-1">
                        <div className="h-2 w-2 bg-primary/60 rounded-full animate-bounce"></div>
                        <div className="h-2 w-2 bg-primary/60 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="h-2 w-2 bg-primary/60 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </CardContent>
          <div className="border-t border-border p-4 bg-card">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Command OperAI... (e.g., 'Create task', 'Apply leave tomorrow', 'Mark attendance WFH', 'List my tasks')"
                className="min-h-[60px] resize-none bg-background border-input text-foreground placeholder:text-muted-foreground"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                data-testid="chat-input"
              />
              <Button
                type="submit"
                size="icon"
                className="h-[60px] w-[60px] bg-primary text-primary-foreground hover:bg-primary/90"
                disabled={loading || !input.trim()}
                data-testid="chat-send-btn"
              >
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </Card>
      </div>
    </DashboardLayout>
  );
}
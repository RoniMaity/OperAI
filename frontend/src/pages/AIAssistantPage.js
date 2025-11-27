import { useState, useRef, useEffect } from 'react';
import DashboardLayout from '../components/DashboardLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Badge } from '../components/ui/badge';
import api from '../services/api';
import { toast } from 'sonner';
import { Send, Bot, User, Zap, CheckCircle, XCircle, Play } from 'lucide-react';

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
        content: response.data.explanation,
        actions: response.data.actions || []
      }]);
    } catch (error) {
      console.error('AI error:', error);
      toast.error('Failed to process request');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        actions: []
      }]);
    } finally {
      setLoading(false);
    }
  };

  const renderActions = (actions) => {
    if (!actions || actions.length === 0) return null;

    return (
      <div className="mt-3 space-y-2">
        <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground">
          <Play className="h-3 w-3" />
          ACTIONS EXECUTED
        </div>
        {actions.map((action, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg border ${
              action.success
                ? 'border-green-500/30 bg-green-500/5'
                : 'border-red-500/30 bg-red-500/5'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  {action.success ? (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  ) : (
                    <XCircle className="h-4 w-4 text-red-500" />
                  )}
                  <span className="text-sm font-medium text-foreground">
                    {action.action?.replace(/_/g, ' ').toUpperCase()}
                  </span>
                  <Badge variant={action.success ? 'default' : 'destructive'} className="text-xs">
                    {action.success ? 'Success' : 'Failed'}
                  </Badge>
                </div>
                {action.details && (
                  <div className="text-xs text-muted-foreground mt-1 ml-6">
                    {Object.entries(action.details).map(([key, value]) => (
                      <div key={key}>
                        <span className="font-medium">{key}:</span> {JSON.stringify(value)}
                      </div>
                    ))}
                  </div>
                )}
                {action.error && (
                  <div className="text-xs text-red-500 mt-1 ml-6">
                    Error: {action.error}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
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
          <p className="text-muted-foreground">Your Operational AI Engine — Take actions through natural language</p>
        </div>

        <Card className="h-[600px] flex flex-col bg-card border-border" data-testid="chat-card">
          <CardHeader className="border-b border-border bg-card">
            <CardTitle className="flex items-center gap-2 text-card-foreground">
              <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Zap className="h-4 w-4 text-primary" />
              </div>
              OperAI Intelligence
              <Badge variant="outline" className="ml-auto">Action-Capable AI</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto p-6 space-y-4 bg-background" data-testid="chat-messages">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center space-y-4 max-w-lg">
                  <div className="h-16 w-16 mx-auto rounded-full bg-primary/10 flex items-center justify-center">
                    <Zap className="h-8 w-8 text-primary" />
                  </div>
                  <div>
                    <p className="text-lg font-semibold text-foreground">OperAI Intelligence System</p>
                    <p className="text-sm text-muted-foreground mt-1">AI-powered workforce operations agent</p>
                  </div>
                  <div className="text-sm text-muted-foreground space-y-2 text-left bg-muted/50 p-4 rounded-lg">
                    <p className="font-semibold text-foreground">I can execute actions for you:</p>
                    <p>• Create and manage tasks</p>
                    <p>• Apply for leave and approve requests</p>
                    <p>• Mark attendance and update work mode</p>
                    <p>• Create announcements</p>
                    <p>• Generate reports</p>
                    <p className="text-xs mt-3 italic">Just tell me what you need in natural language.</p>
                  </div>
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
                      <div className={`max-w-[80%] rounded-lg px-4 py-3 ${
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
                placeholder="Tell me what to do... (e.g., 'Create a task for me', 'Apply for leave next Monday', 'Mark my attendance as WFH')"
                className="min-h-[60px] resize-none bg-background border-input text-foreground"
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
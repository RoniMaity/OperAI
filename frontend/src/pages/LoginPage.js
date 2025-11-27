import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { toast } from 'sonner';
import { LogIn, Loader2, User, Users, Shield, Briefcase, GraduationCap } from 'lucide-react';

// Demo accounts for quick access
const DEMO_ACCOUNTS = [
  { role: 'Admin', email: 'admin@operai.demo', password: 'Password123!', icon: Shield, color: 'text-purple-600 dark:text-purple-400' },
  { role: 'HR', email: 'hr@operai.demo', password: 'Password123!', icon: Users, color: 'text-blue-600 dark:text-blue-400' },
  { role: 'Team Lead', email: 'lead@operai.demo', password: 'Password123!', icon: Briefcase, color: 'text-green-600 dark:text-green-400' },
  { role: 'Employee', email: 'emp1@operai.demo', password: 'Password123!', icon: User, color: 'text-orange-600 dark:text-orange-400' },
  { role: 'Intern', email: 'intern@operai.demo', password: 'Password123!', icon: GraduationCap, color: 'text-pink-600 dark:text-pink-400' },
];

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showDemoAccounts, setShowDemoAccounts] = useState(true);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const user = await login(email, password);
      toast.success(`Welcome back, ${user.name}!`);
      
      switch(user.role) {
        case 'admin':
        case 'hr':
          navigate('/hr-dashboard');
          break;
        case 'team_lead':
          navigate('/team-dashboard');
          break;
        case 'employee':
        case 'intern':
          navigate('/dashboard');
          break;
        default:
          navigate('/dashboard');
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (account) => {
    setEmail(account.email);
    setPassword(account.password);
    toast.info(`Demo account filled: ${account.role}`);
  };

  return (
    <div className="min-h-screen grid-pattern flex items-center justify-center p-4 bg-background transition-colors duration-300" data-testid="login-page">
      <Card className="w-full max-w-md shadow-2xl border-border bg-card">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-3xl font-bold tracking-tight text-foreground" data-testid="login-title">
            OperAI
          </CardTitle>
          <CardDescription className="text-muted-foreground" data-testid="login-description">
            Enterprise Workforce Intelligence Platform
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Demo Accounts Section */}
          {showDemoAccounts && (
            <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-950/30 border border-blue-200 dark:border-blue-800 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-blue-900 dark:text-blue-100">
                  🎯 Demo Accounts - Quick Access
                </h3>
                <button
                  onClick={() => setShowDemoAccounts(false)}
                  className="text-xs text-blue-700 dark:text-blue-300 hover:underline"
                >
                  Hide
                </button>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {DEMO_ACCOUNTS.map((account) => {
                  const Icon = account.icon;
                  return (
                    <button
                      key={account.email}
                      onClick={() => handleQuickFill(account)}
                      className="flex flex-col items-center gap-1 p-2 bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-700 rounded-md hover:bg-blue-100 dark:hover:bg-blue-900/50 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-200 group"
                      type="button"
                    >
                      <Icon className={`h-5 w-5 ${account.color} group-hover:scale-110 transition-transform`} />
                      <span className="text-xs font-medium text-gray-700 dark:text-gray-300">
                        {account.role}
                      </span>
                    </button>
                  );
                })}
              </div>
              <p className="mt-3 text-xs text-blue-700 dark:text-blue-300 text-center">
                Click any role to auto-fill credentials • Password: Password123!
              </p>
            </div>
          )}

          {!showDemoAccounts && (
            <div className="mb-4 text-center">
              <button
                onClick={() => setShowDemoAccounts(true)}
                className="text-sm text-primary hover:underline"
                type="button"
              >
                Show demo accounts
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-foreground">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="john@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                data-testid="login-email-input"
                className="h-11 bg-background border-input text-foreground"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                data-testid="login-password-input"
                className="h-11 bg-background border-input text-foreground"
              />
            </div>
            <Button
              type="submit"
              className="w-full h-11 bg-primary text-primary-foreground hover:bg-primary/90"
              disabled={loading}
              data-testid="login-submit-btn"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Signing In...
                </>
              ) : (
                <>
                  <LogIn className="mr-2 h-4 w-4" />
                  Sign In
                </>
              )}
            </Button>
          </form>
          
          <div className="mt-6 text-center text-sm">
            <span className="text-muted-foreground">Don't have an account?</span>{' '}
            <Link to="/register" className="text-primary hover:underline font-medium" data-testid="register-link">
              Register
            </Link>
          </div>
          
          <div className="mt-4 p-3 bg-muted/50 rounded-md border border-border">
            <p className="text-xs text-muted-foreground text-center">
              💡 <strong>Demo Mode:</strong> Use the quick access buttons above or see{' '}
              <a href="https://github.com/your-repo" className="text-primary hover:underline" target="_blank" rel="noopener noreferrer">
                README
              </a>{' '}
              for full account list
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
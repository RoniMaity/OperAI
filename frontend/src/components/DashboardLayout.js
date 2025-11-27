import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';
import { Avatar, AvatarFallback } from './ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';
import {
  LayoutDashboard,
  CheckSquare,
  Calendar,
  FileText,
  Users,
  Settings,
  LogOut,
  Menu,
  X,
  MessageCircle,
  Briefcase
} from 'lucide-react';

export default function DashboardLayout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getNavItems = () => {
    const baseItems = [
      { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
      { name: 'Tasks', icon: CheckSquare, path: '/tasks' },
      { name: 'Attendance', icon: Calendar, path: '/attendance' },
      { name: 'Leave', icon: FileText, path: '/leave' },
      { name: 'Announcements', icon: MessageCircle, path: '/announcements' },
      { name: 'AI Assistant', icon: Briefcase, path: '/ai-assistant' },
    ];

    if (user?.role === 'admin' || user?.role === 'hr') {
      return [
        { name: 'Dashboard', icon: LayoutDashboard, path: '/hr-dashboard' },
        { name: 'Employees', icon: Users, path: '/employees' },
        { name: 'Tasks', icon: CheckSquare, path: '/tasks' },
        { name: 'Attendance', icon: Calendar, path: '/attendance' },
        { name: 'Leave', icon: FileText, path: '/leave' },
        { name: 'Announcements', icon: MessageCircle, path: '/announcements' },
        { name: 'AI Assistant', icon: Briefcase, path: '/ai-assistant' },
      ];
    }

    if (user?.role === 'team_lead') {
      return [
        { name: 'Dashboard', icon: LayoutDashboard, path: '/team-dashboard' },
        ...baseItems.slice(1)
      ];
    }

    return baseItems;
  };

  const navItems = getNavItems();

  return (
    <div className="min-h-screen bg-background" data-testid="dashboard-layout">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-16 items-center px-4 gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            data-testid="mobile-menu-btn"
          >
            {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
          
          <div className="flex-1">
            <h1 className="text-xl font-bold tracking-tight" data-testid="dashboard-header-title">
              WorkforceOS
            </h1>
          </div>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-10 w-10 rounded-full" data-testid="user-menu-btn">
                <Avatar>
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    {user?.name?.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none" data-testid="user-menu-name">{user?.name}</p>
                  <p className="text-xs leading-none text-muted-foreground" data-testid="user-menu-email">{user?.email}</p>
                  <p className="text-xs leading-none text-muted-foreground mt-1">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary/10 text-primary">
                      {user?.role?.replace('_', ' ').toUpperCase()}
                    </span>
                  </p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => navigate('/profile')} data-testid="profile-menu-item">
                <Settings className="mr-2 h-4 w-4" />
                Profile Settings
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={handleLogout} data-testid="logout-menu-item">
                <LogOut className="mr-2 h-4 w-4" />
                Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          } fixed inset-y-0 z-40 w-64 border-r bg-background transition-transform duration-300 ease-in-out md:translate-x-0 md:static`}
          data-testid="sidebar"
        >
          <nav className="flex flex-col gap-1 p-4 pt-20 md:pt-4">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  data-testid={`nav-${item.name.toLowerCase().replace(' ', '-')}`}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors smooth-transition ${
                    isActive
                      ? 'bg-primary text-primary-foreground'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Mobile overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-background/80 backdrop-blur-sm md:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main Content */}
        <main className="flex-1 p-6" data-testid="dashboard-content">
          {children}
        </main>
      </div>
    </div>
  );
}
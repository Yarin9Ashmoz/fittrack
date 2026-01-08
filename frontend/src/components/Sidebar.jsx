import { Home, Users, Calendar, Dumbbell, CreditCard, LogOut, AlertTriangle } from 'lucide-react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // עדכן נתיב אם צריך
import './Sidebar.css';

const Sidebar = () => {
    const { logout, user } = useAuth();
    const navigate = useNavigate();

    // Role-based menu items
    const getMenuItems = () => {
        const userRole = user?.role || 'member';

        // Base items for all users
        const baseItems = [
            { icon: <Home size={22} />, label: 'Dashboard', path: '/', roles: ['member', 'trainer', 'admin'] },
        ];

        // Member-specific items
        const memberItems = [
            { icon: <Calendar size={22} />, label: 'My Classes', path: '/classes/list', roles: ['member'] },
            { icon: <Dumbbell size={22} />, label: 'My Workouts', path: '/workout-plans/list', roles: ['member'] },
            { icon: <CreditCard size={22} />, label: 'My Payments', path: '/payments/list', roles: ['member'] },
        ];

        // Trainer-specific items
        const trainerItems = [
            { icon: <Users size={22} />, label: 'My Students', path: '/users/list', roles: ['trainer'] },
            { icon: <Calendar size={22} />, label: 'My Classes', path: '/classes/list', roles: ['trainer'] },
            { icon: <CreditCard size={22} />, label: 'Payments', path: '/payments/list', roles: ['trainer'] },
        ];

        // Admin-specific items
        const adminItems = [
            { icon: <Users size={22} />, label: 'Members', path: '/users/list', roles: ['admin'] },
            { icon: <Calendar size={22} />, label: 'Schedule', path: '/classes/list', roles: ['admin'] },
            { icon: <Dumbbell size={22} />, label: 'Workouts', path: '/workout-plans/list', roles: ['admin'] },
            { icon: <CreditCard size={22} />, label: 'Payments', path: '/payments/list', roles: ['admin'] },
            { icon: <AlertTriangle size={22} />, label: 'Error Reports', path: '/error-reports', roles: ['admin'] },
        ];

        let items = [...baseItems];

        if (userRole === 'member') {
            items = [...items, ...memberItems];
        } else if (userRole === 'trainer') {
            items = [...items, ...trainerItems];
        } else if (userRole === 'admin') {
            items = [...items, ...adminItems];
        }

        return items.filter(item => item.roles.includes(userRole));
    };

    const menuItems = getMenuItems();

    const handleLogout = () => {
        logout();
        navigate('/login', { replace: true });
    };

    return (
        <aside className="sidebar glass">
            <div className="logo-container">
                <div className="logo-icon premium-gradient">
                    <Dumbbell color="white" size={24} />
                </div>
                <span className="logo-text">
                    Fit<span className="text-primary">Track</span>
                </span>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `nav-item ${isActive ? 'active' : ''}`
                        }
                    >
                        <span className="icon-wrapper">{item.icon}</span>
                        <span className="label">{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            <div className="sidebar-footer">
                <button
                    type="button"
                    className="nav-item logout-btn"
                    onClick={handleLogout}
                >
                    <span className="icon-wrapper">
                        <LogOut size={22} />
                    </span>
                    <span className="label">Logout</span>
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;

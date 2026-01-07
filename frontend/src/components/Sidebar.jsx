import { Home, Users, Calendar, Dumbbell, CreditCard, Settings, LogOut } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
    const menuItems = [
        { icon: <Home size={22} />, label: 'Dashboard', path: '/' },
        { icon: <Users size={22} />, label: 'Members', path: '/users/list' },
        { icon: <Calendar size={22} />, label: 'Schedule', path: '/classes/list' },
        { icon: <Dumbbell size={22} />, label: 'Workouts', path: '/workout-plans/list' },
        { icon: <CreditCard size={22} />, label: 'Payments', path: '/payments/list' },
    ];

    return (
        <aside className="sidebar glass">
            <div className="logo-container">
                <div className="logo-icon premium-gradient">
                    <Dumbbell color="white" size={24} />
                </div>
                <span className="logo-text">Fit<span className="text-primary">Track</span></span>
            </div>

            <nav className="sidebar-nav">
                {menuItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
                    >
                        <span className="icon-wrapper">{item.icon}</span>
                        <span className="label">{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            <div className="sidebar-footer">
                <button className="nav-item logout-btn">
                    <span className="icon-wrapper"><LogOut size={22} /></span>
                    <span className="label">Logout</span>
                </button>
            </div>
        </aside>
    );
};

export default Sidebar;

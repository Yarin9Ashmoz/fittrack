import Sidebar from './Sidebar';
import './Layout.css';

const Layout = ({ children }) => {
    return (
        <div className="layout-container">
            <Sidebar />
            <main className="main-content">
                <header className="header">
                    <div className="search-bar glass">
                        <input type="text" placeholder="Search members, classes..." />
                    </div>
                    <div className="user-profile">
                        <div className="user-info">
                            <p className="user-name">Admin User</p>
                            <p className="user-role">Gym Manager</p>
                        </div>
                        <div className="avatar premium-gradient">JS</div>
                    </div>
                </header>
                <div className="page-content">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;

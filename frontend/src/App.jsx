import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import UserCreate from './pages/users/user_create';
import UsersList from './pages/users/users_list';

function App() {
    return (
        <Router>
            <div className="app-container">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/users/create" element={<UserCreate />} />
                    <Route path="/users/list" element={<UsersList />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

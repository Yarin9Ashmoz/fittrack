import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { Users, CreditCard, Calendar, Activity } from 'lucide-react';
import axios from 'axios';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';

const API_URL = import.meta.env.VITE_API_URL


const StatCard = ({ icon, label, value, color }) => (
    <div className="stat-card glass">
        <div className={`icon-box ${color}`}>
            {icon}
        </div>
        <div className="stat-info">
            <p className="stat-label">{label}</p>
            <h3 className="stat-value">{value}</h3>
        </div>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState({
        members: 0,
        plans: 0,
        subscriptions: 0,
        classes: 0
    });

    const navigate = useNavigate();

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const [usersRes, plansRes, subsRes, classesRes] = await Promise.all([
                    axios.get(`${API_URL}/subscriptions/`),
                    axios.get(`${API_URL}/plans/`),
                    axios.get(`${API_URL}/users/`),
                    axios.get(`${API_URL}/classes/`)
                ]);

                setStats({
                    members: usersRes.data.length,
                    plans: plansRes.data.length,
                    subscriptions: subsRes.data.length,
                    classes: classesRes.data.length
                });
            } catch (error) {
                console.error("Error fetching stats:", error);
            }
        };

        fetchStats();
    }, []);

    return (
        <Layout>
            <div className="dashboard-header">
                <h1>Dashboard Overview</h1>
                <p className="text-dim">Welcome back! Here's what's happening today.</p>
            </div>

            <div className="stats-grid">
                <StatCard
                    icon={<Users size={24} />}
                    label="Total Members"
                    value={stats.members}
                    color="blue"
                />
                <StatCard
                    icon={<CreditCard size={24} />}
                    label="Active Plans"
                    value={stats.plans}
                    color="green"
                />
                <StatCard
                    icon={<Activity size={24} />}
                    label="Subscriptions"
                    value={stats.subscriptions}
                    color="purple"
                />
                <StatCard
                    icon={<Calendar size={24} />}
                    label="Today's Classes"
                    value={stats.classes}
                    color="orange"
                />
            </div>

            <div className="dashboard-grid">
                <div className="recent-activity glass">
                    <h3>Recent Members</h3>
                    <div className="activity-list">
                        <p className="text-dim">Fetching recent activity...</p>
                    </div>
                </div>
                <div className="quick-actions glass">
                    <h3>Quick Actions</h3>
                    <div className="action-buttons">
                        <button className="action-btn premium-gradient"
                            onClick={() => navigate('/users/create')}
                        >Add New Member</button>

                        <button className="action-btn glass"
                            onClick={() => navigate('/workout-plan/create')}
                        >Create Workout Plan</button>
                        <button className="action-btn glass"
                            onClick={() => navigate('/classes/create')}
                        >Schedule Class</button>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Dashboard;

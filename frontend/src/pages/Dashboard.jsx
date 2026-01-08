import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { Users, CreditCard, Calendar, Activity, AlertTriangle, Heart, Shield } from 'lucide-react';
import axios from 'axios';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { errorReportAPI } from '../services/api';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5005';

const StatCard = ({ icon, label, value, color, onClick }) => (
    <div className={`stat-card glass ${onClick ? 'clickable' : ''}`} onClick={onClick}>
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
        classes: 0,
        unresolvedErrors: 0
    });

    const navigate = useNavigate();
    const { user } = useAuth();
    const isAdmin = user?.role === 'admin';
    const isTrainer = user?.role === 'trainer';

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const token = localStorage.getItem('token');
                const headers = token ? { Authorization: `Bearer ${token}` } : {};

                const requests = [
                    axios.get(`${API_URL}/users/`, { headers }),
                    axios.get(`${API_URL}/plans/`, { headers }),
                    axios.get(`${API_URL}/subscriptions/`, { headers }),
                    axios.get(`${API_URL}/classes/`, { headers })
                ];

                if (isAdmin) {
                    requests.push(errorReportAPI.getStats());
                }

                const results = await Promise.all(requests);
                const [usersRes, plansRes, subsRes, classesRes, errorStatsRes] = results;

                setStats({
                    members: usersRes.data.length,
                    plans: plansRes.data.length,
                    subscriptions: subsRes.data.length,
                    classes: classesRes.data.length,
                    unresolvedErrors: errorStatsRes?.data?.unresolved || 0
                });
            } catch (error) {
                console.error("Dashboard: Error fetching stats:", error);
            }
        };

        fetchStats();
    }, [isAdmin]);

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
                    onClick={() => navigate('/users/list')}
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
                    onClick={() => navigate('/classes/list')}
                />
                {isAdmin && (
                    <StatCard
                        icon={<AlertTriangle size={24} />}
                        label="Unresolved Errors"
                        value={stats.unresolvedErrors}
                        color={stats.unresolvedErrors > 0 ? "red" : "green"}
                        onClick={() => navigate('/error-reports')}
                    />
                )}
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <div style={{ width: '50%' }} className="dashboard-grid">

                    <div className="recent-activity glass">
                        <h3>Quick Actions</h3>
                        <div className="action-buttons">
                            <button className="action-btn premium-gradient"
                                onClick={() => navigate('/users/create')}
                            >
                                <Users size={18} /> Add New Member
                            </button>

                            <button className="action-btn glass"
                                onClick={() => navigate('/classes/create')}
                            >
                                <Calendar size={18} /> Schedule Class
                            </button>

                            {(isAdmin || isTrainer) && (
                                <button className="action-btn glass"
                                    onClick={() => navigate('/users/list')}
                                    title="Create intake evaluation for a member"
                                >
                                    <Shield size={18} /> New Evaluation
                                </button>
                            )}

                            <button className="action-btn glass"
                                onClick={() => navigate('/workout-plan/create')}
                            >
                                <Activity size={18} /> Create Workout
                            </button>
                        </div>
                    </div>

                    {/* New Features */}
                    <div className="quick-actions glass" style={{ width: '100%' }}>
                        <h3>🆕 New Features</h3>
                        <div className="features-list">
                            {(isAdmin || isTrainer) && (
                                <div className="feature-item" onClick={() => navigate('/users/list')}>
                                    <Shield className="feature-icon" size={20} />
                                    <div>
                                        <strong>Intake Evaluations</strong>
                                        <p className="text-dim">Assess new members before training</p>
                                    </div>
                                </div>
                            )}

                            <div className="feature-item" onClick={() => {
                                const currentUserId = user?.id || 1;
                                navigate(`/personal-tracking/${currentUserId}`);
                            }}>
                                <Heart className="feature-icon" size={20} />
                                <div>
                                    <strong>Personal Tracking</strong>
                                    <p className="text-dim">Track wellness and progress</p>
                                </div>
                            </div>

                            {isAdmin && (
                                <div className="feature-item" onClick={() => navigate('/error-reports')}>
                                    <AlertTriangle className="feature-icon" size={20} />
                                    <div>
                                        <strong>Error Reports</strong>
                                        <p className="text-dim">Monitor system health</p>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </Layout>
    );
};

export default Dashboard;

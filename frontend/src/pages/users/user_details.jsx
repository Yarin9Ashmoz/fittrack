import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/Layout';
import { useAuth } from '../../context/AuthContext';
import { intakeEvaluationAPI, personalTrackingAPI } from '../../services/api';
import { Shield, Heart, CheckCircle, XCircle, Calendar } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL;

const UserDetails = () => {
    const { userId } = useParams();
    const navigate = useNavigate();
    const { user: currentUser } = useAuth();
    const [user, setUser] = useState(null);
    const [latestEvaluation, setLatestEvaluation] = useState(null);
    const [recentTracking, setRecentTracking] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('details');

    const isAdmin = currentUser?.role === 'admin';
    const isTrainer = currentUser?.role === 'trainer';
    const canCreateEvaluation = isAdmin || isTrainer;

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                setLoading(true);
                const userResponse = await axios.get(`${API_URL}/users/${userId}`);
                setUser(userResponse.data);

                // Fetch latest evaluation if user is member
                if (userResponse.data.role === 'member' && canCreateEvaluation) {
                    try {
                        const evalResponse = await intakeEvaluationAPI.getLatest(userId);
                        setLatestEvaluation(evalResponse.data);
                    } catch (err) {
                        // No evaluation found, that's ok
                        console.log('No evaluation found');
                    }

                    // Fetch recent tracking
                    try {
                        const trackingResponse = await personalTrackingAPI.getByMember(userId);
                        setRecentTracking(trackingResponse.data.slice(0, 5)); // Latest 5
                    } catch (err) {
                        console.log('No tracking found');
                    }
                }
            } catch (err) {
                setError('Error fetching user details');
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [userId, canCreateEvaluation]);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <div style={{ maxWidth: 1200, margin: '0 auto' }}>
                <div style={{ background: 'white', borderRadius: '12px', padding: '24px', marginBottom: '20px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
                    <h2 style={{ margin: '0 0 20px 0' }}>
                        {user?.first_name} {user?.last_name}
                    </h2>

                    {/* Tabs */}
                    <div style={{ borderBottom: '2px solid #e5e7eb', marginBottom: '20px' }}>
                        <div style={{ display: 'flex', gap: '20px' }}>
                            {['details', 'evaluation', 'tracking'].map(tab => (
                                <button
                                    key={tab}
                                    onClick={() => setActiveTab(tab)}
                                    style={{
                                        padding: '10px 16px',
                                        border: 'none',
                                        background: 'none',
                                        borderBottom: activeTab === tab ? '3px solid #667eea' : '3px solid transparent',
                                        color: activeTab === tab ? '#667eea' : '#64748b',
                                        fontWeight: activeTab === tab ? '600' : '400',
                                        cursor: 'pointer',
                                        textTransform: 'capitalize'
                                    }}
                                >
                                    {tab}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Tab Content */}
                    {activeTab === 'details' && user && (
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                            <div><strong>ID:</strong> {user.id}</div>
                            <div><strong>Email:</strong> {user.email}</div>
                            <div><strong>Phone:</strong> {user.phone}</div>
                            <div><strong>Address:</strong> {user.address}</div>
                            <div><strong>Role:</strong> <span style={{
                                padding: '4px 12px',
                                borderRadius: '12px',
                                background: user.role === 'admin' ? '#fee2e2' : user.role === 'trainer' ? '#dbeafe' : '#e0e7ff',
                                color: user.role === 'admin' ? '#991b1b' : user.role === 'trainer' ? '#1e40af' : '#3730a3'
                            }}>{user.role}</span></div>
                            <div><strong>Status:</strong> {user.status}</div>
                        </div>
                    )}

                    {activeTab === 'evaluation' && (
                        <div>
                            {user?.role === 'member' ? (
                                <>
                                    {latestEvaluation ? (
                                        <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                                                <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                                                    <Shield size={20} />
                                                    Latest Intake Evaluation
                                                </h3>
                                                {latestEvaluation.cleared_for_training ? (
                                                    <CheckCircle size={24} color="#10b981" />
                                                ) : (
                                                    <XCircle size={24} color="#ef4444" />
                                                )}
                                            </div>
                                            <div style={{ marginBottom: '12px' }}>
                                                <strong>Date:</strong> {new Date(latestEvaluation.evaluation_date).toLocaleDateString()}
                                            </div>
                                            <div style={{ marginBottom: '12px' }}>
                                                <strong>Cleared for Training:</strong> {latestEvaluation.cleared_for_training ? 'Yes' : 'No'}
                                            </div>
                                            {latestEvaluation.notes && (
                                                <div>
                                                    <strong>Notes:</strong>
                                                    <p style={{ marginTop: '8px', color: '#64748b' }}>{latestEvaluation.notes}</p>
                                                </div>
                                            )}
                                        </div>
                                    ) : (
                                        <div style={{ textAlign: 'center', padding: '40px' }}>
                                            <p style={{ color: '#64748b', marginBottom: '16px' }}>No intake evaluation found</p>
                                            {canCreateEvaluation && (
                                                <button
                                                    onClick={() => navigate(`/intake-evaluation/member/${userId}`)}
                                                    style={{
                                                        padding: '10px 20px',
                                                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                                        color: 'white',
                                                        border: 'none',
                                                        borderRadius: '8px',
                                                        cursor: 'pointer',
                                                        fontWeight: '600'
                                                    }}
                                                >
                                                    Create Evaluation
                                                </button>
                                            )}
                                        </div>
                                    )}
                                </>
                            ) : (
                                <p style={{ color: '#64748b' }}>Intake evaluations are only for members</p>
                            )}
                        </div>
                    )}

                    {activeTab === 'tracking' && (
                        <div>
                            {user?.role === 'member' ? (
                                <>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                                        <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                                            <Heart size={20} />
                                            Personal Tracking
                                        </h3>
                                        <button
                                            onClick={() => navigate(`/personal-tracking/${userId}`)}
                                            style={{
                                                padding: '8px 16px',
                                                background: '#667eea',
                                                color: 'white',
                                                border: 'none',
                                                borderRadius: '6px',
                                                cursor: 'pointer',
                                                fontSize: '14px'
                                            }}
                                        >
                                            View Full Dashboard
                                        </button>
                                    </div>

                                    {recentTracking.length > 0 ? (
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                            {recentTracking.map(entry => (
                                                <div key={entry.id} style={{
                                                    background: '#f8f9fa',
                                                    padding: '12px',
                                                    borderRadius: '8px',
                                                    borderLeft: '4px solid #667eea'
                                                }}>
                                                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                                        <Calendar size={16} color="#667eea" />
                                                        <strong>{new Date(entry.tracking_date).toLocaleDateString()}</strong>
                                                    </div>
                                                    {entry.emotional_regulation && (
                                                        <div style={{ fontSize: '14px', color: '#64748b' }}>
                                                            Mood: {entry.emotional_regulation.mood} | Stress: {entry.emotional_regulation.stress}
                                                        </div>
                                                    )}
                                                    {entry.physical_function && (
                                                        <div style={{ fontSize: '14px', color: '#64748b' }}>
                                                            Energy: {entry.physical_function.energy} | Sleep: {entry.physical_function.sleep_hours}h
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <p style={{ textAlign: 'center', color: '#64748b', padding: '20px' }}>
                                            No tracking entries yet
                                        </p>
                                    )}
                                </>
                            ) : (
                                <p style={{ color: '#64748b' }}>Personal tracking is only for members</p>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
};

export default UserDetails;

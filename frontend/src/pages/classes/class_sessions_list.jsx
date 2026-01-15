import React, { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './class_sessions_list.css';

const ClassSessionsList = () => {
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    const [classSessions, setClassSessions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchClassSessions = async () => {
            try {
                const response = await axios.get(`${API_URL}/classes/`);
                setClassSessions(response.data);
            } catch (err) {
                setError('Error fetching classes');
            } finally {
                setLoading(false);
            }
        };

        fetchClassSessions();
    }, []);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <div className="table-container">
                <h2 className="table-title">Classes List</h2>

                <div className="table-wrapper">
                    <table className="modern-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Class Name</th>
                                <th>Start Time</th>
                                <th>Status</th>
                                <th>Capacity</th>
                                <th>Enrolled</th>
                                <th>Waitlist</th>
                                <th>Trainer</th>
                                <th>Actions</th>
                            </tr>
                        </thead>

                        <tbody>
                            {classSessions.map(session => (
                                <tr key={session.id}>
                                    <td>{session.id}</td>
                                    <td>{session.title}</td>
                                    <td>{new Date(session.starts_at).toLocaleString()}</td>

                                    <td>
                                        <span
                                            className={`status-badge ${
                                                session.status === "open"
                                                    ? "status-active"
                                                    : session.status === "full"
                                                    ? "status-inactive"
                                                    : session.status === "closed"
                                                    ? "status-pending"
                                                    : "status-canceled"
                                            }`}
                                        >
                                            {session.status}
                                        </span>
                                    </td>

                                    <td>{session.capacity}</td>
                                    <td>{session.enrolled_count ?? 0}</td>
                                    <td>{session.waitlist_count ?? 0}</td>
                                    <td>{session.trainer_id}</td>

                                    <td className="actions-cell">
                                        <button
                                            className="action-btn view"
                                            onClick={() => navigate(`/classes/${session.id}`)}
                                        >
                                            View
                                        </button>

                                        <button
                                            className="action-btn edit"
                                            onClick={() => navigate(`/classes/${session.id}/edit`)}
                                        >
                                            Edit
                                        </button>

                                        {session.status === "open" && (
                                            <button
                                                className="action-btn enroll"
                                                onClick={() => navigate(`/enroll/${session.id}`)}
                                            >
                                                Enroll
                                            </button>
                                        )}

                                        <button
                                            className="action-btn waitlist"
                                            onClick={() => navigate(`/classes/${session.id}/waitlist`)}
                                        >
                                            Waitlist
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </Layout>
    );
};

export default ClassSessionsList;

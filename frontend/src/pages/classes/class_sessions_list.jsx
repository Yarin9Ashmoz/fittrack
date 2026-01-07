import React, { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

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
            <div style={{ maxWidth: 1100, margin: '0 auto' }}>
                <h2>Classes List</h2>

                <table className="table table-striped">
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

                                {/* Status badge */}
                                <td>
                                    {session.status === "open" && <span className="badge bg-success">Open</span>}
                                    {session.status === "full" && <span className="badge bg-danger">Full</span>}
                                    {session.status === "closed" && <span className="badge bg-secondary">Closed</span>}
                                    {session.status === "canceled" && <span className="badge bg-dark">Canceled</span>}
                                </td>

                                <td>{session.capacity}</td>
                                <td>{session.enrolled_count ?? 0}</td>
                                <td>{session.waitlist_count ?? 0}</td>
                                <td>{session.trainer_id}</td>

                                <td style={{ display: "flex", gap: "8px" }}>
                                    <button
                                        className="btn btn-primary btn-sm"
                                        onClick={() => navigate(`/classes/${session.id}`)}
                                    >
                                        View
                                    </button>

                                    <button
                                        className="btn btn-warning btn-sm"
                                        onClick={() => navigate(`/classes/${session.id}/edit`)}
                                    >
                                        Edit
                                    </button>

                                    {/* Register button */}
                                    {session.status === "open" && (
                                        <button
                                            className="btn btn-success btn-sm"
                                            onClick={() => navigate(`/enroll/${session.id}`)}
                                        >
                                            Enroll
                                        </button>
                                    )}

                                    {/* View waitlist */}
                                    <button
                                        className="btn btn-info btn-sm"
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
        </Layout>
    );
};

export default ClassSessionsList;

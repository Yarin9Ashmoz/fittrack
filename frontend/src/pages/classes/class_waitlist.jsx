import React, { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

const ClassWaitlist = () => {
    const { classId } = useParams();
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    const [waitlist, setWaitlist] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchWaitlist = async () => {
            try {
                const response = await axios.get(`${API_URL}/enrollments/class/${classId}`);
                const data = response.data.filter(e => e.status === "waitlist");
                setWaitlist(data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchWaitlist();
    }, []);

    if (loading) return <Layout><p>טוען...</p></Layout>;

    return (
        <Layout>
            <div style={{ maxWidth: 800, margin: "0 auto" }}>
                <h2>תור המתנה לשיעור #{classId}</h2>

                {waitlist.length === 0 ? (
                    <p>אין אף אחד בתור.</p>
                ) : (
                    <table className="table table-striped">
                        <thead>
                            <tr>
                                <th>מיקום</th>
                                <th>משתמש</th>
                                <th>נוצר בתאריך</th>
                            </tr>
                        </thead>
                        <tbody>
                            {waitlist.map((w) => (
                                <tr key={w.id}>
                                    <td>{w.waitlist_position}</td>
                                    <td>{w.member_id}</td>
                                    <td>{new Date(w.created_at).toLocaleString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}

                <button className="btn btn-secondary" onClick={() => navigate(-1)}>
                    חזור
                </button>
            </div>
        </Layout>
    );
};

export default ClassWaitlist;

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import Layout from "../../components/Layout";

const ClassSessionView = () => {
    const { classId } = useParams();
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    const [classData, setClassData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchClass = async () => {
            try {
                const res = await axios.get(`${API_URL}/classes/${classId}`);
                setClassData(res.data);
            } catch (err) {
                setError("Failed to load class details");
            } finally {
                setLoading(false);
            }
        };

        fetchClass();
    }, [classId]);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p className="text-danger">{error}</p></Layout>;

    return (
        <Layout>
            <div style={{ maxWidth: 700, margin: "0 auto" }}>
                <h2>{classData.title}</h2>

                <p><strong>Starts:</strong> {new Date(classData.starts_at).toLocaleString()}</p>
                <p><strong>Ends:</strong> {classData.ends_at ? new Date(classData.ends_at).toLocaleString() : "N/A"}</p>
                <p><strong>Capacity:</strong> {classData.capacity}</p>
                <p><strong>Status:</strong> {classData.status}</p>
                <p><strong>Registration Closed:</strong> {classData.is_registration_closed ? "Yes" : "No"}</p>

                <hr />

                <button
                    className="btn btn-primary"
                    onClick={() => navigate(`/enroll/${classId}`)}
                >
                    הרשם לשיעור
                </button>

                <button
                    className="btn btn-secondary ms-2"
                    onClick={() => navigate(`/classes/${classId}/waitlist`)}
                >
                    צפה בתור
                </button>

                <button
                    className="btn btn-outline-dark ms-2"
                    onClick={() => navigate(-1)}
                >
                    חזור
                </button>
            </div>
        </Layout>
    );
};

export default ClassSessionView;

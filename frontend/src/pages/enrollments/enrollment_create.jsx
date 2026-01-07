import React, { useState } from "react";
import Layout from "../../components/Layout";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

const EnrollmentCreate = () => {
    const { classId } = useParams();
    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL;

    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    const handleEnroll = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post(`${API_URL}/enrollments/`, {
                member_id: 1, // TODO: להחליף ב־auth אמיתי
                class_id: Number(classId)
            });

            const data = response.data;

            if (data.status === "waitlist") {
                setMessage(`אין מקום כרגע. נכנסת לתור במקום ${data.waitlist_position}`);
            } else if (data.status === "enrolled") {
                setMessage("נרשמת בהצלחה!");
            } else if (data.status === "promoted") {
                setMessage("קודמת מהתור! אנא אשר את ההרשמה.");
            }

        } catch (err) {
            setError("שגיאה בהרשמה");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div style={{ maxWidth: 600, margin: "0 auto" }}>
                <h2>הרשמה לשיעור #{classId}</h2>

                {message && <div className="alert alert-success">{message}</div>}
                {error && <div className="alert alert-danger">{error}</div>}

                <button
                    className="btn btn-primary"
                    onClick={handleEnroll}
                    disabled={loading}
                >
                    {loading ? "מבצע הרשמה..." : "הרשם לשיעור"}
                </button>

                <button
                    className="btn btn-secondary ms-2"
                    onClick={() => navigate(-1)}
                >
                    חזור
                </button>
            </div>
        </Layout>
    );
};

export default EnrollmentCreate;

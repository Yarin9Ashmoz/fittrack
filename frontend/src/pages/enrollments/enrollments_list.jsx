import React, { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import axios from "axios";

const EnrollmentsList = () => {
    const API_URL = import.meta.env.VITE_API_URL;

    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchEnrollments = async () => {
        try {
            const response = await axios.get(`${API_URL}/enrollments/`);
            setEnrollments(response.data);
        } catch (err) {
            console.error(err);
            setError("Error fetching enrollments");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEnrollments();
    }, []);

    const handleCancel = async (id) => {
        if (!window.confirm("לבטל את ההרשמה הזו?")) return;
        try {
            await axios.delete(`${API_URL}/enrollments/${id}`);
            await fetchEnrollments();
        } catch (err) {
            console.error(err);
            alert("שגיאה בביטול ההרשמה");
        }
    };

    if (loading) {
        return (
            <Layout>
                <p>Loading...</p>
            </Layout>
        );
    }

    if (error) {
        return (
            <Layout>
                <p>{error}</p>
            </Layout>
        );
    }

    return (
        <Layout>
            <div style={{ maxWidth: 1000, margin: "0 auto" }}>
                <h2>Enrollments List</h2>

                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Member</th>
                            <th>Class</th>
                            <th>Status</th>
                            <th>Waitlist Position</th>
                            <th>Created At</th>
                            <th>Deadline</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {enrollments.map((enr) => (
                            <tr key={enr.id}>
                                <td>{enr.id}</td>
                                <td>{enr.member_id}</td>
                                <td>{enr.class_id}</td>
                                <td>
                                    {enr.status === "enrolled" && (
                                        <span className="badge bg-success">enrolled</span>
                                    )}
                                    {enr.status === "waitlist" && (
                                        <span className="badge bg-warning text-dark">waitlist</span>
                                    )}
                                    {enr.status === "promoted" && (
                                        <span className="badge bg-info text-dark">promoted</span>
                                    )}
                                    {enr.status === "canceled" && (
                                        <span className="badge bg-secondary">canceled</span>
                                    )}
                                    {enr.status === "expired" && (
                                        <span className="badge bg-dark">expired</span>
                                    )}
                                </td>
                                <td>{enr.waitlist_position ?? "-"}</td>
                                <td>{new Date(enr.created_at).toLocaleString()}</td>
                                <td>
                                    {enr.deadline_at
                                        ? new Date(enr.deadline_at).toLocaleString()
                                        : "-"}
                                </td>
                                <td>
                                    {enr.status in ["canceled", "expired"] ? (
                                        "-"
                                    ) : (
                                        <button
                                            className="btn btn-sm btn-danger"
                                            onClick={() => handleCancel(enr.id)}
                                        >
                                            Cancel
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Layout>
    );
};

export default EnrollmentsList;

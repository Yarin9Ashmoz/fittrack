import { useState } from "react";
import axios from "axios";
import Layout from "../../../components/Layout";



const API_URL = import.meta.env.VITE_API_URL;

const WorkoutPlansCreate = () => {
    const [form, setForm] = useState({
        member_id: "",
        name: "",
        goal: "",
        status: ""
    });
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setError(null);

        try {
            await axios.post(`${API_URL}/workout-plans/`, {
                member_id: form.member_id ? parseInt(form.member_id) : null,
                name: form.name,
                goal: form.goal || null,
                status: form.status || "active",
            });
            alert("Workout plan created");
            setForm({
                member_id: "",
                name: "",
                goal: "",
                status: ""
            });
        } catch (err) {
            setError("Error creating workout plan");
        } finally {
            setSaving(false);
        }
    };

    return (
        <Layout>
            <h2>Create Workout Plan</h2>
            <form onSubmit={handleSubmit} style={{ maxWidth: 500 }}>
                {error && <p className="text-danger">{error}</p>}

                <div className="mb-2">
                    <label className="form-label">Member ID</label>
                    <input
                        type="number"
                        className="form-control"
                        name="member_id"
                        value={form.member_id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="mb-2">
                    <label className="form-label">Name</label>
                    <input
                        className="form-control"
                        name="name"
                        value={form.name}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="mb-2">
                    <label className="form-label">Goal</label>
                    <input
                        className="form-control"
                        name="goal"
                        value={form.goal}
                        onChange={handleChange}
                    />
                </div>

                <div className="mb-3">
                    <label className="form-label">Status</label>
                    <input
                        className="form-control"
                        name="status"
                        value={form.status}
                        onChange={handleChange}
                        placeholder="e.g. active, archived"
                    />
                </div>

                <button className="btn btn-primary" disabled={saving}>
                    {saving ? "Saving..." : "Create"}
                </button>
            </form>
        </Layout>
    );
};

export default WorkoutPlansCreate;

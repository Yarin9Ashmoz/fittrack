import { useState } from "react";
import axios from "axios";
import Layout from "../../../components/Layout";


const API_URL = import.meta.env.VITE_API_URL;

const WorkoutItemCreate = () => {
    const [form, setForm] = useState({
        workout_plan_id: "",
        exercise_id: "",
        sets: "",
        reps: "",
        notes: ""
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
            await axios.post(`${API_URL}/workout-items/`, {
                workout_plan_id: form.workout_plan_id ? parseInt(form.workout_plan_id) : null,
                exercise_id: form.exercise_id ? parseInt(form.exercise_id) : null,
                sets: form.sets ? parseInt(form.sets) : null,
                reps: form.reps ? parseInt(form.reps) : null,
                notes: form.notes || null,
            });
            alert("Workout item created");
            setForm({
                workout_plan_id: "",
                exercise_id: "",
                sets: "",
                reps: "",
                notes: ""
            });
        } catch (err) {
            setError("Error creating workout item");
        } finally {
            setSaving(false);
        }
    };

    return (
        <Layout>
            <h2>Create Workout Item</h2>
            <form onSubmit={handleSubmit} style={{ maxWidth: 500 }}>
                {error && <p className="text-danger">{error}</p>}

                <div className="mb-2">
                    <label className="form-label">Workout plan ID</label>
                    <input
                        type="number"
                        className="form-control"
                        name="workout_plan_id"
                        value={form.workout_plan_id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="mb-2">
                    <label className="form-label">Exercise ID</label>
                    <input
                        type="number"
                        className="form-control"
                        name="exercise_id"
                        value={form.exercise_id}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="mb-2">
                    <label className="form-label">Sets</label>
                    <input
                        type="number"
                        className="form-control"
                        name="sets"
                        value={form.sets}
                        onChange={handleChange}
                    />
                </div>

                <div className="mb-2">
                    <label className="form-label">Reps</label>
                    <input
                        type="number"
                        className="form-control"
                        name="reps"
                        value={form.reps}
                        onChange={handleChange}
                    />
                </div>

                <div className="mb-3">
                    <label className="form-label">Notes</label>
                    <textarea
                        className="form-control"
                        name="notes"
                        value={form.notes}
                        onChange={handleChange}
                    />
                </div>

                <button className="btn btn-primary" disabled={saving}>
                    {saving ? "Saving..." : "Create"}
                </button>
            </form>
        </Layout>
    );
};

export default WorkoutItemCreate;

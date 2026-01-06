import { useState } from "react";
import axios from "axios";
import Layout from "../../components/Layout";

const API_URL = import.meta.env.VITE_API_URL;

const PlanCreate = () => {
    const [form, setForm] = useState({
        name: "",
        type: "",
        price: "",
        valid_days: "",
        max_entries: ""
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
            await axios.post(`${API_URL}/plans`, {
                name: form.name,
                type: form.type,
                price: form.price ? parseFloat(form.price) : 0,
                valid_days: form.valid_days ? parseInt(form.valid_days) : null,
                max_entries: form.max_entries ? parseInt(form.max_entries) : null,
            });
            alert("Plan created successfully");
            setForm({
                name: "",
                type: "",
                price: "",
                valid_days: "",
                max_entries: ""
            });
        } catch (err) {
            setError("Error creating plan");
        } finally {
            setSaving(false);
        }
    };

    return (
        <Layout>
            <h2>Create Plan</h2>
            <form onSubmit={handleSubmit} style={{ maxWidth: 500 }}>
                {error && <p className="text-danger">{error}</p>}
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
                    <label className="form-label">Type</label>
                    <input
                        className="form-control"
                        name="type"
                        value={form.type}
                        onChange={handleChange}
                        placeholder="e.g. monthly, entries"
                        required
                    />
                </div>
                <div className="mb-2">
                    <label className="form-label">Price</label>
                    <input
                        type="number"
                        step="0.01"
                        className="form-control"
                        name="price"
                        value={form.price}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-2">
                    <label className="form-label">Valid days (optional)</label>
                    <input
                        type="number"
                        className="form-control"
                        name="valid_days"
                        value={form.valid_days}
                        onChange={handleChange}
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Max entries (optional)</label>
                    <input
                        type="number"
                        className="form-control"
                        name="max_entries"
                        value={form.max_entries}
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

export default PlanCreate;

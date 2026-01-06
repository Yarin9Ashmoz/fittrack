import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/Layout';
const API_URL = import.meta.env.VITE_API_URL

const UserCreate = () => {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        address: '',
        role: 'member',
        status: 'active'
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((f) => ({ ...f, [name]: value }));
    };

    const validate = () => {
        const e = {};
        if (!form.first_name) e.first_name = 'First name is required';
        if (!form.last_name) e.last_name = 'Last name is required';
        if (!form.email) e.email = 'Email is required';
        else {
            const re = /^\S+@\S+\.\S+$/;
            if (!re.test(form.email)) e.email = 'Invalid email address';
        }
        if (!form.phone) e.phone = 'Phone is required';
        return e;
    };

    const handleSubmit = async (ev) => {
        ev.preventDefault();
        const v = validate();
        if (Object.keys(v).length) {
            setErrors(v);
            return;
        }

        try {
            setLoading(true);
            await axios.post(`${API_URL}/users/`, form);
            navigate('/');
        } catch (err) {
            const msg = err.response?.data || err.message || 'Unknown error';
            setErrors({ submit: typeof msg === 'string' ? msg : JSON.stringify(msg) });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <div style={{ maxWidth: 720, margin: '0 auto' }}>
                <h2>Add New Member</h2>
                <form onSubmit={handleSubmit} className="glass" style={{ padding: 20 }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12}}>
                        <div>
                            <label>First Name</label>
                            <input name="first_name" value={form.first_name} onChange={handleChange} />
                            {errors.first_name && <div className="text-error">{errors.first_name}</div>}
                        </div>

                        <div>
                            <label>Last Name</label>
                            <input name="last_name" value={form.last_name} onChange={handleChange} />
                            {errors.last_name && <div className="text-error">{errors.last_name}</div>}
                        </div>

                        <div>
                            <label>Email</label>
                            <input name="email" value={form.email} onChange={handleChange} />
                            {errors.email && <div className="text-error">{errors.email}</div>}
                        </div>

                        <div>
                            <label>Phone</label>
                            <input name="phone" value={form.phone} onChange={handleChange} />
                            {errors.phone && <div className="text-error">{errors.phone}</div>}
                        </div>

                        <div style={{ gridColumn: '1 / -1' }}>
                            <label>Address</label>
                            <input name="address" value={form.address} onChange={handleChange} />
                        </div>

                        <div>
                            <label>Role</label>
                            <select name="role" value={form.role} onChange={handleChange}>
                                <option value="member">Member</option>
                                <option value="coach">Coach</option>
                                <option value="admin">Admin</option>
                            </select>
                        </div>

                        <div>
                            <label>Status</label>
                            <select name="status" value={form.status} onChange={handleChange}>
                                <option value="active">Active</option>
                                <option value="inactive">Inactive</option>
                            </select>
                        </div>
                    </div>

                    {errors.submit && <div className="text-error" style={{ marginTop: 12 }}>{errors.submit}</div>}

                    <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
                        <button type="submit" disabled={loading} className="action-btn premium-gradient">
                            {loading ? 'Saving...' : 'Create Member'}
                        </button>
                        <button type="button" onClick={() => navigate(-1)} className="action-btn glass">Cancel</button>
                    </div>
                </form>
            </div>
        </Layout>
    );
};

export default UserCreate;

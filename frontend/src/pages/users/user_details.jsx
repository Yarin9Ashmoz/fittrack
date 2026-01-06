import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/Layout';

const API_URL = import.meta.env.VITE_API_URL;

const UserDetails = () => {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get(`${API_URL}/users/${userId}`);
                setUser(response.data);
            } catch (err) {
                setError('Error fetching user details');
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [userId]);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <div style={{ maxWidth: 600, margin: '0 auto' }}>
                <h2>User Details</h2>
                {user ? (
                    <div>
                        <p><strong>ID:</strong> {user.id}</p>
                        <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>Phone:</strong> {user.phone}</p>
                        <p><strong>Address:</strong> {user.address}</p>
                        <p><strong>Role:</strong> {user.role}</p>
                        <p><strong>Status:</strong> {user.status}</p>
                    </div>
                ) : (
                    <p>User not found.</p>
                )}
            </div>
        </Layout>
    );
};

export default UserDetails;

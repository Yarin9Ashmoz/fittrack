import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Layout from '../../components/Layout';
const API_URL = import.meta.env.VITE_API_URL

const UsersList = () => {
    const navigate = useNavigate();
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get(`${API_URL}/users/`);
                setUsers(response.data);
            } catch (err) {
                setError('Error fetching users');
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, []);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <div style={{ maxWidth: 1000, margin: '0 auto' }}>
                <h2>Users List</h2>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th >ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Role</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user.id}>
                                <td>{user.id}</td>
                                <td>{user.first_name} {user.last_name}</td>
                                <td>{user.email}</td>
                                <td>{user.phone}</td>
                                <td>{user.role}</td>
                                <td>{user.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Layout>
    );
};

export default UsersList;

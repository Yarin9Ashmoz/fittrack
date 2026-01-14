import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Layout from "../../components/Layout";

const API_URL = import.meta.env.VITE_API_URL;

const SubscriptionsList = () => {
    const [subscriptions, setSubscriptions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSubscriptions = async () => {
            try {
                const response = await axios.get(`${API_URL}/subscriptions/`);
                setSubscriptions(response.data);
            } catch (err) {
                setError("Error loading subscriptions");
            } finally {
                setLoading(false);
            }
        };

        fetchSubscriptions();
    }, []);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <h2>Subscriptions List</h2>
            {subscriptions.length === 0 ? (
                <p>No subscriptions found.</p>
            ) : (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>User ID</th>
                            <th>Plan ID</th>
                            <th>Start date</th>
                            <th>End date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {subscriptions.map(sub => (
                            <tr key={sub.id}>
                                <td>{sub.id}</td>
                                <td>{sub.user_id}</td>
                                <td>{sub.plan_id}</td>
                                <td>{sub.start_date}</td>
                                <td>{sub.end_date}</td>
                                <td>{sub.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </Layout>
    );
};

export default SubscriptionsList;

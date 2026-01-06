import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../../components/Layout";

const API_URL = import.meta.env.VITE_API_URL;

const PlanList = () => {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPlans = async () => {
            try {
                const res = await axios.get(`${API_URL}/plans`);
                setPlans(res.data);
            } catch (err) {
                setError("Error loading plans");
            } finally {
                setLoading(false);
            }
        };

        fetchPlans();
    }, []);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <h2>Plans List</h2>
            {plans.length === 0 ? (
                <p>No plans found.</p>
            ) : (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Type</th>
                            <th>Price</th>
                            <th>Valid days</th>
                            <th>Max entries</th>
                        </tr>
                    </thead>
                    <tbody>
                        {plans.map(plan => (
                            <tr key={plan.id}>
                                <td>{plan.id}</td>
                                <td>{plan.name}</td>
                                <td>{plan.type}</td>
                                <td>{plan.price}</td>
                                <td>{plan.valid_days}</td>
                                <td>{plan.max_entries}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </Layout>
    );
};

export default PlanList;

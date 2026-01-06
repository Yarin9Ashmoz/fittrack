import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../../../components/Layout";


const API_URL = import.meta.env.VITE_API_URL;

const WorkoutPlansList = () => {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPlans = async () => {
            try {
                const res = await axios.get(`${API_URL}/workout-plans/`);
                setPlans(res.data);
            } catch (err) {
                setError("Error loading workout plans");
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
            <h2>Workout Plans List</h2>
            {plans.length === 0 ? (
                <p>No workout plans found.</p>
            ) : (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Member ID</th>
                            <th>Name</th>
                            <th>Goal</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {plans.map(plan => (
                            <tr key={plan.id}>
                                <td>{plan.id}</td>
                                <td>{plan.member_id}</td>
                                <td>{plan.name}</td>
                                <td>{plan.goal}</td>
                                <td>{plan.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </Layout>
    );
};

export default WorkoutPlansList;

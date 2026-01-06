import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../../../components/Layout";


const API_URL = import.meta.env.VITE_API_URL;

const WorkoutItemList = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchItems = async () => {
            try {
                const res = await axios.get(`${API_URL}/workout-items/`);
                setItems(res.data);
            } catch (err) {
                setError("Error loading workout items");
            } finally {
                setLoading(false);
            }
        };

        fetchItems();
    }, []);

    if (loading) return <Layout><p>Loading...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <h2>Workout Items List</h2>
            {items.length === 0 ? (
                <p>No workout items found.</p>
            ) : (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Workout plan ID</th>
                            <th>Exercise ID</th>
                            <th>Sets</th>
                            <th>Reps</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map(item => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.workout_plan_id}</td>
                                <td>{item.exercise_id}</td>
                                <td>{item.sets}</td>
                                <td>{item.reps}</td>
                                <td>{item.notes}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </Layout>
    );
};

export default WorkoutItemList;

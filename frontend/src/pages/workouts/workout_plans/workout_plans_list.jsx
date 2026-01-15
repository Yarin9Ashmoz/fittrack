import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../../../components/Layout";
import "./workout_plans.css";

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

  if (loading)
    return (
      <Layout>
        <p>Loading...</p>
      </Layout>
    );
  if (error)
    return (
      <Layout>
        <p>{error}</p>
      </Layout>
    );

  return (
    <Layout>
      <div className="table-container">
        <h2 className="table-title">Workout Plans</h2>

        {plans.length === 0 ? (
          <p className="no-data">No workout plans found.</p>
        ) : (
          <div className="table-wrapper">
            <table className="modern-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Member ID</th>
                  <th>Title</th>
                  <th>Created At</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {plans.map((plan) => (
                  <tr key={plan.id}>
                    <td>{plan.id}</td>
                    <td>{plan.member_id}</td>
                    <td>{plan.title}</td>
                    <td>{plan.created_at}</td>

                    <td>
                      <span
                        className={`status-badge ${
                          plan.is_active ? "status-active" : "status-inactive"
                        }`}
                      >
                        {plan.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default WorkoutPlansList;

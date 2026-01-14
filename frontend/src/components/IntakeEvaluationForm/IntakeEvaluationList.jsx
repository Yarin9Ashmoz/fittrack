import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Layout from "../../components/Layout";
const API_URL = import.meta.env.VITE_API_URL;

const IntakeEvaluationList = () => {
  const navigate = useNavigate();
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

useEffect(() => {
    const fetchEvaluations = async () => {
        try {
            const token = localStorage.getItem("token");

            const response = await axios.get(
                `${API_URL}/intake-evaluations/`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setEvaluations(response.data);
        } catch (err) {
            console.error(err);
            setError("Error loading intake evaluations");
        } finally {
            setLoading(false);
        }
    };

    fetchEvaluations();
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
      <h2>Intake Evaluations</h2>
      {evaluations.length === 0 ? (
        <p>No intake evaluations found.</p>
      ) : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Member ID</th>
              <th>Date</th>
              <th>Trainer ID</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {evaluations.map((ev) => (
              <tr
                key={ev.id}
                onClick={() =>
                  navigate(`/intake-evaluation/member/${ev.member_id}`)
                }
                style={{ cursor: "pointer" }}
              >
                <td>{ev.id}</td>
                <td>{ev.member_id}</td>
                <td>{new Date(ev.date).toLocaleDateString()}</td>
                <td>{ev.evaluated_by_id}</td>
                <td>{ev.notes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
};

export default IntakeEvaluationList;

import { useState, useEffect } from "react";
import Layout from "../../components/Layout";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5005";

const CheckinsList = () => {
  const [checkins, setCheckins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchToday = async () => {
      try {
        const response = await axios.get(`${API_URL}/checkins/today`);
        setCheckins(response.data);
      } catch (err) {
        console.error("Error fetching today's check-ins", err);
        setError("Error fetching today's check-ins");
      } finally {
        setLoading(false);
      }
    };

    fetchToday();
  }, []);

  if (loading)
    return (
      <Layout>
        <p>Loading today's check-ins...</p>
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
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        <h1>Today's Check-ins</h1>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Member</th>
              <th>Subscription</th>
              <th>Class</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {checkins.map((c) => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.member_name || `${c.member_id}`}</td>
                <td>{c.subscription_id}</td>
                <td>{c.class_id ?? "-"}</td>
                <td>{new Date(c.timestamp).toLocaleString()}</td>
              </tr>
            ))}
            {checkins.length === 0 && (
              <tr>
                <td colSpan={5} className="text-center">
                  No check-ins today
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Layout>
  );
};

export default CheckinsList;

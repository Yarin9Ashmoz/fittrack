import React from 'react';
import Layout from '../../components/Layout';

const ClassSessionCreate = () => {

    const navigate = useNavigate();
    const API_URL = import.meta.env.VITE_API_URL
    const [classSession, setClassSession] = useState({
        class_name: '',
        trainer: '',
        start_time: '',
        end_time: '',
        capacity: '',
        current_members: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setClassSession({
            ...classSession,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post(`${API_URL}/classes/`, classSession);
            navigate(`/classes/${response.data.id}`);
        } catch (err) {
            setError('Error creating class session');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Layout>
            <h1>Schedule New Class</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="title">Class Name</label>
                    <input type="text" className="form-control" id="title" name="title" value={classSession.title} onChange={handleInputChange} />
                </div>

                <div className="form-group">
                    <label htmlFor="starts_at">Start Time</label>
                    <input type="datetime-local" className="form-control" id="starts_at" name="starts_at" value={classSession.starts_at} onChange={handleInputChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="capacity">Capacity</label>
                    <input type="number" className="form-control" id="capacity" name="capacity" value={classSession.capacity} onChange={handleInputChange} />
                </div>
                <div className="form-group">
                    <label htmlFor="current_members">Current Members</label>
                    <input type="number" className="form-control" id="current_members" name="current_members" value={classSession.current_members} onChange={handleInputChange} />
                </div>
                <button type="submit" className="btn btn-primary">Schedule Class</button>
            </form>
        </Layout>
    );
};

export default ClassSessionCreate;

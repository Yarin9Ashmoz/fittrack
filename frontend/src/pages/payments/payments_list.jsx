import { useState, useEffect } from 'react';
import Layout from '../../components/Layout';
import axios from 'axios';
import './payments.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5005';

const PaymentsList = () => {
    const [payments, setPayments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPayments = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`${API_URL}/payments/`, {
                    headers: token ? { Authorization: `Bearer ${token}` } : {}
                });
                setPayments(response.data);
            } catch (err) {
                setError('Failed to load payments');
            } finally {
                setLoading(false);
            }
        };

        fetchPayments();
    }, []);

    if (loading) return <Layout><p>Loading payments...</p></Layout>;
    if (error) return <Layout><p>{error}</p></Layout>;

    return (
        <Layout>
            <div className="payments-container table table-striped">
                <h1 className="payments-title">Payments Management</h1>

                {payments.length === 0 ? (
                    <p className="no-payments">No payments found</p>
                ) : (
                    <div className="payments-table-wrapper">
                        <table className="payments-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Amount</th>
                                    <th>Method</th>
                                    <th>Status</th>
                                    <th>Reference</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                {payments.map(payment => (
                                    <tr key={payment.id}>
                                        <td>{payment.id}</td>
                                        <td>₪{payment.amount}</td>
                                        <td>{payment.payment_method || 'N/A'}</td>
                                        <td>
                                            <span className={`status-badge status-${payment.status}`}>
                                                {payment.status}
                                            </span>
                                        </td>
                                        <td>{payment.reference || '-'}</td>
                                        <td>
                                            {payment.paid_at
                                                ? new Date(payment.paid_at).toLocaleDateString()
                                                : '-'}
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

export default PaymentsList;

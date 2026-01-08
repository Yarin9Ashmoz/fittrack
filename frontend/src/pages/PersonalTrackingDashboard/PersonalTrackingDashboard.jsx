import React, { useState, useEffect } from 'react';
import { personalTrackingAPI } from '../../services/api';
import { useParams } from 'react-router-dom';
import './PersonalTrackingDashboard.css';

const PersonalTrackingDashboard = () => {
    const { memberId } = useParams();
    const [trackingData, setTrackingData] = useState([]);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [days, setDays] = useState(30);

    useEffect(() => {
        loadData();
    }, [memberId, days]);

    const loadData = async () => {
        try {
            setLoading(true);
            const [dataRes, summaryRes] = await Promise.all([
                personalTrackingAPI.getByMember(memberId),
                personalTrackingAPI.getSummary(memberId, days),
            ]);
            setTrackingData(dataRes.data);
            setSummary(summaryRes.data);
        } catch (error) {
            console.error('Failed to load tracking data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Loading...</div>;

    return (
        <div className="personal-tracking-dashboard">
            <div className="dashboard-header">
                <h2>Personal Tracking Dashboard</h2>
                <div className="period-selector">
                    <label>Period: </label>
                    <select value={days} onChange={(e) => setDays(Number(e.target.value))}>
                        <option value={7}>Last 7 days</option>
                        <option value={30}>Last 30 days</option>
                        <option value={90}>Last 90 days</option>
                    </select>
                </div>
            </div>

            {/* Summary Cards */}
            {summary && (
                <div className="summary-cards">
                    <div className="summary-card">
                        <h3>Total Entries</h3>
                        <div className="stat-value">{summary.total_entries}</div>
                    </div>
                    <div className="summary-card">
                        <h3>Period</h3>
                        <div className="stat-value">{summary.period_days} days</div>
                    </div>
                </div>
            )}

            {/* Tracking Entries */}
            <div className="tracking-entries">
                <h3>Recent Entries</h3>
                {trackingData.length === 0 ? (
                    <p>No tracking data available</p>
                ) : (
                    <div className="entries-list">
                        {trackingData.map((entry) => (
                            <div key={entry.id} className="entry-card">
                                <div className="entry-date">
                                    {new Date(entry.tracking_date).toLocaleDateString()}
                                </div>

                                <div className="entry-content">
                                    {entry.emotional_regulation && (
                                        <div className="entry-section">
                                            <strong>Emotional:</strong> Mood: {entry.emotional_regulation.mood},
                                            Stress: {entry.emotional_regulation.stress}
                                        </div>
                                    )}

                                    {entry.physical_function && (
                                        <div className="entry-section">
                                            <strong>Physical:</strong> Energy: {entry.physical_function.energy},
                                            Sleep: {entry.physical_function.sleep_hours}h
                                        </div>
                                    )}

                                    {entry.notes && (
                                        <div className="entry-notes">
                                            <strong>Notes:</strong> {entry.notes}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PersonalTrackingDashboard;

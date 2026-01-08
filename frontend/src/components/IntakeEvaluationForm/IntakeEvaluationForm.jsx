import React, { useState } from 'react';
import { intakeEvaluationAPI } from '../../services/api';
import './IntakeEvaluationForm.css';

const IntakeEvaluationForm = ({ memberId, onSuccess }) => {
    const [formData, setFormData] = useState({
        member_id: memberId,
        mental_status: { mood: '', anxiety: '', depression: '' },
        cognitive_function: { memory: 5, focus: 5, processing: 5 },
        physical_limitations: { injuries: '', mobility: '', pain_level: 0 },
        cleared_for_training: false,
        notes: '',
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            // Get current user ID from context or token
            const userData = JSON.parse(localStorage.getItem('user'));
            const dataToSubmit = {
                ...formData,
                evaluated_by_id: userData.id,
            };

            await intakeEvaluationAPI.create(dataToSubmit);
            alert('Intake evaluation created successfully!');
            if (onSuccess) onSuccess();
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to create evaluation');
        } finally {
            setLoading(false);
        }
    };

    const updateMentalStatus = (field, value) => {
        setFormData(prev => ({
            ...prev,
            mental_status: { ...prev.mental_status, [field]: value },
        }));
    };

    const updateCognitiveFunction = (field, value) => {
        setFormData(prev => ({
            ...prev,
            cognitive_function: { ...prev.cognitive_function, [field]: parseInt(value) },
        }));
    };

    const updatePhysicalLimitations = (field, value) => {
        setFormData(prev => ({
            ...prev,
            physical_limitations: { ...prev.physical_limitations, [field]: value },
        }));
    };

    return (
        <div className="intake-evaluation-form">
            <h2>Intake Evaluation</h2>
            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={handleSubmit}>
                {/* Mental Status */}
                <div className="form-section">
                    <h3>Mental Status</h3>
                    <div className="form-group">
                        <label>Mood</label>
                        <select
                            value={formData.mental_status.mood}
                            onChange={(e) => updateMentalStatus('mood', e.target.value)}
                            className="form-control"
                        >
                            <option value="">Select</option>
                            <option value="excellent">Excellent</option>
                            <option value="good">Good</option>
                            <option value="fair">Fair</option>
                            <option value="poor">Poor</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Anxiety Level</label>
                        <select
                            value={formData.mental_status.anxiety}
                            onChange={(e) => updateMentalStatus('anxiety', e.target.value)}
                            className="form-control"
                        >
                            <option value="">Select</option>
                            <option value="none">None</option>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>
                </div>

                {/* Cognitive Function */}
                <div className="form-section">
                    <h3>Cognitive Function</h3>
                    <div className="form-group">
                        <label>Memory (1-10): {formData.cognitive_function.memory}</label>
                        <input
                            type="range"
                            min="1"
                            max="10"
                            value={formData.cognitive_function.memory}
                            onChange={(e) => updateCognitiveFunction('memory', e.target.value)}
                            className="form-range"
                        />
                    </div>

                    <div className="form-group">
                        <label>Focus (1-10): {formData.cognitive_function.focus}</label>
                        <input
                            type="range"
                            min="1"
                            max="10"
                            value={formData.cognitive_function.focus}
                            onChange={(e) => updateCognitiveFunction('focus', e.target.value)}
                            className="form-range"
                        />
                    </div>
                </div>

                {/* Physical Limitations */}
                <div className="form-section">
                    <h3>Physical Limitations</h3>
                    <div className="form-group">
                        <label>Injuries/Conditions</label>
                        <textarea
                            value={formData.physical_limitations.injuries}
                            onChange={(e) => updatePhysicalLimitations('injuries', e.target.value)}
                            className="form-control"
                            rows="3"
                            placeholder="List any injuries or medical conditions..."
                        />
                    </div>

                    <div className="form-group">
                        <label>Pain Level (0-10): {formData.physical_limitations.pain_level}</label>
                        <input
                            type="range"
                            min="0"
                            max="10"
                            value={formData.physical_limitations.pain_level}
                            onChange={(e) => updatePhysicalLimitations('pain_level', parseInt(e.target.value))}
                            className="form-range"
                        />
                    </div>
                </div>

                {/* Notes and Clearance */}
                <div className="form-section">
                    <div className="form-group">
                        <label>Additional Notes</label>
                        <textarea
                            value={formData.notes}
                            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                            className="form-control"
                            rows="4"
                            placeholder="Any additional observations..."
                        />
                    </div>

                    <div className="form-check">
                        <input
                            type="checkbox"
                            checked={formData.cleared_for_training}
                            onChange={(e) => setFormData({ ...formData, cleared_for_training: e.target.checked })}
                            className="form-check-input"
                            id="clearanceCheck"
                        />
                        <label className="form-check-label" htmlFor="clearanceCheck">
                            Clear member for training
                        </label>
                    </div>
                </div>

                <div className="form-actions">
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {loading ? 'Saving...' : 'Save Evaluation'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default IntakeEvaluationForm;

import React, { useState, useEffect } from "react";
import { errorReportAPI } from "../../services/api";
import Layout from "../../components/Layout";
import "./ErrorReportDashboard.css";

const ErrorReportDashboard = () => {
  const [errors, setErrors] = useState([]);
  const [stats, setStats] = useState(null);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [filter]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [statsRes, errorsRes] = await Promise.all([
        errorReportAPI.getStats(),
        filter === "unresolved"
          ? errorReportAPI.getUnresolved()
          : errorReportAPI.getAll(),
      ]);

      setStats(statsRes.data);
      setErrors(errorsRes.data);
    } catch (error) {
      console.error("Failed to load error data:", error);
      alert("Failed to load error reports. Admin access required.");
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (errorId, newStatus) => {
    try {
      await errorReportAPI.updateStatus(errorId, { status: newStatus });
      alert("Error status updated successfully");
      loadData();
    } catch (error) {
      console.error("Failed to update status:", error);
      alert("Failed to update error status");
    }
  };

  const getSeverityClass = (severity) => {
    const classes = {
      low: "severity-low",
      medium: "severity-medium",
      high: "severity-high",
      critical: "severity-critical",
    };
    return classes[severity] || "";
  };

  const getStatusClass = (status) => {
    const classes = {
      new: "status-new",
      investigating: "status-investigating",
      resolved: "status-resolved",
      ignored: "status-ignored",
    };
    return classes[status] || "";
  };

  if (loading) return <div className="loading">Loading error reports...</div>;

  return (
    <Layout>
      <div className="error-report-dashboard">
        <div className="dashboard-header">
          <h2>🛡️ Error Reports Dashboard</h2>
          <div className="filter-controls">
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="all">All Errors</option>
              <option value="unresolved">Unresolved Only</option>
            </select>
          </div>
        </div>

        {/* Statistics Cards */}
        {stats && (
          <div className="stats-grid">
            <div className="stat-card total">
              <div className="stat-label">Total Errors</div>
              <div className="stat-value">{stats.total}</div>
            </div>
            <div className="stat-card unresolved">
              <div className="stat-label">Unresolved</div>
              <div className="stat-value">{stats.unresolved}</div>
            </div>
            <div className="stat-card by-severity">
              <div className="stat-label">By Severity</div>
              <div className="severity-breakdown">
                {Object.entries(stats.by_severity || {}).map(([sev, count]) => (
                  <div key={sev} className={`severity-item ${sev}`}>
                    {sev}: {count}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Error List */}
        <div className="errors-section">
          <h3>Error Reports ({errors.length})</h3>
          {errors.length === 0 ? (
            <div className="no-errors">✅ No errors to display</div>
          ) : (
            <div className="errors-list">
              {errors.map((error) => (
                <div key={error.id} className="error-card">
                  <div className="error-header">
                    <span
                      className={`severity-badge ${getSeverityClass(
                        error.severity
                      )}`}
                    >
                      {error.severity.toUpperCase()}
                    </span>
                    <span
                      className={`status-badge ${getStatusClass(error.status)}`}
                    >
                      {error.status}
                    </span>
                    <span className="error-date">
                      {new Date(error.occurred_at).toLocaleString()}
                    </span>
                  </div>

                  <div className="error-body">
                    <div className="error-type">
                      <strong>Type:</strong> {error.error_type}
                    </div>
                    <div className="error-message">
                      <strong>Message:</strong> {error.error_message}
                    </div>
                    {error.url && (
                      <div className="error-url">
                        <strong>URL:</strong> <code>{error.url}</code>
                      </div>
                    )}
                    {error.stack_trace && (
                      <details className="stack-trace">
                        <summary>Stack Trace</summary>
                        <pre>{error.stack_trace}</pre>
                      </details>
                    )}
                    {error.notes && (
                      <div className="error-notes">
                        <strong>Notes:</strong> {error.notes}
                      </div>
                    )}
                  </div>

                  <div className="error-actions">
                    {error.status !== "resolved" && (
                      <>
                        <button
                          className="btn btn-sm btn-warning"
                          onClick={() =>
                            handleStatusUpdate(error.id, "investigating")
                          }
                          disabled={error.status === "investigating"}
                        >
                          Investigate
                        </button>
                        <button
                          className="btn btn-sm btn-success"
                          onClick={() =>
                            handleStatusUpdate(error.id, "resolved")
                          }
                        >
                          Resolve
                        </button>
                      </>
                    )}
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={() => handleStatusUpdate(error.id, "ignored")}
                      disabled={error.status === "ignored"}
                    >
                      Ignore
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default ErrorReportDashboard;

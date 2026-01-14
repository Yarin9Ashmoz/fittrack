import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

import UserCreate from './pages/users/user_create';
import UsersList from './pages/users/users_list';
import UserDetails from './pages/users/user_details';

import SubscriptionsList from './pages/subscriptions/subscriptions_list';

import EnrollmentsList from "./pages/enrollments/enrollments_list";
import EnrollmentCreate from "./pages/enrollments/enrollment_create";
import ClassWaitlist from "./pages/classes/class_waitlist";

import CheckinsList from './pages/checkins/checkins_list';

import PlanCreate from './pages/plans/plan_create';
import PlanList from './pages/plans/plans_list';

import WorkoutItemCreate from './pages/workouts/workout_items/workout_item_create';
import WorkoutItemList from './pages/workouts/workout_items/workout_items_list';

import WorkoutPlansCreate from './pages/workouts/workout_plans/workout_plan_create';
import WorkoutPlansList from './pages/workouts/workout_plans/workout_plans_list';

import 'bootstrap/dist/css/bootstrap.css';

import ClassSessionCreate from './pages/classes/class_session_create';
import ClassSessionsList from './pages/classes/class_sessions_list';
import ClassSessionView from './pages/classes/class_session_view';

import PaymentsList from './pages/payments/payments_list';

import IntakeEvaluationForm from './components/IntakeEvaluationForm/IntakeEvaluationForm';
import IntakeEvaluationList from './components/IntakeEvaluationForm/IntakeEvaluationList';

import PersonalTrackingDashboard from './pages/PersonalTrackingDashboard/PersonalTrackingDashboard';
import ErrorReportDashboard from './pages/ErrorReportDashboard/ErrorReportDashboard';

import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';

const PrivateRoute = ({ children }) => {
    const { token, loading } = useAuth();
    if (loading) return <div>Loading...</div>;
    return token ? children : <Login />;
};

function App() {
    return (
        <AuthProvider>
            <Router>
                <div className="app-container">
                    <Routes>
                        <Route path="/login" element={<Login />} />

                        <Route path="/" element={
                            <PrivateRoute>
                                <Dashboard />
                            </PrivateRoute>
                        } />

                        <Route path="/users/create" element={<PrivateRoute><UserCreate /></PrivateRoute>} />
                        <Route path="/users/list" element={<PrivateRoute><UsersList /></PrivateRoute>} />
                        <Route path="/users/:userId" element={<PrivateRoute><UserDetails /></PrivateRoute>} />

                        <Route path="/subscriptions/list" element={<PrivateRoute><SubscriptionsList /></PrivateRoute>} />

                        <Route path="/enrollments/list" element={<PrivateRoute><EnrollmentsList /></PrivateRoute>} />
                        <Route path="/enroll/:classId" element={<PrivateRoute><EnrollmentCreate /></PrivateRoute>} />
                        <Route path="/classes/:classId/waitlist" element={<PrivateRoute><ClassWaitlist /></PrivateRoute>} />
                        
                        <Route path="/checkins/today" element={<PrivateRoute><CheckinsList /></PrivateRoute>} />

                        <Route path="/plans/create" element={<PrivateRoute><PlanCreate /></PrivateRoute>} />
                        <Route path="/plans/list" element={<PrivateRoute><PlanList /></PrivateRoute>} />

                        <Route path="/classes/create" element={<PrivateRoute><ClassSessionCreate /></PrivateRoute>} />
                        <Route path="/classes/list" element={<PrivateRoute><ClassSessionsList /></PrivateRoute>} />
                        <Route path="/classes/:classId" element={<PrivateRoute><ClassSessionView /></PrivateRoute>} />

                        <Route path="/payments/list" element={<PrivateRoute><PaymentsList /></PrivateRoute>} />

                        <Route path="/workout-item/create" element={<PrivateRoute><WorkoutItemCreate /></PrivateRoute>} />
                        <Route path="/workout-items/list" element={<PrivateRoute><WorkoutItemList /></PrivateRoute>} />

                        <Route path="/workout-plan/create" element={<PrivateRoute><WorkoutPlansCreate /></PrivateRoute>} />
                        <Route path="/workout-plans/list" element={<PrivateRoute><WorkoutPlansList /></PrivateRoute>} />

                        <Route path="/intake-evaluations/" element={<PrivateRoute><IntakeEvaluationForm /></PrivateRoute>} />
                        <Route path="/intake-evaluations/list" element={<PrivateRoute><IntakeEvaluationList /></PrivateRoute>} />
                        <Route path="/intake-evaluation/member/:memberId" element={<PrivateRoute><IntakeEvaluationForm /></PrivateRoute>} />
                        <Route path="/personal-tracking/:memberId" element={<PrivateRoute><PersonalTrackingDashboard /></PrivateRoute>} />
                        <Route path="/error-reports" element={<PrivateRoute><ErrorReportDashboard /></PrivateRoute>} />
                    </Routes>
                </div>
            </Router>
        </AuthProvider>
    );
}

export default App;

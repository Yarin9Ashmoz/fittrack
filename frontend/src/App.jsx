import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

import UserCreate from './pages/users/user_create';
import UsersList from './pages/users/users_list';
import UserDetails from './pages/users/user_details';

import SubscriptionsList from './pages/subscriptions/subscriptions_list';

import PlanCreate from './pages/plans/plan_create';
import PlanList from './pages/plans/plans_list';

import WorkoutItemCreate from './pages/workouts/workout_items/workout_item_create';
import WorkoutItemList from './pages/workouts/workout_items/workout_items_list';

import WorkoutPlansCreate from './pages/workouts/workout_plans/workout_plan_create';
import WorkoutPlansList from './pages/workouts/workout_plans/workout_plans_list';

import 'bootstrap/dist/css/bootstrap.css';

function App() {
    return (
        <Router>
            <div className="app-container">
                <Routes>
                    <Route path="/" element={<Dashboard />} />

                    <Route path="/users/create" element={<UserCreate />} />
                    <Route path="/users/list" element={<UsersList />} />
                    <Route path="/users/:userId" element={<UserDetails />} />

                    <Route path="/subscriptions/list" element={<SubscriptionsList />} />

                    <Route path="/plans/create" element={<PlanCreate />} />
                    <Route path="/plans/list" element={<PlanList />} />

                    <Route path="/workout-item/create" element={<WorkoutItemCreate />} />
                    <Route path="/workout-items/list" element={<WorkoutItemList />} />

                    <Route path="/workout-plan/create" element={<WorkoutPlansCreate />} />
                    <Route path="/workout-plans/list" element={<WorkoutPlansList />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;

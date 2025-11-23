import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Departments from './pages/Departments';
import Positions from './pages/Positions';
import Layout from './components/Layout';

function App() {
    const [user, setUser] = useState(null);

    const isAuthenticated = () => {
        return localStorage.getItem('token') !== null;
    };

    const PrivateRoute = ({ children }) => {
        return isAuthenticated() ? children : <Navigate to="/login" />;
    };

    return (
        <ConfigProvider
            theme={{
                token: {
                    colorPrimary: '#1890ff',
                },
            }}
        >
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={<Login setUser={setUser} />} />
                    <Route
                        path="/"
                        element={
                            <PrivateRoute>
                                <Layout user={user}>
                                    <Dashboard />
                                </Layout>
                            </PrivateRoute>
                        }
                    />
                    <Route
                        path="/employees"
                        element={
                            <PrivateRoute>
                                <Layout user={user}>
                                    <Employees />
                                </Layout>
                            </PrivateRoute>
                        }
                    />
                    <Route
                        path="/departments"
                        element={
                            <PrivateRoute>
                                <Layout user={user}>
                                    <Departments />
                                </Layout>
                            </PrivateRoute>
                        }
                    />
                    <Route
                        path="/positions"
                        element={
                            <PrivateRoute>
                                <Layout user={user}>
                                    <Positions />
                                </Layout>
                            </PrivateRoute>
                        }
                    />
                </Routes>
            </BrowserRouter>
        </ConfigProvider>
    );
}

export default App;

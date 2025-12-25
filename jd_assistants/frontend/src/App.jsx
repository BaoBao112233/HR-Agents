import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Departments from './pages/Departments';
import Positions from './pages/Positions';
import Candidates from './pages/Candidates';
import JobDescriptions from './pages/JobDescriptions';
import CVMatching from './pages/CVMatching';
import JDRewriting from './pages/JDRewriting';
import JDGenerator from './pages/JDGenerator';
import Settings from './pages/Settings';
import Layout from './components/Layout';
import { LanguageProvider } from './contexts/LanguageContext';
import { authAPI } from './services/api';

function App() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch user if token exists
        const token = localStorage.getItem('token');
        if (token) {
            authAPI.getCurrentUser()
                .then(response => {
                    setUser(response.data);
                })
                .catch(error => {
                    console.error('Failed to fetch user:', error);
                    // Clear invalid token
                    localStorage.removeItem('token');
                })
                .finally(() => {
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, []);

    const isAuthenticated = () => {
        return localStorage.getItem('token') !== null;
    };

    const PrivateRoute = ({ children }) => {
        if (loading) {
            return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
        }
        return isAuthenticated() ? children : <Navigate to="/login" />;
    };

    return (
        <LanguageProvider>
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
                        <Route
                            path="/recruitment/candidates"
                            element={
                                <PrivateRoute>
                                    <Layout user={user}>
                                        <Candidates />
                                    </Layout>
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/recruitment/job-descriptions"
                            element={
                                <PrivateRoute>
                                    <Layout user={user}>
                                        <JobDescriptions />
                                    </Layout>
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/recruitment/cv-matching"
                            element={
                                <PrivateRoute>
                                    <Layout user={user}>
                                        <CVMatching />
                                    </Layout>
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/recruitment/jd-rewriting"
                            element={
                                <PrivateRoute>
                                    <Layout user={user}>
                                        <JDRewriting />
                                    </Layout>
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/recruitment/jd-generator"
                            element={
                                <PrivateRoute>
                                    <Layout user={user}>
                                        <JDGenerator />
                                    </Layout>
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/settings"
                            element={
                                <PrivateRoute>
                                    <Layout user={user}>
                                        <Settings />
                                    </Layout>
                                </PrivateRoute>
                            }
                        />
                    </Routes>
                </BrowserRouter>
            </ConfigProvider>
        </LanguageProvider>
    );
}

export default App;

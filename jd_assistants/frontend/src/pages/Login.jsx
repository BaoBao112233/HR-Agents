import React, { useState } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import './Login.css';

function Login({ setUser }) {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const onFinish = async (values) => {
        setLoading(true);
        try {
            const response = await authAPI.login(values.email, values.password);
            const token = response.data.access_token;
            
            // Save token
            localStorage.setItem('token', token);
            
            message.success('Đăng nhập thành công!');
            
            // Redirect to home - let App.jsx handle user fetch
            window.location.href = '/';
        } catch (error) {
            console.error('Login error:', error);
            message.error(error.response?.data?.detail || 'Đăng nhập thất bại. Vui lòng kiểm tra lại email và mật khẩu.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <Card title="HR Management System" className="login-card">
                <Form
                    name="login"
                    onFinish={onFinish}
                    autoComplete="off"
                    layout="vertical"
                >
                    <Form.Item
                        label="Email"
                        name="email"
                        rules={[
                            { required: true, message: 'Please input your email!' },
                            { type: 'email', message: 'Please enter a valid email!' }
                        ]}
                    >
                        <Input prefix={<UserOutlined />} placeholder="Email" />
                    </Form.Item>

                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[{ required: true, message: 'Please input your password!' }]}
                    >
                        <Input.Password prefix={<LockOutlined />} placeholder="Password" />
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit" loading={loading} block>
                            Log In
                        </Button>
                    </Form.Item>
                </Form>
            </Card>
        </div>
    );
}

export default Login;

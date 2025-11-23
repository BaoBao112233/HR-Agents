import React, { useState, useEffect } from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown, Button } from 'antd';
import {
    DashboardOutlined,
    TeamOutlined,
    ApartmentOutlined,
    IdcardOutlined,
    LogoutOutlined,
    UserOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { authAPI } from '../services/api';

const { Header, Sider, Content } = AntLayout;

function Layout({ children, user }) {
    const navigate = useNavigate();
    const location = useLocation();
    const [currentUser, setCurrentUser] = useState(user);

    useEffect(() => {
        if (!user) {
            authAPI.getCurrentUser().then(res => setCurrentUser(res.data)).catch(() => { });
        }
    }, [user]);

    const menuItems = [
        { key: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
        { key: '/employees', icon: <TeamOutlined />, label: 'Employees' },
        { key: '/departments', icon: <ApartmentOutlined />, label: 'Departments' },
        { key: '/positions', icon: <IdcardOutlined />, label: 'Positions' },
    ];

    const handleMenuClick = ({ key }) => {
        navigate(key);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const userMenu = (
        <Menu>
            <Menu.Item key="profile" icon={<UserOutlined />}>
                Profile
            </Menu.Item>
            <Menu.Divider />
            <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
                Logout
            </Menu.Item>
        </Menu>
    );

    return (
        <AntLayout style={{ minHeight: '100vh' }}>
            <Sider theme="dark" collapsible>
                <div style={{ padding: '16px', textAlign: 'center', color: 'white', fontSize: '18px', fontWeight: 'bold' }}>
                    HR System
                </div>
                <Menu
                    theme="dark"
                    mode="inline"
                    selectedKeys={[location.pathname]}
                    items={menuItems}
                    onClick={handleMenuClick}
                />
            </Sider>
            <AntLayout>
                <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h2 style={{ margin: 0 }}>HR Management System</h2>
                    <Dropdown overlay={userMenu} placement="bottomRight">
                        <div style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Avatar icon={<UserOutlined />} />
                            <span>{currentUser?.email || 'User'}</span>
                        </div>
                    </Dropdown>
                </Header>
                <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
                    {children}
                </Content>
            </AntLayout>
        </AntLayout>
    );
}

export default Layout;

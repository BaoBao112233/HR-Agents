import React, { useState, useEffect } from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown, Button } from 'antd';
import {
    DashboardOutlined,
    TeamOutlined,
    ApartmentOutlined,
    IdcardOutlined,
    LogoutOutlined,
    UserOutlined,
    FileTextOutlined,
    ThunderboltOutlined,
    EditOutlined,
    UserAddOutlined,
    RobotOutlined,
    GlobalOutlined,
} from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import { authAPI } from '../services/api';
import { useLanguage } from '../contexts/LanguageContext';

const { Header, Sider, Content } = AntLayout;

function Layout({ children, user }) {
    const navigate = useNavigate();
    const location = useLocation();
    const [currentUser, setCurrentUser] = useState(user);
    const { language, toggleLanguage, t } = useLanguage();

    useEffect(() => {
        if (!user) {
            authAPI.getCurrentUser().then(res => setCurrentUser(res.data)).catch(() => { });
        }
    }, [user]);

    const menuItems = [
        { key: '/', icon: <DashboardOutlined />, label: t('nav.dashboard') },
        { key: '/employees', icon: <TeamOutlined />, label: t('nav.employees') },
        { key: '/departments', icon: <ApartmentOutlined />, label: t('nav.departments') },
        { key: '/positions', icon: <IdcardOutlined />, label: t('nav.positions') },
        {
            key: 'recruitment',
            icon: <UserAddOutlined />,
            label: t('nav.recruitment'),
            children: [
                { key: '/recruitment/candidates', icon: <FileTextOutlined />, label: t('nav.candidates') },
                { key: '/recruitment/job-descriptions', icon: <FileTextOutlined />, label: t('nav.jobDescriptions') },
                { key: '/recruitment/jd-generator', icon: <RobotOutlined />, label: t('nav.jdGenerator') },
                { key: '/recruitment/cv-matching', icon: <ThunderboltOutlined />, label: t('nav.cvMatching') },
                { key: '/recruitment/jd-rewriting', icon: <EditOutlined />, label: t('nav.jdRewriting') },
            ],
        },
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
                {t('nav.profile')}
            </Menu.Item>
            <Menu.Divider />
            <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
                {t('nav.logout')}
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
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                        <Button
                            icon={<GlobalOutlined />}
                            onClick={toggleLanguage}
                            type="text"
                        >
                            {language === 'en' ? '🇻🇳 Tiếng Việt' : '🇬🇧 English'}
                        </Button>
                        <Dropdown overlay={userMenu} placement="bottomRight">
                            <div style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <Avatar icon={<UserOutlined />} />
                                <span>{currentUser?.email || 'User'}</span>
                            </div>
                        </Dropdown>
                    </div>
                </Header>
                <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
                    {children}
                </Content>
            </AntLayout>
        </AntLayout>
    );
}

export default Layout;

import React from 'react';
import { Row, Col, Card, Statistic } from 'antd';
import { TeamOutlined, ApartmentOutlined, IdcardOutlined, UserAddOutlined } from '@ant-design/icons';

function Dashboard() {
    return (
        <div>
            <h1>Dashboard</h1>
            <Row gutter={16}>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Total Employees"
                            value={0}
                            prefix={<TeamOutlined />}
                            valueStyle={{ color: '#3f8600' }}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Departments"
                            value={0}
                            prefix={<ApartmentOutlined />}
                            valueStyle={{ color: '#1890ff' }}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="Positions"
                            value={0}
                            prefix={<IdcardOutlined />}
                            valueStyle={{ color: '#722ed1' }}
                        />
                    </Card>
                </Col>
                <Col span={6}>
                    <Card>
                        <Statistic
                            title="New This Month"
                            value={0}
                            prefix={<UserAddOutlined />}
                            valueStyle={{ color: '#cf1322' }}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
}

export default Dashboard;

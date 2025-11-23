import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, Select, DatePicker, message, Space } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { employeeAPI, departmentAPI, positionAPI } from '../services/api';
import dayjs from 'dayjs';

function Employees() {
    const [employees, setEmployees] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [positions, setPositions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [form] = Form.useForm();

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [empRes, deptRes, posRes] = await Promise.all([
                employeeAPI.list(),
                departmentAPI.list(),
                positionAPI.list(),
            ]);
            setEmployees(empRes.data);
            setDepartments(deptRes.data);
            setPositions(posRes.data);
        } catch (error) {
            message.error('Failed to load data');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = () => {
        form.resetFields();
        setModalVisible(true);
    };

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            const data = {
                ...values,
                join_date: values.join_date.format('YYYY-MM-DD'),
                date_of_birth: values.date_of_birth?.format('YYYY-MM-DD'),
            };
            await employeeAPI.create(data);
            message.success('Employee created successfully');
            setModalVisible(false);
            loadData();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to create employee');
        }
    };

    const columns = [
        { title: 'Code', dataIndex: 'employee_code', key: 'employee_code' },
        { title: 'First Name', dataIndex: 'first_name', key: 'first_name' },
        { title: 'Last Name', dataIndex: 'last_name', key: 'last_name' },
        { title: 'Email', dataIndex: 'email', key: 'email' },
        { title: 'Phone', dataIndex: 'phone', key: 'phone' },
        { title: 'Status', dataIndex: 'status', key: 'status' },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Space>
                    <Button icon={<EditOutlined />} size="small">Edit</Button>
                    <Button icon={<DeleteOutlined />} size="small" danger>Delete</Button>
                </Space>
            ),
        },
    ];

    return (
        <div>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
                <h1>Employees</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
                    Add Employee
                </Button>
            </div>
            <Table
                columns={columns}
                dataSource={employees}
                rowKey="id"
                loading={loading}
            />
            <Modal
                title="Create Employee"
                open={modalVisible}
                onOk={handleSubmit}
                onCancel={() => setModalVisible(false)}
                width={600}
            >
                <Form form={form} layout="vertical">
                    <Form.Item name="first_name" label="First Name" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="last_name" label="Last Name" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="email" label="Email" rules={[{ required: true, type: 'email' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="password" label="Password" rules={[{ required: true }]}>
                        <Input.Password />
                    </Form.Item>
                    <Form.Item name="phone" label="Phone">
                        <Input />
                    </Form.Item>
                    <Form.Item name="date_of_birth" label="Date of Birth">
                        <DatePicker style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="gender" label="Gender">
                        <Select>
                            <Select.Option value="male">Male</Select.Option>
                            <Select.Option value="female">Female</Select.Option>
                            <Select.Option value="other">Other</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="department_id" label="Department">
                        <Select>
                            {departments.map(d => (
                                <Select.Option key={d.id} value={d.id}>{d.name}</Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                    <Form.Item name="position_id" label="Position">
                        <Select>
                            {positions.map(p => (
                                <Select.Option key={p.id} value={p.id}>{p.title}</Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                    <Form.Item name="join_date" label="Join Date" rules={[{ required: true }]}>
                        <DatePicker style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="contract_type" label="Contract Type" rules={[{ required: true }]}>
                        <Select>
                            <Select.Option value="full_time">Full Time</Select.Option>
                            <Select.Option value="part_time">Part Time</Select.Option>
                            <Select.Option value="contract">Contract</Select.Option>
                            <Select.Option value="intern">Intern</Select.Option>
                        </Select>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
}

export default Employees;

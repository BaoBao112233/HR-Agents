import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { departmentAPI } from '../services/api';

function Departments() {
    const [departments, setDepartments] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [form] = Form.useForm();

    useEffect(() => {
        loadDepartments();
    }, []);

    const loadDepartments = async () => {
        setLoading(true);
        try {
            const response = await departmentAPI.list();
            setDepartments(response.data);
        } catch (error) {
            message.error('Failed to load departments');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async () => {
        try {
            const values = await form.validateFields();
            await departmentAPI.create(values);
            message.success('Department created successfully');
            setModalVisible(false);
            form.resetFields();
            loadDepartments();
        } catch (error) {
            message.error('Failed to create department');
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        { title: 'Name', dataIndex: 'name', key: 'name' },
        { title: 'Description', dataIndex: 'description', key: 'description' },
    ];

    return (
        <div>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
                <h1>Departments</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
                    Add Department
                </Button>
            </div>
            <Table columns={columns} dataSource={departments} rowKey="id" loading={loading} />
            <Modal
                title="Create Department"
                open={modalVisible}
                onOk={handleCreate}
                onCancel={() => setModalVisible(false)}
            >
                <Form form={form} layout="vertical">
                    <Form.Item name="name" label="Name" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="description" label="Description">
                        <Input.TextArea rows={4} />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
}

export default Departments;

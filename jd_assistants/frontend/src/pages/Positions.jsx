import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { positionAPI } from '../services/api';

function Positions() {
    const [positions, setPositions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [form] = Form.useForm();

    useEffect(() => {
        loadPositions();
    }, []);

    const loadPositions = async () => {
        setLoading(true);
        try {
            const response = await positionAPI.list();
            setPositions(response.data);
        } catch (error) {
            message.error('Failed to load positions');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = async () => {
        try {
            const values = await form.validateFields();
            await positionAPI.create(values);
            message.success('Position created successfully');
            setModalVisible(false);
            form.resetFields();
            loadPositions();
        } catch (error) {
            message.error('Failed to create position');
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        { title: 'Title', dataIndex: 'title', key: 'title' },
        { title: 'Level', dataIndex: 'level', key: 'level' },
        { title: 'Salary Min', dataIndex: 'salary_range_min', key: 'salary_range_min' },
        { title: 'Salary Max', dataIndex: 'salary_range_max', key: 'salary_range_max' },
    ];

    return (
        <div>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
                <h1>Positions</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
                    Add Position
                </Button>
            </div>
            <Table columns={columns} dataSource={positions} rowKey="id" loading={loading} />
            <Modal
                title="Create Position"
                open={modalVisible}
                onOk={handleCreate}
                onCancel={() => setModalVisible(false)}
            >
                <Form form={form} layout="vertical">
                    <Form.Item name="title" label="Title" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="description" label="Description">
                        <Input.TextArea rows={4} />
                    </Form.Item>
                    <Form.Item name="level" label="Level">
                        <Input />
                    </Form.Item>
                    <Form.Item name="salary_range_min" label="Minimum Salary">
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                    <Form.Item name="salary_range_max" label="Maximum Salary">
                        <InputNumber style={{ width: '100%' }} />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
}

export default Positions;

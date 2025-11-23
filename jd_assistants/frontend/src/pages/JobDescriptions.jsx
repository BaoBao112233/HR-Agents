import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Tag, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { jobDescriptionAPI } from '../services/api';

function JobDescriptions() {
    const [jds, setJds] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingJD, setEditingJD] = useState(null);
    const [form] = Form.useForm();

    useEffect(() => {
        loadJDs();
    }, []);

    const loadJDs = async () => {
        setLoading(true);
        try {
            const response = await jobDescriptionAPI.list();
            setJds(response.data);
        } catch (error) {
            message.error('Failed to load job descriptions');
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = () => {
        form.resetFields();
        setEditingJD(null);
        setModalVisible(true);
    };

    const handleEdit = (jd) => {
        form.setFieldsValue(jd);
        setEditingJD(jd);
        setModalVisible(true);
    };

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            if (editingJD) {
                await jobDescriptionAPI.update(editingJD.id, values);
                message.success('Job description updated successfully');
            } else {
                await jobDescriptionAPI.create(values);
                message.success('Job description created successfully');
            }
            setModalVisible(false);
            loadJDs();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (id) => {
        try {
            await jobDescriptionAPI.delete(id);
            message.success('Job description deleted successfully');
            loadJDs();
        } catch (error) {
            message.error('Failed to delete job description');
        }
    };

    const handleActivate = async (id) => {
        try {
            await jobDescriptionAPI.activate(id);
            message.success('Job description activated successfully');
            loadJDs();
        } catch (error) {
            message.error('Failed to activate job description');
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
        { title: 'Title', dataIndex: 'title', key: 'title' },
        {
            title: 'Skills',
            dataIndex: 'skills',
            key: 'skills',
            render: (skills) => skills?.substring(0, 80) + (skills?.length > 80 ? '...' : '')
        },
        {
            title: 'Status',
            dataIndex: 'is_active',
            key: 'is_active',
            render: (active) => active ?
                <Tag color="green">Active</Tag> :
                <Tag>Inactive</Tag>
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Space>
                    <Button icon={<EditOutlined />} size="small" onClick={() => handleEdit(record)}>
                        Edit
                    </Button>
                    {!record.is_active && (
                        <Button
                            icon={<CheckCircleOutlined />}
                            size="small"
                            type="primary"
                            onClick={() => handleActivate(record.id)}
                        >
                            Set Active
                        </Button>
                    )}
                    <Popconfirm
                        title="Delete JD?"
                        onConfirm={() => handleDelete(record.id)}
                        okText="Yes"
                        cancelText="No"
                    >
                        <Button icon={<DeleteOutlined />} size="small" danger>Delete</Button>
                    </Popconfirm>
                </Space>
            ),
        },
    ];

    return (
        <div>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
                <h1>📋 Job Descriptions</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
                    Create Job Description
                </Button>
            </div>
            <Table
                columns={columns}
                dataSource={jds}
                rowKey="id"
                loading={loading}
                pagination={{ pageSize: 10 }}
            />
            <Modal
                title={editingJD ? "Edit Job Description" : "Create Job Description"}
                open={modalVisible}
                onOk={handleSubmit}
                onCancel={() => setModalVisible(false)}
                width={700}
            >
                <Form form={form} layout="vertical">
                    <Form.Item name="title" label="Job Title" rules={[{ required: true }]}>
                        <Input placeholder="e.g., Senior Backend Developer" />
                    </Form.Item>
                    <Form.Item name="description" label="Job Description" rules={[{ required: true }]}>
                        <Input.TextArea rows={8} placeholder="Enter full job description..." />
                    </Form.Item>
                    <Form.Item name="skills" label="Required Skills" rules={[{ required: true }]}>
                        <Input.TextArea rows={3} placeholder="Python, FastAPI, PostgreSQL, Docker..." />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
}

export default JobDescriptions;

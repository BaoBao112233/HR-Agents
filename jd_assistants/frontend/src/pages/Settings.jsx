import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Select, Table, message, Modal, Space } from 'antd';
import { PlusOutlined, DeleteOutlined, KeyOutlined } from '@ant-design/icons';
import { apiKeysAPI } from '../services/api';

const { Option } = Select;

function Settings() {
    const [keys, setKeys] = useState([]);
    const [providers, setProviders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [form] = Form.useForm();

    useEffect(() => {
        loadProviders();
        loadKeys();
    }, []);

    const loadProviders = async () => {
        try {
            const response = await apiKeysAPI.listProviders();
            setProviders(response.data.providers);
        } catch (error) {
            message.error('Failed to load providers');
        }
    };

    const loadKeys = async () => {
        setLoading(true);
        try {
            const response = await apiKeysAPI.listKeys();
            setKeys(response.data.keys);
        } catch (error) {
            message.error('Failed to load API keys');
        } finally {
            setLoading(false);
        }
    };

    const handleAddKey = async (values) => {
        try {
            await apiKeysAPI.addKey(values);
            message.success('API key added successfully');
            setModalVisible(false);
            form.resetFields();
            loadKeys();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to add API key');
        }
    };

    const handleDeleteKey = async (keyId) => {
        Modal.confirm({
            title: 'Delete API Key',
            content: 'Are you sure you want to delete this API key?',
            okText: 'Delete',
            okType: 'danger',
            onOk: async () => {
                try {
                    await apiKeysAPI.deleteKey(keyId);
                    message.success('API key deleted successfully');
                    loadKeys();
                } catch (error) {
                    message.error('Failed to delete API key');
                }
            }
        });
    };

    const columns = [
        {
            title: 'Provider',
            dataIndex: 'provider',
            key: 'provider',
            render: (provider) => {
                const p = providers.find(prov => prov.id === provider);
                return p ? p.name : provider;
            }
        },
        {
            title: 'Key Name',
            dataIndex: 'key_name',
            key: 'key_name',
        },
        {
            title: 'API Key',
            dataIndex: 'api_key_preview',
            key: 'api_key_preview',
            render: (preview) => <code>{preview}</code>
        },
        {
            title: 'Status',
            dataIndex: 'is_active',
            key: 'is_active',
            render: (active) => (
                <span style={{ color: active ? '#52c41a' : '#999' }}>
                    {active ? 'Active' : 'Inactive'}
                </span>
            )
        },
        {
            title: 'Created',
            dataIndex: 'created_at',
            key: 'created_at',
            render: (date) => new Date(date).toLocaleDateString()
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => handleDeleteKey(record.id)}
                >
                    Delete
                </Button>
            )
        }
    ];

    return (
        <div>
            <h1>⚙️ Settings</h1>
            
            <Card
                title="LLM API Keys"
                extra={
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={() => setModalVisible(true)}
                    >
                        Add API Key
                    </Button>
                }
            >
                <Table
                    dataSource={keys}
                    columns={columns}
                    loading={loading}
                    rowKey="id"
                    pagination={{ pageSize: 10 }}
                />
            </Card>

            <Modal
                title="Add API Key"
                open={modalVisible}
                onCancel={() => {
                    setModalVisible(false);
                    form.resetFields();
                }}
                footer={null}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleAddKey}
                >
                    <Form.Item
                        name="provider"
                        label="Provider"
                        rules={[{ required: true, message: 'Please select a provider' }]}
                    >
                        <Select placeholder="Select LLM Provider">
                            {providers.map(provider => (
                                <Option key={provider.id} value={provider.id}>
                                    <Space>
                                        <KeyOutlined />
                                        {provider.name}
                                        <span style={{ color: '#999', fontSize: '12px' }}>
                                            ({provider.description})
                                        </span>
                                    </Space>
                                </Option>
                            ))}
                        </Select>
                    </Form.Item>

                    <Form.Item
                        name="key_name"
                        label="Key Name (Optional)"
                    >
                        <Input placeholder="e.g., Production Key, Test Key" />
                    </Form.Item>

                    <Form.Item
                        name="api_key"
                        label="API Key"
                        rules={[{ required: true, message: 'Please enter the API key' }]}
                    >
                        <Input.Password placeholder="Enter your API key" />
                    </Form.Item>

                    <Form.Item>
                        <Space>
                            <Button type="primary" htmlType="submit">
                                Add Key
                            </Button>
                            <Button onClick={() => {
                                setModalVisible(false);
                                form.resetFields();
                            }}>
                                Cancel
                            </Button>
                        </Space>
                    </Form.Item>
                </Form>
            </Modal>

            <Card
                title="Supported Providers"
                style={{ marginTop: 16 }}
            >
                {providers.map(provider => (
                    <Card.Grid key={provider.id} style={{ width: '50%' }}>
                        <h3>{provider.name}</h3>
                        <p style={{ color: '#666' }}>{provider.description}</p>
                        <p>
                            <strong>Default Model:</strong>{' '}
                            <code>{provider.default_model}</code>
                        </p>
                        <p>
                            <strong>Available Models:</strong>{' '}
                            {provider.models.map(m => (
                                <code key={m} style={{ marginRight: 8 }}>{m}</code>
                            ))}
                        </p>
                    </Card.Grid>
                ))}
            </Card>
        </div>
    );
}

export default Settings;

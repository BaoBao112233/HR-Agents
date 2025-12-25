import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, Select, Table, message, Modal, Space, Typography, Alert, Tag, Divider } from 'antd';
import { PlusOutlined, DeleteOutlined, KeyOutlined, InfoCircleOutlined, LinkOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { apiKeysAPI } from '../services/api';

const { Option } = Select;
const { Title, Text, Paragraph } = Typography;

function Settings() {
    const [keys, setKeys] = useState([]);
    const [providers, setProviders] = useState([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [form] = Form.useForm();
    const [selectedProvider, setSelectedProvider] = useState(null);

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
            message.success('🎉 API key đã được thêm thành công!');
            setModalVisible(false);
            form.resetFields();
            setSelectedProvider(null);
            loadKeys();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Không thể thêm API key');
        }
    };

    const handleDeleteKey = async (keyId) => {
        Modal.confirm({
            title: 'Xóa API Key',
            content: 'Bạn có chắc chắn muốn xóa API key này không? Các tính năng AI sẽ không hoạt động nếu không có key.',
            okText: 'Xóa',
            cancelText: 'Hủy',
            okType: 'danger',
            onOk: async () => {
                try {
                    await apiKeysAPI.deleteKey(keyId);
                    message.success('API key đã được xóa');
                    loadKeys();
                } catch (error) {
                    message.error('Không thể xóa API key');
                }
            }
        });
    };

    const getProviderInfo = (providerId) => {
        return providers.find(p => p.id === providerId);
    };

    const getAPIKeyUrl = (providerId) => {
        const urls = {
            'openai': 'https://platform.openai.com/api-keys',
            'groq': 'https://console.groq.com/keys',
            'gemini': 'https://makersuite.google.com/app/apikey',
            'openrouter': 'https://openrouter.ai/keys'
        };
        return urls[providerId] || '#';
    };

    const columns = [
        {
            title: 'Nhà cung cấp',
            dataIndex: 'provider',
            key: 'provider',
            render: (provider) => {
                const p = providers.find(prov => prov.id === provider);
                return p ? (
                    <Space>
                        <KeyOutlined style={{ color: '#1890ff' }} />
                        <strong>{p.name}</strong>
                    </Space>
                ) : provider;
            }
        },
        {
            title: 'Tên Key',
            dataIndex: 'key_name',
            key: 'key_name',
        },
        {
            title: 'Model',
            dataIndex: 'model',
            key: 'model',
            render: (model) => (
                model ? (
                    <Tag color="purple" style={{ fontFamily: 'monospace' }}>
                        {model}
                    </Tag>
                ) : (
                    <Text type="secondary">Chưa chọn</Text>
                )
            )
        },
        {
            title: 'API Key',
            dataIndex: 'api_key_preview',
            key: 'api_key_preview',
            render: (preview) => (
                <Tag color="blue" style={{ fontFamily: 'monospace' }}>
                    {preview}
                </Tag>
            )
        },
        {
            title: 'Trạng thái',
            dataIndex: 'is_active',
            key: 'is_active',
            render: (active) => (
                <Tag icon={<CheckCircleOutlined />} color={active ? 'success' : 'default'}>
                    {active ? 'Đang hoạt động' : 'Không hoạt động'}
                </Tag>
            )
        },
        {
            title: 'Ngày tạo',
            dataIndex: 'created_at',
            key: 'created_at',
            render: (date) => new Date(date).toLocaleDateString('vi-VN')
        },
        {
            title: 'Thao tác',
            key: 'actions',
            render: (_, record) => (
                <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={() => handleDeleteKey(record.id)}
                >
                    Xóa
                </Button>
            )
        }
    ];

    return (
        <div>
            <Title level={2}>⚙️ Cấu hình hệ thống</Title>
            <Paragraph type="secondary">
                Quản lý API keys của các nhà cung cấp AI để sử dụng các tính năng phân tích JD, viết lại JD, và đánh giá CV.
            </Paragraph>

            <Alert
                message="Lưu ý quan trọng"
                description={
                    <div>
                        <p>• API keys của bạn được lưu trữ an toàn và chỉ bạn mới có thể truy cập.</p>
                        <p>• Mỗi nhà cung cấp có thể có nhiều keys, nhưng chỉ có một key hoạt động tại một thời điểm.</p>
                        <p>• Bạn cần ít nhất một API key đang hoạt động để sử dụng các tính năng AI.</p>
                    </div>
                }
                type="info"
                icon={<InfoCircleOutlined />}
                showIcon
                style={{ marginBottom: 24 }}
            />
            
            <Card
                title={<span><KeyOutlined /> Quản lý API Keys</span>}
                extra={
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={() => setModalVisible(true)}
                        size="large"
                    >
                        Thêm API Key
                    </Button>
                }
            >
                {keys.length === 0 && !loading ? (
                    <Alert
                        message="Chưa có API key nào"
                        description="Hãy thêm API key đầu tiên để bắt đầu sử dụng các tính năng AI."
                        type="warning"
                        showIcon
                        style={{ marginBottom: 16 }}
                    />
                ) : null}
                
                <Table
                    dataSource={keys}
                    columns={columns}
                    loading={loading}
                    rowKey="id"
                    pagination={{ pageSize: 10 }}
                />
            </Card>

            <Modal
                title={<span><PlusOutlined /> Thêm API Key mới</span>}
                open={modalVisible}
                onCancel={() => {
                    setModalVisible(false);
                    form.resetFields();
                    setSelectedProvider(null);
                }}
                footer={null}
                width={600}
            >
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleAddKey}
                >
                    <Form.Item
                        name="provider"
                        label="Nhà cung cấp AI"
                        rules={[{ required: true, message: 'Vui lòng chọn nhà cung cấp' }]}
                    >
                        <Select 
                            placeholder="Chọn nhà cung cấp AI"
                            onChange={(value) => setSelectedProvider(value)}
                            size="large"
                        >
                            {providers.map(provider => (
                                <Option key={provider.id} value={provider.id}>
                                    <Space>
                                        <KeyOutlined style={{ color: '#1890ff' }} />
                                        <strong>{provider.name}</strong>
                                        <Text type="secondary" style={{ fontSize: '12px' }}>
                                            - {provider.description}
                                        </Text>
                                    </Space>
                                </Option>
                            ))}
                        </Select>
                    </Form.Item>

                    {selectedProvider && (
                        <>
                            <Alert
                                message={`Lấy API key từ ${getProviderInfo(selectedProvider)?.name}`}
                                description={
                                    <Space direction="vertical">
                                        <Text>Bạn có thể lấy API key tại:</Text>
                                        <Button
                                            type="link"
                                            icon={<LinkOutlined />}
                                            href={getAPIKeyUrl(selectedProvider)}
                                            target="_blank"
                                        >
                                            {getAPIKeyUrl(selectedProvider)}
                                        </Button>
                                    </Space>
                                }
                                type="info"
                                showIcon
                                style={{ marginBottom: 16 }}
                            />

                            <Form.Item
                                name="model"
                                label="Model"
                                rules={[{ required: true, message: 'Vui lòng chọn model' }]}
                                tooltip="Chọn model AI sẽ được sử dụng cho các tính năng phân tích"
                            >
                                <Select 
                                    placeholder="Chọn model AI"
                                    size="large"
                                >
                                    {getProviderInfo(selectedProvider)?.models.map(model => (
                                        <Option key={model} value={model}>
                                            <Space>
                                                <Text strong>{model}</Text>
                                                {model === getProviderInfo(selectedProvider)?.default_model && (
                                                    <Tag color="green">Mặc định</Tag>
                                                )}
                                            </Space>
                                        </Option>
                                    ))}
                                </Select>
                            </Form.Item>
                        </>
                    )}

                    <Form.Item
                        name="key_name"
                        label="Tên key (Tùy chọn)"
                        tooltip="Đặt tên để dễ nhận biết, ví dụ: Production Key, Test Key"
                    >
                        <Input 
                            placeholder="Ví dụ: Production Key, Test Key" 
                            size="large"
                        />
                    </Form.Item>

                    <Form.Item
                        name="api_key"
                        label="API Key"
                        rules={[
                            { required: true, message: 'Vui lòng nhập API key' },
                            { min: 20, message: 'API key quá ngắn, vui lòng kiểm tra lại' }
                        ]}
                    >
                        <Input.Password 
                            placeholder="Nhập API key của bạn" 
                            size="large"
                        />
                    </Form.Item>

                    <Form.Item>
                        <Space>
                            <Button type="primary" htmlType="submit" size="large">
                                Thêm Key
                            </Button>
                            <Button onClick={() => {
                                setModalVisible(false);
                                form.resetFields();
                                setSelectedProvider(null);
                            }} size="large">
                                Hủy
                            </Button>
                        </Space>
                    </Form.Item>
                </Form>
            </Modal>

            <Divider />

            <Card
                title={<span><InfoCircleOutlined /> Các nhà cung cấp được hỗ trợ</span>}
                style={{ marginTop: 24 }}
            >
                <Paragraph type="secondary">
                    Dưới đây là danh sách các nhà cung cấp AI được hệ thống hỗ trợ và các models có sẵn.
                </Paragraph>
                
                {providers.map(provider => (
                    <Card.Grid key={provider.id} style={{ width: '50%', minHeight: 200 }}>
                        <Space direction="vertical" size="small" style={{ width: '100%' }}>
                            <Title level={4} style={{ marginBottom: 8 }}>
                                <KeyOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                                {provider.name}
                            </Title>
                            
                            <Paragraph type="secondary" style={{ marginBottom: 12 }}>
                                {provider.description}
                            </Paragraph>
                            
                            <div>
                                <Text strong>Model mặc định: </Text>
                                <Tag color="blue">{provider.default_model}</Tag>
                            </div>
                            
                            <div>
                                <Text strong>Các models có sẵn:</Text>
                                <div style={{ marginTop: 8 }}>
                                    {provider.models.map(m => (
                                        <Tag key={m} style={{ marginBottom: 4 }}>
                                            {m}
                                        </Tag>
                                    ))}
                                </div>
                            </div>
                            
                            <Button
                                type="link"
                                icon={<LinkOutlined />}
                                href={getAPIKeyUrl(provider.id)}
                                target="_blank"
                                style={{ paddingLeft: 0 }}
                            >
                                Lấy API key
                            </Button>
                        </Space>
                    </Card.Grid>
                ))}
            </Card>
        </div>
    );
}

export default Settings;

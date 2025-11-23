import React, { useState, useEffect } from 'react';
import { Table, Button, Upload, message, Space, Popconfirm } from 'antd';
import { UploadOutlined, DeleteOutlined } from '@ant-design/icons';
import { candidateAPI } from '../services/api';

function Candidates() {
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);

    useEffect(() => {
        loadCandidates();
    }, []);

    const loadCandidates = async () => {
        setLoading(true);
        try {
            const response = await candidateAPI.list();
            setCandidates(response.data);
        } catch (error) {
            message.error('Failed to load candidates');
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async ({ fileList }) => {
        if (fileList.length === 0) return;

        setUploading(true);
        try {
            const files = fileList.map(file => file.originFileObj);
            const response = await candidateAPI.uploadCV(files);
            message.success(`Uploaded ${response.data.success} CV(s) successfully!`);
            if (response.data.errors.length > 0) {
                response.data.errors.forEach(err => message.warning(err));
            }
            loadCandidates();
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to upload CVs');
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (id) => {
        try {
            await candidateAPI.delete(id);
            message.success('Candidate deleted successfully');
            loadCandidates();
        } catch (error) {
            message.error('Failed to delete candidate');
        }
    };

    const columns = [
        { title: 'Name', dataIndex: 'name', key: 'name' },
        { title: 'Email', dataIndex: 'email', key: 'email' },
        {
            title: 'Skills',
            dataIndex: 'skills',
            key: 'skills',
            render: (skills) => skills.substring(0, 100) + (skills.length > 100 ? '...' : '')
        },
        {
            title: 'Bio',
            dataIndex: 'bio',
            key: 'bio',
            render: (bio) => bio?.substring(0, 150) + (bio?.length > 150 ? '...' : '')
        },
        {
            title: 'Actions',
            key: 'actions',
            render: (_, record) => (
                <Popconfirm
                    title="Delete candidate?"
                    description="This action cannot be undone"
                    onConfirm={() => handleDelete(record.id)}
                    okText="Yes"
                    cancelText="No"
                >
                    <Button icon={<DeleteOutlined />} size="small" danger>Delete</Button>
                </Popconfirm>
            ),
        },
    ];

    return (
        <div>
            <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
                <h1>📄 Candidates</h1>
                <Upload
                    accept=".pdf"
                    multiple
                    beforeUpload={() => false}
                    onChange={handleUpload}
                    showUploadList={false}
                >
                    <Button type="primary" icon={<UploadOutlined />} loading={uploading}>
                        Upload CVs (PDF)
                    </Button>
                </Upload>
            </div>
            <Table
                columns={columns}
                dataSource={candidates}
                rowKey="id"
                loading={loading}
                pagination={{ pageSize: 10 }}
            />
        </div>
    );
}

export default Candidates;

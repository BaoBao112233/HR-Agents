import React, { useState } from 'react';
import { Button, Table, message, Progress, Alert } from 'antd';
import { ThunderboltOutlined } from '@ant-design/icons';
import { scoringAPI } from '../services/api';

function CVMatching() {
    const [scores, setScores] = useState([]);
    const [loading, setLoading] = useState(false);
    const [jdInfo, setJdInfo] = useState(null);

    const handleScoreAll = async () => {
        setLoading(true);
        try {
            const response = await scoringAPI.scoreAll();
            setScores(response.data.results);
            setJdInfo({
                id: response.data.jd_id,
                title: response.data.jd_title,
                total: response.data.total_scored
            });
            message.success(`Scored ${response.data.total_scored} candidates successfully!`);
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to score candidates');
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score) => {
        if (score >= 80) return 'success';
        if (score >= 60) return 'normal';
        if (score >= 40) return 'exception';
        return 'exception';
    };

    const columns = [
        {
            title: 'Candidate',
            dataIndex: 'name',
            key: 'name',
            sorter: (a, b) => a.name.localeCompare(b.name)
        },
        {
            title: 'Score',
            dataIndex: 'score',
            key: 'score',
            width: 200,
            render: (score) => (
                <Progress
                    percent={score}
                    status={getScoreColor(score)}
                    strokeColor={
                        score >= 80 ? '#52c41a' :
                            score >= 60 ? '#1890ff' :
                                score >= 40 ? '#faad14' : '#f5222d'
                    }
                />
            ),
            sorter: (a, b) => b.score - a.score,
            defaultSortOrder: 'ascend'
        },
        {
            title: 'Reason',
            dataIndex: 'reason',
            key: 'reason',
            ellipsis: true
        },
    ];

    return (
        <div>
            <div style={{ marginBottom: 16 }}>
                <h1>🎯 CV-JD Matching</h1>
                <p style={{ color: '#666' }}>
                    Score all candidates against the active job description using AI
                </p>
            </div>

            {jdInfo && (
                <Alert
                    message={`Scoring Results for: ${jdInfo.title}`}
                    description={`Total candidates scored: ${jdInfo.total}`}
                    type="success"
                    showIcon
                    style={{ marginBottom: 16 }}
                />
            )}

            <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                onClick={handleScoreAll}
                loading={loading}
                size="large"
                style={{ marginBottom: 16 }}
            >
                Score All Candidates
            </Button>

            {scores.length > 0 && (
                <Table
                    columns={columns}
                    dataSource={scores}
                    rowKey={(record) => `${record.name}-${record.score}`}
                    loading={loading}
                    pagination={{ pageSize: 20 }}
                />
            )}

            {scores.length === 0 && !loading && (
                <Alert
                    message="No Scores Yet"
                    description="Click 'Score All Candidates' button to evaluate all candidates against the active job description."
                    type="info"
                    showIcon
                />
            )}
        </div>
    );
}

export default CVMatching;

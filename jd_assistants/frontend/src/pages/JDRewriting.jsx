import React, { useState } from 'react';
import { Row, Col, Input, Button, Card, message, Alert, List, Tag } from 'antd';
import { BulbOutlined, EditOutlined } from '@ant-design/icons';
import { jdAIAPI } from '../services/api';

const { TextArea } = Input;

function JDRewriting() {
    const [inputJD, setInputJD] = useState('');
    const [analysis, setAnalysis] = useState(null);
    const [rewritten, setRewritten] = useState('');
    const [analyzing, setAnalyzing] = useState(false);
    const [rewriting, setRewriting] = useState(false);

    const handleAnalyze = async () => {
        if (!inputJD.trim()) {
            message.warning('Please enter a job description to analyze');
            return;
        }

        setAnalyzing(true);
        try {
            const response = await jdAIAPI.analyze(inputJD);
            setAnalysis(response.data);
            message.success('Analysis complete!');
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to analyze JD');
        } finally {
            setAnalyzing(false);
        }
    };

    const handleRewrite = async () => {
        if (!inputJD.trim()) {
            message.warning('Please enter a job description to rewrite');
            return;
        }

        setRewriting(true);
        try {
            const response = await jdAIAPI.rewrite(inputJD);
            setRewritten(response.data.rewritten);
            message.success('JD rewritten successfully!');
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to rewrite JD');
        } finally {
            setRewriting(false);
        }
    };

    return (
        <div>
            <div style={{ marginBottom: 16 }}>
                <h1>✍️ AI-Powered JD Rewriting</h1>
                <p style={{ color: '#666' }}>
                    Use AI to analyze and improve your job descriptions
                </p>
            </div>

            <Row gutter={16}>
                <Col span={12}>
                    <Card title="Original Job Description" extra={
                        <Button.Group>
                            <Button
                                type="primary"
                                icon={<BulbOutlined />}
                                onClick={handleAnalyze}
                                loading={analyzing}
                            >
                                Analyze
                            </Button>
                            <Button
                                icon={<EditOutlined />}
                                onClick={handleRewrite}
                                loading={rewriting}
                            >
                                Rewrite
                            </Button>
                        </Button.Group>
                    }>
                        <TextArea
                            rows={15}
                            placeholder="Paste your job description here..."
                            value={inputJD}
                            onChange={(e) => setInputJD(e.target.value)}
                        />
                    </Card>
                </Col>

                <Col span={12}>
                    {analysis && !rewritten && (
                        <Card title="📊 Analysis Results">
                            <Alert
                                message={`Overall Score: ${analysis.overall_score}/100`}
                                type={analysis.overall_score >= 70 ? 'success' : 'warning'}
                                showIcon
                                style={{ marginBottom: 16 }}
                            />

                            <h3>🎯 Key Recommendations:</h3>
                            <List
                                size="small"
                                dataSource={analysis.key_recommendations || []}
                                renderItem={item => (
                                    <List.Item>
                                        <Tag color="blue">→</Tag> {item}
                                    </List.Item>
                                )}
                                style={{ marginBottom: 16 }}
                            />

                            {analysis.improvements && analysis.improvements.length > 0 && (
                                <>
                                    <h3>📝 Suggested Improvements:</h3>
                                    {analysis.improvements.map((imp, idx) => (
                                        <Card
                                            key={idx}
                                            size="small"
                                            style={{ marginBottom: 8 }}
                                            title={<Tag color="purple">{imp.section}</Tag>}
                                        >
                                            <p><strong>Reason:</strong> {imp.reason}</p>
                                            <TextArea
                                                rows={3}
                                                value={imp.improved}
                                                readOnly
                                                style={{ marginTop: 8 }}
                                            />
                                        </Card>
                                    ))}
                                </>
                            )}
                        </Card>
                    )}

                    {rewritten && (
                        <Card title="✨ Rewritten Job Description">
                            <Alert
                                message="AI-Generated Job Description"
                                description="Review and edit as needed before publishing"
                                type="success"
                                showIcon
                                style={{ marginBottom: 16 }}
                            />
                            <TextArea
                                rows={20}
                                value={rewritten}
                                onChange={(e) => setRewritten(e.target.value)}
                            />
                            <Button
                                type="primary"
                                style={{ marginTop: 16 }}
                                onClick={() => {
                                    navigator.clipboard.writeText(rewritten);
                                    message.success('Copied to clipboard!');
                                }}
                            >
                                Copy to Clipboard
                            </Button>
                        </Card>
                    )}

                    {!analysis && !rewritten && (
                        <Card>
                            <Alert
                                message="No Analysis Yet"
                                description={
                                    <>
                                        <p>Enter a job description on the left, then:</p>
                                        <ul>
                                            <li><strong>Analyze:</strong> Get detailed feedback and suggestions</li>
                                            <li><strong>Rewrite:</strong> Generate a complete improved version</li>
                                        </ul>
                                    </>
                                }
                                type="info"
                                showIcon
                            />
                        </Card>
                    )}
                </Col>
            </Row>
        </div>
    );
}

export default JDRewriting;

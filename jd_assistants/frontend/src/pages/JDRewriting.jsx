import React, { useState } from 'react';
import { Row, Col, Input, Button, Card, message, Alert, List, Tag, Spin } from 'antd';
import { BulbOutlined, EditOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { jdAIAPI } from '../services/api';
import { useLanguage } from '../contexts/LanguageContext';

const { TextArea } = Input;

function JDRewriting() {
    const { language, t } = useLanguage();
    const [inputJD, setInputJD] = useState('');
    const [analysis, setAnalysis] = useState(null);
    const [rewritten, setRewritten] = useState('');
    const [analyzing, setAnalyzing] = useState(false);
    const [rewriting, setRewriting] = useState(false);
    const [thinking, setThinking] = useState('');
    const [showThinking, setShowThinking] = useState(false);
    const [streamingProgress, setStreamingProgress] = useState('');

    const handleAnalyze = async () => {
        if (!inputJD.trim()) {
            message.warning(`${t('jdRewrite.pleaseEnterJD')} ${t('jdRewrite.analyze').toLowerCase()}`);
            return;
        }

        setAnalyzing(true);
        setThinking('');
        setStreamingProgress('');
        setShowThinking(true);
        setAnalysis(null);

        try {
            await jdAIAPI.analyzeStream(
                inputJD,
                language,
                // onProgress - thinking updates
                (progressData) => {
                    setStreamingProgress(progressData.accumulated || '');
                },
                // onFinal - complete analysis
                (finalData) => {
                    setAnalysis({
                        overall_score: finalData.overall_score,
                        key_recommendations: finalData.key_recommendations,
                        improvements: finalData.improvements
                    });
                    setThinking(finalData.thinking || 'No thinking process available');
                    setStreamingProgress('');
                    message.success(t('jdRewrite.analysisComplete'));
                },
                // onError
                (error) => {
                    console.error('Analysis error:', error);
                    message.error(`${t('jdRewrite.analysisFailed')}: ${error}`);
                    setStreamingProgress('');
                }
            );
        } catch (error) {
            console.error('Analysis exception:', error);
            message.error(error.response?.data?.detail || error.message || 'Failed to analyze JD');
        } finally {
            setAnalyzing(false);
        }
    };

    const handleRewrite = async () => {
        if (!inputJD.trim()) {
            message.warning(`${t('jdRewrite.pleaseEnterJD')} ${t('jdRewrite.rewrite').toLowerCase()}`);
            return;
        }

        setRewriting(true);
        setThinking('');
        setStreamingProgress('');
        setShowThinking(true);
        setRewritten('');

        try {
            await jdAIAPI.rewriteStream(
                inputJD,
                language,
                // onProgress - thinking updates
                (progressData) => {
                    setStreamingProgress(progressData.accumulated || '');
                },
                // onFinal - complete rewrite
                (finalData) => {
                    setRewritten(finalData.rewritten_jd);
                    setThinking(finalData.thinking || 'No thinking process available');
                    setStreamingProgress('');
                    message.success(t('jdRewrite.rewriteSuccess'));

                    // Show key changes if available
                    if (finalData.key_changes && finalData.key_changes.length > 0) {
                        message.info({
                            content: (
                                <div>
                                    <strong>{t('jdRewrite.keyChanges')}:</strong>
                                    <ul style={{ marginTop: 8, paddingLeft: 20 }}>
                                        {finalData.key_changes.map((change, idx) => (
                                            <li key={idx}>{change}</li>
                                        ))}
                                    </ul>
                                </div>
                            ),
                            duration: 8
                        });
                    }
                },
                // onError
                (error) => {
                    console.error('Rewrite error:', error);
                    message.error(`${t('jdRewrite.rewriteFailed')}: ${error}`);
                    setStreamingProgress('');
                }
            );
        } catch (error) {
            console.error('Rewrite exception:', error);
            message.error(error.response?.data?.detail || error.message || 'Failed to rewrite JD');
        } finally {
            setRewriting(false);
        }
    };

    return (
        <div>
            <div style={{ marginBottom: 16 }}>
                <h1>✍️ {t('jdRewrite.title')}</h1>
                <p style={{ color: '#666' }}>
                    {t('jdRewrite.subtitle')}
                </p>
            </div>

            {/* Thinking Process Panel */}
            {showThinking && (thinking || streamingProgress) && (
                <Card
                    style={{ marginBottom: 16, backgroundColor: '#f0f5ff' }}
                    title={
                        <span>
                            <ThunderboltOutlined style={{ marginRight: 8 }} />
                            {t('jdRewrite.aiThinking')}
                        </span>
                    }
                    extra={
                        <Button
                            size="small"
                            onClick={() => setShowThinking(false)}
                        >
                            {t('jdRewrite.hide')}
                        </Button>
                    }
                >
                    {streamingProgress ? (
                        <div>
                            <Spin style={{ marginRight: 8 }} />
                            <span style={{ fontStyle: 'italic', color: '#666' }}>
                                {t('jdRewrite.processing')}
                            </span>
                            <pre style={{
                                marginTop: 12,
                                padding: 12,
                                backgroundColor: '#fff',
                                borderRadius: 4,
                                maxHeight: 200,
                                overflow: 'auto',
                                whiteSpace: 'pre-wrap'
                            }}>
                                {streamingProgress}
                            </pre>
                        </div>
                    ) : thinking ? (
                        <div style={{
                            padding: 12,
                            backgroundColor: '#fff',
                            borderRadius: 4,
                            whiteSpace: 'pre-wrap'
                        }}>
                            {thinking}
                        </div>
                    ) : null}
                </Card>
            )}

            <Row gutter={16}>
                <Col span={12}>
                    <Card title={t('jdRewrite.originalJD')} extra={
                        <Button.Group>
                            <Button
                                type="primary"
                                icon={<BulbOutlined />}
                                onClick={handleAnalyze}
                                loading={analyzing}
                            >
                                {t('jdRewrite.analyze')}
                            </Button>
                            <Button
                                icon={<EditOutlined />}
                                onClick={handleRewrite}
                                loading={rewriting}
                            >
                                {t('jdRewrite.rewrite')}
                            </Button>
                        </Button.Group>
                    }>
                        <TextArea
                            rows={15}
                            placeholder={t('jdRewrite.placeholder')}
                            value={inputJD}
                            onChange={(e) => setInputJD(e.target.value)}
                        />
                    </Card>
                </Col>

                <Col span={12}>
                    {analysis && !rewritten && (
                        <Card title={`📊 ${t('jdRewrite.analysisResults')}`}>
                            <Alert
                                message={`${t('jdRewrite.overallScore')}: ${analysis.overall_score}/100`}
                                type={analysis.overall_score >= 70 ? 'success' : 'warning'}
                                showIcon
                                style={{ marginBottom: 16 }}
                            />

                            <h3>🎯 {t('jdRewrite.keyRecommendations')}:</h3>
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
                                    <h3>📝 {t('jdRewrite.suggestedImprovements')}:</h3>
                                    {analysis.improvements.map((imp, idx) => (
                                        <Card
                                            key={idx}
                                            size="small"
                                            style={{ marginBottom: 8 }}
                                            title={<Tag color="purple">{imp.section}</Tag>}
                                        >
                                            <p><strong>{t('jdRewrite.reason')}:</strong> {imp.reason}</p>
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
                        <Card title={`✨ ${t('jdRewrite.rewrittenJD')}`}>
                            <Alert
                                message={t('jdRewrite.aiGenerated')}
                                description={t('jdRewrite.reviewBeforePublish')}
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
                                    message.success(t('jdRewrite.copiedSuccess'));
                                }}
                            >
                                {t('jdRewrite.copyToClipboard')}
                            </Button>
                        </Card>
                    )}

                    {!analysis && !rewritten && (
                        <Card>
                            <Alert
                                message={t('jdRewrite.noAnalysis')}
                                description={
                                    <>
                                        <p>{t('jdRewrite.instructions')}</p>
                                        <ul>
                                            <li><strong>{t('jdRewrite.analyze')}:</strong> {t('jdRewrite.analyzeDesc')}</li>
                                            <li><strong>{t('jdRewrite.rewrite')}:</strong> {t('jdRewrite.rewriteDesc')}</li>
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

import React, { useState } from 'react';
import { Steps, Form, Input, InputNumber, Select, Button, Card, message, Progress, Alert, List, Tag, Divider } from 'antd';
import { RobotOutlined, FileTextOutlined, DollarOutlined } from '@ant-design/icons';
import { jdAIAPI } from '../services/api';
import { useLanguage } from '../contexts/LanguageContext';

const { TextArea } = Input;
const { Step } = Steps;

function JDGenerator() {
    const { language, t } = useLanguage();
    const [current, setCurrent] = useState(0);
    const [form] = Form.useForm();
    const [generatedJD, setGeneratedJD] = useState('');
    const [salaryAssessment, setSalaryAssessment] = useState(null);
    const [generating, setGenerating] = useState(false);
    const [assessing, setAssessing] = useState(false);

    const handleGenerate = async () => {
        try {
            const values = await form.validateFields();
            setGenerating(true);

            const response = await jdAIAPI.generate({
                position: values.position,
                experience_years: values.experience_years,
                required_skills: values.required_skills,
                salary_range: values.salary_range,
                job_type: values.job_type || 'Full-time',
                location: values.location || '',
                benefits: values.benefits || '',
                language: language  // Pass language to backend
            });

            setGeneratedJD(response.data.generated_jd);
            message.success('JD generated successfully!');
            setCurrent(1);

            // Auto-assess salary
            handleSalaryAssessment(values);
        } catch (error) {
            message.error(error.response?.data?.detail || 'Failed to generate JD');
        } finally {
            setGenerating(false);
        }
    };

    const handleSalaryAssessment = async (values) => {
        setAssessing(true);
        try {
            const response = await jdAIAPI.assessSalary({
                position: values.position,
                experience_years: values.experience_years,
                salary_offered: values.salary_range,
                location: values.location || 'Vietnam',
                required_skills: values.required_skills,
                language: language  // Pass language to backend
            });

            setSalaryAssessment(response.data);
        } catch (error) {
            message.warning('Salary assessment not available');
        } finally {
            setAssessing(false);
        }
    };

    const getAssessmentColor = (assessment) => {
        const colors = {
            'highly_competitive': 'green',
            'competitive': 'blue',
            'below_market': 'orange',
            'significantly_below': 'red'
        };
        return colors[assessment] || 'gray';
    };

    const getAssessmentText = (assessment) => {
        const texts = {
            'highly_competitive': 'Highly Competitive',
            'competitive': 'Market Rate',
            'below_market': 'Below Market',
            'significantly_below': 'Significantly Below Market'
        };
        return texts[assessment] || assessment;
    };

    const steps = [
        { title: 'Requirements', icon: <FileTextOutlined /> },
        { title: 'Generated JD', icon: <RobotOutlined /> },
    ];

    return (
        <div>
            <h1>🤖 {t('jdGen.title')}</h1>
            <p style={{ color: '#666', marginBottom: 24 }}>
                {t('jdGen.subtitle')}
            </p>

            <Steps current={current} items={steps} style={{ marginBottom: 32 }} />

            {current === 0 && (
                <Card title="Enter Job Requirements">
                    <Form form={form} layout="vertical">
                        <Form.Item
                            name="position"
                            label="Position Title"
                            rules={[{ required: true, message: 'Please enter position' }]}
                        >
                            <Input placeholder="e.g., Senior Backend Developer" size="large" />
                        </Form.Item>

                        <Form.Item
                            name="experience_years"
                            label="Years of Experience Required"
                            rules={[{ required: true, message: 'Please enter experience' }]}
                        >
                            <InputNumber min={0} max={30} style={{ width: '100%' }} size="large" />
                        </Form.Item>

                        <Form.Item
                            name="required_skills"
                            label="Required Skills (comma-separated)"
                            rules={[{ required: true, message: 'Please enter skills' }]}
                        >
                            <TextArea rows={3} placeholder="Python, FastAPI, PostgreSQL, Docker, AWS" />
                        </Form.Item>

                        <Form.Item
                            name="salary_range"
                            label="Salary Range"
                            rules={[{ required: true, message: 'Please enter salary range' }]}
                        >
                            <Input placeholder="$60,000 - $80,000 hoặc 1,500 - 2,000 USD" size="large" />
                        </Form.Item>

                        <Form.Item name="job_type" label="Job Type" initialValue="Full-time">
                            <Select>
                                <Select.Option value="Full-time">Full-time</Select.Option>
                                <Select.Option value="Part-time">Part-time</Select.Option>
                                <Select.Option value="Contract">Contract</Select.Option>
                                <Select.Option value="Internship">Internship</Select.Option>
                            </Select>
                        </Form.Item>

                        <Form.Item name="location" label="Location">
                            <Input placeholder="Ho Chi Minh City, Vietnam" />
                        </Form.Item>

                        <Form.Item name="benefits" label="Benefits (optional)">
                            <TextArea rows={3} placeholder="Health insurance, 13th month salary, annual bonus..." />
                        </Form.Item>

                        <Button
                            type="primary"
                            size="large"
                            icon={<RobotOutlined />}
                            onClick={handleGenerate}
                            loading={generating}
                            block
                        >
                            Generate Job Description with AI
                        </Button>
                    </Form>
                </Card>
            )}

            {current === 1 && (
                <div>
                    <Card title="📄 Generated Job Description" style={{ marginBottom: 16 }}>
                        <TextArea
                            rows={20}
                            value={generatedJD}
                            onChange={(e) => setGeneratedJD(e.target.value)}
                            style={{ fontFamily: 'monospace' }}
                        />
                        <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
                            <Button onClick={() => setCurrent(0)}>← Back to Edit</Button>
                            <Button
                                type="primary"
                                onClick={() => {
                                    navigator.clipboard.writeText(generatedJD);
                                    message.success('Copied to clipboard!');
                                }}
                            >
                                Copy JD
                            </Button>
                            <Button
                                onClick={async () => {
                                    try {
                                        const values = form.getFieldsValue();
                                        await handleGenerate();
                                    } catch (err) { }
                                }}
                                loading={generating}
                            >
                                🔄 Regenerate
                            </Button>
                        </div>
                    </Card>

                    {salaryAssessment && (
                        <Card
                            title={
                                <span>
                                    <DollarOutlined /> Salary Competitiveness Assessment
                                </span>
                            }
                            loading={assessing}
                        >
                            <Alert
                                message={
                                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                        <span>
                                            Assessment: <Tag color={getAssessmentColor(salaryAssessment.assessment)} style={{ fontSize: 14 }}>
                                                {getAssessmentText(salaryAssessment.assessment)}
                                            </Tag>
                                        </span>
                                        <span style={{ fontSize: 16, fontWeight: 'bold' }}>
                                            Market Range: {salaryAssessment.market_range}
                                        </span>
                                    </div>
                                }
                                type={salaryAssessment.score >= 70 ? 'success' : salaryAssessment.score >= 50 ? 'warning' : 'error'}
                                showIcon
                                style={{ marginBottom: 16 }}
                            />

                            <div style={{ marginBottom: 16 }}>
                                <h3>Competitiveness Score</h3>
                                <Progress
                                    percent={salaryAssessment.score}
                                    status={salaryAssessment.score >= 70 ? 'success' : 'exception'}
                                    strokeColor={
                                        salaryAssessment.score >= 90 ? '#52c41a' :
                                            salaryAssessment.score >= 70 ? '#1890ff' :
                                                salaryAssessment.score >= 50 ? '#faad14' : '#f5222d'
                                    }
                                />
                            </div>

                            <Divider />

                            <h3>💡 Key Insights</h3>
                            <p style={{ whiteSpace: 'pre-wrap' }}>{salaryAssessment.insights}</p>

                            <Divider />

                            <h3>📋 Recommendations</h3>
                            <List
                                dataSource={salaryAssessment.recommendations}
                                renderItem={item => (
                                    <List.Item>
                                        <Tag color="blue">→</Tag> {item}
                                    </List.Item>
                                )}
                            />
                        </Card>
                    )}
                </div>
            )}
        </div>
    );
}

export default JDGenerator;

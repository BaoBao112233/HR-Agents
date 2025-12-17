// Language Context for managing app language
import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
    const context = useContext(LanguageContext);
    if (!context) {
        throw new Error('useLanguage must be used within LanguageProvider');
    }
    return context;
};

// Translation dictionary
const translations = {
    en: {
        // Navigation
        'nav.dashboard': 'Dashboard',
        'nav.employees': 'Employees',
        'nav.departments': 'Departments',
        'nav.positions': 'Positions',
        'nav.recruitment': 'Recruitment',
        'nav.candidates': 'Candidates',
        'nav.jobDescriptions': 'Job Descriptions',
        'nav.jdGenerator': 'JD Generator',
        'nav.cvMatching': 'CV Matching',
        'nav.jdRewriting': 'JD Rewriting',
        'nav.logout': 'Logout',
        'nav.profile': 'Profile',

        // Common
        'common.loading': 'Loading...',
        'common.save': 'Save',
        'common.cancel': 'Cancel',
        'common.delete': 'Delete',
        'common.edit': 'Edit',
        'common.create': 'Create',
        'common.search': 'Search',
        'common.filter': 'Filter',
        'common.export': 'Export',
        'common.import': 'Import',
        'common.upload': 'Upload',
        'common.download': 'Download',
        'common.copy': 'Copy',
        'common.back': 'Back',
        'common.next': 'Next',
        'common.finish': 'Finish',
        'common.success': 'Success',
        'common.error': 'Error',
        'common.warning': 'Warning',

        // JD Generator
        'jdGen.title': 'AI Job Description Generator',
        'jdGen.subtitle': 'Create professional job descriptions from your requirements',
        'jdGen.position': 'Position Title',
        'jdGen.experience': 'Years of Experience Required',
        'jdGen.skills': 'Required Skills (comma-separated)',
        'jdGen.salary': 'Salary Range',
        'jdGen.jobType': 'Job Type',
        'jdGen.location': 'Location',
        'jdGen.benefits': 'Benefits (optional)',
        'jdGen.generate': 'Generate Job Description with AI',
        'jdGen.regenerate': 'Regenerate',
        'jdGen.copyJD': 'Copy JD',
        'jdGen.salaryAssessment': 'Salary Competitiveness Assessment',
        'jdGen.marketRange': 'Market Range',
        'jdGen.insights': 'Key Insights',
        'jdGen.recommendations': 'Recommendations',
        'jdGen.score': 'Competitiveness Score',

        // JD Rewriting
        'jdRewrite.title': 'AI-Powered JD Rewriting',
        'jdRewrite.subtitle': 'Use AI to analyze and improve your job descriptions with real-time thinking process',
        'jdRewrite.aiThinking': 'AI Thinking Process',
        'jdRewrite.hide': 'Hide',
        'jdRewrite.processing': 'Processing...',
        'jdRewrite.originalJD': 'Original Job Description',
        'jdRewrite.analyze': 'Analyze',
        'jdRewrite.rewrite': 'Rewrite',
        'jdRewrite.placeholder': 'Paste your job description here...',
        'jdRewrite.analysisResults': 'Analysis Results',
        'jdRewrite.overallScore': 'Overall Score',
        'jdRewrite.keyRecommendations': 'Key Recommendations',
        'jdRewrite.suggestedImprovements': 'Suggested Improvements',
        'jdRewrite.introduction': 'Introduction',
        'jdRewrite.reason': 'Reason',
        'jdRewrite.rewrittenJD': 'Rewritten Job Description',
        'jdRewrite.aiGenerated': 'AI-Generated Job Description',
        'jdRewrite.reviewBeforePublish': 'Review and edit as needed before publishing',
        'jdRewrite.copyToClipboard': 'Copy to Clipboard',
        'jdRewrite.copiedSuccess': 'Copied to clipboard!',
        'jdRewrite.noAnalysis': 'No Analysis Yet',
        'jdRewrite.instructions': 'Enter a job description on the left, then:',
        'jdRewrite.analyzeDesc': 'Analyze: Get detailed feedback and suggestions with AI thinking process',
        'jdRewrite.rewriteDesc': 'Rewrite: Generate a complete improved version with reasoning',
        'jdRewrite.keyChanges': 'Key Changes',
        'jdRewrite.pleaseEnterJD': 'Please enter a job description to',
        'jdRewrite.analysisComplete': 'Analysis complete!',
        'jdRewrite.rewriteSuccess': 'JD rewritten successfully!',
        'jdRewrite.analysisFailed': 'Failed to analyze',
        'jdRewrite.rewriteFailed': 'Failed to rewrite',
    },
    vi: {
        // Navigation
        'nav.dashboard': 'Tổng quan',
        'nav.employees': 'Nhân viên',
        'nav.departments': 'Phòng ban',
        'nav.positions': 'Vị trí',
        'nav.recruitment': 'Tuyển dụng',
        'nav.candidates': 'Ứng viên',
        'nav.jobDescriptions': 'Mô tả công việc',
        'nav.jdGenerator': 'Tạo JD bằng AI',
        'nav.cvMatching': 'Đánh giá CV',
        'nav.jdRewriting': 'Viết lại JD',
        'nav.logout': 'Đăng xuất',
        'nav.profile': 'Hồ sơ',

        // Common
        'common.loading': 'Đang tải...',
        'common.save': 'Lưu',
        'common.cancel': 'Hủy',
        'common.delete': 'Xóa',
        'common.edit': 'Sửa',
        'common.create': 'Tạo mới',
        'common.search': 'Tìm kiếm',
        'common.filter': 'Lọc',
        'common.export': 'Xuất',
        'common.import': 'Nhập',
        'common.upload': 'Tải lên',
        'common.download': 'Tải xuống',
        'common.copy': 'Sao chép',
        'common.back': 'Quay lại',
        'common.next': 'Tiếp',
        'common.finish': 'Hoàn tất',
        'common.success': 'Thành công',
        'common.error': 'Lỗi',
        'common.warning': 'Cảnh báo',

        // JD Generator
        'jdGen.title': 'Tạo Mô Tả Công Việc bằng AI',
        'jdGen.subtitle': 'Tạo mô tả công việc chuyên nghiệp từ yêu cầu của bạn',
        'jdGen.position': 'Tên vị trí',
        'jdGen.experience': 'Số năm kinh nghiệm yêu cầu',
        'jdGen.skills': 'Kỹ năng yêu cầu (phân cách bằng dấu phẩy)',
        'jdGen.salary': 'Mức lương',
        'jdGen.jobType': 'Loại công việc',
        'jdGen.location': 'Địa điểm',
        'jdGen.benefits': 'Phúc lợi (tùy chọn)',
        'jdGen.generate': 'Tạo Mô Tả Công Việc bằng AI',
        'jdGen.regenerate': 'Tạo lại',
        'jdGen.copyJD': 'Sao chép JD',
        'jdGen.salaryAssessment': 'Đánh Giá Mức Lương',
        'jdGen.marketRange': 'Mức lương thị trường',
        'jdGen.insights': 'Phân Tích Chính',
        'jdGen.recommendations': 'Đề Xuất',
        'jdGen.score': 'Điểm Cạnh Tranh',

        // JD Rewriting
        'jdRewrite.title': 'Viết Lại JD bằng AI',
        'jdRewrite.subtitle': 'Sử dụng AI để phân tích và cải thiện mô tả công việc của bạn với quy trình suy nghĩ thời gian thực',
        'jdRewrite.aiThinking': 'Quy Trình Suy Nghĩ của AI',
        'jdRewrite.hide': 'Ẩn',
        'jdRewrite.processing': 'Đang xử lý...',
        'jdRewrite.originalJD': 'Mô Tả Công Việc Gốc',
        'jdRewrite.analyze': 'Phân Tích',
        'jdRewrite.rewrite': 'Viết Lại',
        'jdRewrite.placeholder': 'Dán mô tả công việc của bạn vào đây...',
        'jdRewrite.analysisResults': 'Kết Quả Phân Tích',
        'jdRewrite.overallScore': 'Điểm Tổng Thể',
        'jdRewrite.keyRecommendations': 'Các Khuyến Nghị Chính',
        'jdRewrite.suggestedImprovements': 'Các Cải Tiến Đề Xuất',
        'jdRewrite.introduction': 'Giới Thiệu',
        'jdRewrite.reason': 'Lý Do',
        'jdRewrite.rewrittenJD': 'Mô Tả Công Việc Đã Viết Lại',
        'jdRewrite.aiGenerated': 'Mô Tả Công Việc Được Tạo Bởi AI',
        'jdRewrite.reviewBeforePublish': 'Xem lại và chỉnh sửa nếu cần trước khi xuất bản',
        'jdRewrite.copyToClipboard': 'Sao Chép',
        'jdRewrite.copiedSuccess': 'Đã sao chép!',
        'jdRewrite.noAnalysis': 'Chưa Có Phân Tích',
        'jdRewrite.instructions': 'Nhập mô tả công việc bên trái, sau đó:',
        'jdRewrite.analyzeDesc': 'Phân Tích: Nhận phản hồi chi tiết và đề xuất với quy trình suy nghĩ AI',
        'jdRewrite.rewriteDesc': 'Viết Lại: Tạo phiên bản cải tiến hoàn chỉnh với lý do',
        'jdRewrite.keyChanges': 'Các Thay Đổi Chính',
        'jdRewrite.pleaseEnterJD': 'Vui lòng nhập mô tả công việc để',
        'jdRewrite.analysisComplete': 'Phân tích hoàn tất!',
        'jdRewrite.rewriteSuccess': 'Viết lại JD thành công!',
        'jdRewrite.analysisFailed': 'Phân tích thất bại',
        'jdRewrite.rewriteFailed': 'Viết lại thất bại',
    }
};

export const LanguageProvider = ({ children }) => {
    const [language, setLanguage] = useState(() => {
        return localStorage.getItem('app_language') || 'en';
    });

    useEffect(() => {
        localStorage.setItem('app_language', language);
    }, [language]);

    const t = (key) => {
        return translations[language][key] || key;
    };

    const toggleLanguage = () => {
        setLanguage(prev => prev === 'en' ? 'vi' : 'en');
    };

    const value = {
        language,
        setLanguage,
        t,
        toggleLanguage
    };

    return (
        <LanguageContext.Provider value={value}>
            {children}
        </LanguageContext.Provider>
    );
};

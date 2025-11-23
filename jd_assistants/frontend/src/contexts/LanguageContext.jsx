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

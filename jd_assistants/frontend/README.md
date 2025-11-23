# React Frontend - HR Management System

Modern React-based frontend for the HR Management System.

## Setup

```bash
cd frontend
npm install
npm run dev
```

The app will run on http://localhost:3000

## Features

- **Authentication**: Login with email/password
- **Dashboard**: Overview of employees, departments, positions
- **Employee Management**: Create, view, edit employees
- **Department Management**: Manage company departments
- **Position Management**: Manage job positions

## Tech Stack

- React 18
- Ant Design 5
- React Router v6
- Axios for API calls
- Vite for bundling

## Default Login

To create the first admin user, use the API directly:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"admin123","role":"admin"}'
```

Then login with:
- Email: admin@company.com
- Password: admin123

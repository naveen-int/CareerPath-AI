# CareerPath-AI
AI-Enhanced Career Guidance System for Personalized Career Pathways

---

## Problem Statement

Students often face difficulty in choosing the right course, domain, or career path due to a lack of proper guidance. This project provides personalized career recommendations, skill gap analysis, and internship suggestions based on user skills and interests.

---

## Objectives

- Guide school students in choosing suitable courses and streams.
- Help college students identify suitable domains and job roles.
- Recommend careers based on skills and interests.
- Identify missing skills for a target career.
- Suggest suitable internships and career opportunities.

---

## Users

- School Students
- College Students

## Modules

### 1. Login & Registration

Allows users to create an account and securely log in to the system.

### 2. School Student Guidance

Recommends suitable streams, courses, and career paths based on student interests and academic preferences.

### 3. College Student Guidance

Suggests suitable domains and job roles based on skills, technologies, certifications, and interests.

### 4. Missing Skill Detection

Identifies the skills required for a target role and compares them with the user's current skills.

### 5. Internship Recommendation

Suggests suitable internship opportunities based on the user's domain and skill set.

### 6. Trending Domains & Skills

Displays current trending career domains and the skills required for each domain.

---

# Features

* User Login & Registration
* School Student Guidance
* College Student Guidance
* Skill Gap Detection
* Role Match Score Analysis
* Internship Recommendation
* Career Domain Recommendation
* Personalized Career Suggestions


---


# Workflow

```
CareerPath AI

│

├── User Module

│   ├── Login / Register

│   ├── Select User Type

│   ├── View Career Recommendations

│   ├── View Skill Gap Analysis

│   └── View Internship Recommendations

│

├── School Guidance Module

│   ├── Enter Interests

│   ├── Enter Favorite Subjects

│   └── View Recommended Stream

│

├── College Guidance Module

│   ├── Enter Skills

│   ├── Enter Technologies

│   ├── Enter Certifications

│   ├── View Recommended Domain

│   └── View Recommended Role

│

├── Skill Gap Module

│   ├── Select Target Role

│   ├── Analyze Current Skills

│   └── View Missing Skills

│

└── Internship Module


├── View Internship Opportunities

├── View Required Skills

└── Apply Career Recommendations
```

---

# Database Requirement Analysis

The system requires a database to store user information, academic interests, skills, career recommendations, skill gap analysis, and internship details.

---

# Database Tables

## Users
```

| Field Name | Data Type    |
| ---------- | ------------ |
| name       | VARCHAR(100) |
| email      | VARCHAR(100) |
| password   | VARCHAR(100) |
| user_type  | VARCHAR(20)  |

## School Guidance

| Field Name         | Data Type    |
| ------------------ | ------------ |
| interests          | VARCHAR(200) |
| favorite_subjects  | VARCHAR(200) |
| recommended_stream | VARCHAR(100) |

## College Guidance

| Field Name         | Data Type    |
| ------------------ | ------------ |
| skills             | VARCHAR(200) |
| technologies       | VARCHAR(200) |
| certifications     | VARCHAR(200) |
| recommended_domain | VARCHAR(100) |
| recommended_role   | VARCHAR(100) |

## Skill Gap

| Field Name     | Data Type    |
| -------------- | ------------ |
| target_role    | VARCHAR(100) |
| current_skills | VARCHAR(200) |
| missing_skills | VARCHAR(200) |

## Internship

| Field Name      | Data Type    |
| --------------- | ------------ |
| internship_name | VARCHAR(150) |
| domain          | VARCHAR(100) |
| required_skill  | VARCHAR(150) |

```

---

from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3
import pandas as pd

# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)
CORS(app)

DATABASE = "careerpath.db"

# ==========================================
# Database Connection
# ==========================================

def get_connection():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# Create User Table
# ==========================================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )

    """)

    conn.commit()

    conn.close()


create_tables()

# ==========================================
# Load CSV Files
# ==========================================

school_df = pd.read_csv("school_guidance.csv")

college_df = pd.read_csv("college_guidance.csv")

skill_df = pd.read_csv("skill_gap.csv")

role_df = pd.read_csv("role_match.csv")

internship_df = pd.read_csv("internship.csv")

print("\nDatasets Loaded Successfully")

print("School Dataset      :", len(school_df))
print("College Dataset     :", len(college_df))
print("Skill Gap Dataset   :", len(skill_df))
print("Role Match Dataset  :", len(role_df))
print("Internship Dataset  :", len(internship_df))

# ==========================================
# Helper Functions
# ==========================================

def clean(text):

    return str(text).strip().lower()


def split_skills(skill_text):

    return [

        x.strip().lower()

        for x in str(skill_text).split(",")

    ]


# ==========================================
# Home API
# ==========================================

@app.route("/")

def home():

    return jsonify({

        "status": "Running",

        "project": "CareerPath AI",

        "backend": "Flask",

        "recommendation": "Rule Based"

    })


# ==========================================
# Register API
# ==========================================

@app.route("/register", methods=["POST"])

def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    if user:

        conn.close()

        return jsonify({

            "success": False,

            "message": "Email already exists"

        })

    cursor.execute("""

    INSERT INTO users

    (name,email,password)

    VALUES

    (?,?,?)

    """, (name, email, password))

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message": "Registration Successful"

    })


# ==========================================
# Login API
# ==========================================

@app.route("/login", methods=["POST"])

def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM users

        WHERE email=? AND password=?

        """,

        (email, password)

    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return jsonify({

            "success": True,

            "message": "Login Successful",

            "user": dict(user)

        })

    return jsonify({

        "success": False,

        "message": "Invalid Email or Password"

    })


# ==========================================
# School Guidance API
# ==========================================

@app.route("/school-guidance", methods=["POST"])

def school_guidance():

    try:

        data = request.get_json()

        interest = data.get("interest")

        subject = data.get("subject")

        result = school_df[

            (school_df["Interest"] == interest)

            &

            (school_df["Favourite_Subject"] == subject)

        ]

        if result.empty:

            return jsonify({

                "success": False,

                "message": "No recommendation found."

            })

        row = result.iloc[0]

        return jsonify({

            "success": True,

            "interest": row["Interest"],

            "favourite_subject": row["Favourite_Subject"],

            "recommended_stream": row["Recommended_Stream"],

            "recommended_course": row["Recommended_Course"],

            "career_path": row["Career_Path"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ==========================================
# College Guidance API
# ==========================================

@app.route("/college-guidance", methods=["POST"])

def college_guidance():

    try:

        data = request.get_json()

        skill = data.get("skill")

        technology = data.get("technology")

        certification = data.get("certification")

        result = college_df[

            (college_df["Skills"] == skill)

            &

            (college_df["Technologies"] == technology)

            &

            (college_df["Certifications"] == certification)

        ]

        if result.empty:

            return jsonify({

                "success": False,

                "message": "No recommendation found."

            })

        row = result.iloc[0]

        return jsonify({

            "success": True,

            "skills": row["Skills"],

            "technology": row["Technologies"],

            "certification": row["Certifications"],

            "recommended_domain": row["Recommended_Domain"],

            "recommended_role": row["Recommended_Role"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# ==========================================
# Skill Gap API
# ==========================================

@app.route("/skill-gap", methods=["POST"])

def skill_gap():

    try:

        data = request.get_json()

        target_role = clean(data.get("target_role"))

        current_skills = split_skills(

            data.get("current_skills")

        )

        result = skill_df[

            skill_df["Target_Role"]

            .str.lower()

            .str.strip()

            == target_role

        ]

        if result.empty:

            return jsonify({

                "success": False,

                "message": "Target role not found."

            })

        row = result.iloc[0]

        required_skills = split_skills(

            row["Required_Skills"]

        )

        matched_skills = []

        missing_skills = []

        for skill in required_skills:

            if skill in current_skills:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

        return jsonify({

            "success": True,

            "target_role": row["Target_Role"],

            "required_skills": required_skills,

            "current_skills": current_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "recommended_course": row["Recommended_Course"],

            "learning_resource": row["Learning_Resource"],

            "career_level": row["Career_Level"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# ==========================================
# Role Match API
# ==========================================

@app.route("/role-match", methods=["POST"])

def role_match():

    try:

        data = request.get_json()

        target_role = clean(data.get("target_role"))

        current_skills = split_skills(
            data.get("current_skills")
        )

        result = role_df[

            role_df["Target_Role"]

            .str.lower()

            .str.strip()

            == target_role

        ]

        if result.empty:

            return jsonify({

                "success": False,

                "message": "Role not found."

            })

        row = result.iloc[0]

        required_skills = split_skills(
            row["Required_Skills"]
        )

        matched_skills = []

        missing_skills = []

        for skill in required_skills:

            if skill in current_skills:

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

        total = len(required_skills)

        matched = len(matched_skills)

        percentage = 0

        if total > 0:

            percentage = round((matched / total) * 100)

        if percentage >= 90:

            status = "Excellent"

        elif percentage >= 70:

            status = "Good"

        elif percentage >= 50:

            status = "Average"

        else:

            status = "Needs Improvement"

        return jsonify({

            "success": True,

            "target_role": row["Target_Role"],

            "required_skills": required_skills,

            "current_skills": current_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_percentage": percentage,

            "status": status,

            "preferred_technology": row["Preferred_Technologies"],

            "recommended_certification": row["Recommended_Certification"],

            "career_level": row["Career_Level"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# ==========================================
# Internship Recommendation API
# ==========================================

@app.route("/internship", methods=["POST"])

def internship():

    try:

        data = request.get_json()

        domain = clean(data.get("domain"))

        skills = split_skills(
            data.get("skills")
        )

        result = internship_df[

            internship_df["Domain"]

            .str.lower()

            .str.strip()

            == domain

        ]

        if result.empty:

            return jsonify({

                "success": False,

                "message": "No internship found."

            })

        recommendations = []

        for _, row in result.iterrows():

            required_skills = split_skills(
                row["Required_Skills"]
            )

            matched = 0

            for skill in required_skills:

                if skill in skills:

                    matched += 1

            percentage = round(

                (matched / len(required_skills)) * 100

            )

            recommendations.append({

                "internship_id": row["Internship_ID"],

                "internship_name": row["Internship_Name"],

                "domain": row["Domain"],

                "required_skills": required_skills,

                "match_percentage": percentage,

                "duration": row["Duration"],

                "mode": row["Mode"],

                "stipend": row["Stipend"],

                "recommended_role": row["Recommended_Role"]

            })

        recommendations.sort(

            key=lambda x: x["match_percentage"],

            reverse=True

        )

        return jsonify({

            "success": True,

            "total_recommendations": len(recommendations),

            "recommendations": recommendations[:5]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })
    
# ==========================================
# Run Flask Application
# ==========================================

if __name__ == "__main__":

    print("\n====================================")

    print(" CareerPath AI Backend Started")

    print(" Recommendation System : Rule Based")

    print(" Backend URL : http://127.0.0.1:5000")

    print("====================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )    
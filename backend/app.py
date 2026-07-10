# ==========================================
# CareerPath AI
# Backend Application
# ==========================================

from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sqlite3
import pandas as pd
import joblib

# ==========================================
# Flask App Configuration
# ==========================================

app = Flask(__name__)

CORS(app)

DATABASE = "careerpath.db"

# ==========================================
# Load Machine Learning Models
# ==========================================

school_model = joblib.load(
    "models/school_model.pkl"
)

school_encoders = joblib.load(
    "models/school_encoders.pkl"
)

college_model = joblib.load(
    "models/college_model.pkl"
)

college_encoders = joblib.load(
    "models/college_encoders.pkl"
)

# ==========================================
# Load Datasets
# ==========================================

school_df = pd.read_csv(
    "school_guidance.csv"
)

college_df = pd.read_csv(
    "college_guidance.csv"
)

print("\nDatasets Loaded Successfully\n")

print(
    "School Dataset :",
    len(school_df)
)

print(
    "College Dataset :",
    len(college_df)
)

# ==========================================
# Database Connection
# ==========================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# Create User Table
# ==========================================

def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )

    """)

    connection.commit()

    connection.close()


create_tables()

# ==========================================
# Helper Functions
# ==========================================

def clean(text):

    return str(text).strip()


def split_skills(skill_text):

    return [

        skill.strip().lower()

        for skill in str(skill_text).split(",")

    ]


# ==========================================
# Rule-Based Knowledge Base
# Skill Gap Expert System
# ==========================================

ROLE_RULES = {

    "Machine Learning Engineer": {

        "required_skills": [

            "Python",

            "Machine Learning",

            "Pandas",

            "NumPy"

        ],

        "recommended_course":
        "Machine Learning with Python",

        "learning_resource":
        "Coursera",

        "career_level":
        "Intermediate"

    },

    "Data Scientist": {

        "required_skills": [

            "Python",

            "Machine Learning",

            "Pandas",

            "NumPy",

            "SQL"

        ],

        "recommended_course":
        "Data Science",

        "learning_resource":
        "Coursera",

        "career_level":
        "Intermediate"

    },

    "Data Analyst": {

        "required_skills": [

            "Python",

            "SQL",

            "Pandas",

            "NumPy"

        ],

        "recommended_course":
        "Google Data Analytics",

        "learning_resource":
        "Coursera",

        "career_level":
        "Beginner"

    },

    "Full Stack Developer": {

        "required_skills": [

            "HTML",

            "CSS",

            "JavaScript",

            "React",

            "Node.js",

            "MongoDB"

        ],

        "recommended_course":
        "Full Stack Web Development",

        "learning_resource":
        "freeCodeCamp",

        "career_level":
        "Beginner"

    },

    "Cyber Security Analyst": {

        "required_skills": [

            "Networking",

            "Cyber Security"

        ],

        "recommended_course":
        "Cyber Security Fundamentals",

        "learning_resource":
        "Cisco Networking Academy",

        "career_level":
        "Intermediate"

    },

    "Cloud Engineer": {

        "required_skills": [

            "Cloud Computing",

            "AWS",

            "Docker",

            "Networking"

        ],

        "recommended_course":
        "Cloud Computing",

        "learning_resource":
        "AWS Skill Builder",

        "career_level":
        "Intermediate"

    },

    "UI/UX Designer": {

        "required_skills": [

            "UI/UX Design",

            "Figma",

            "HTML",

            "CSS"

        ],

        "recommended_course":
        "UI/UX Design",

        "learning_resource":
        "Google UX Design",

        "career_level":
        "Beginner"

    },

    "Software Engineer": {

        "required_skills": [

            "Java",

            "Python",

            "SQL",

            "JavaScript"

        ],

        "recommended_course":
        "Software Engineering",

        "learning_resource":
        "Coursera",

        "career_level":
        "Beginner"

    }

}

# ==========================================
# Home API
# ==========================================

@app.route("/")

def home():

    return jsonify({

        "message":
        "CareerPath AI Backend Running Successfully"

    })

# ==========================================
# Register API
# ==========================================

@app.route("/register", methods=["POST"])

def register():

    try:

        data = request.get_json()

        name = clean(data.get("name"))

        email = clean(data.get("email"))

        password = clean(data.get("password"))

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            "SELECT * FROM users WHERE email=?",

            (email,)

        )

        user = cursor.fetchone()

        if user:

            connection.close()

            return jsonify({

                "success": False,

                "message": "Email already exists."

            })

        cursor.execute(

            """

            INSERT INTO users

            (name, email, password)

            VALUES

            (?, ?, ?)

            """,

            (

                name,

                email,

                password

            )

        )

        connection.commit()

        connection.close()

        return jsonify({

            "success": True,

            "message": "Registration Successful"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# ==========================================
# Login API
# ==========================================

@app.route("/login", methods=["POST"])

def login():

    try:

        data = request.get_json()

        email = clean(data.get("email"))

        password = clean(data.get("password"))

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

            """

            SELECT *

            FROM users

            WHERE email=? AND password=?

            """,

            (

                email,

                password

            )

        )

        user = cursor.fetchone()

        connection.close()

        if user:

            return jsonify({

                "success": True,

                "message": "Login Successful",

                "user": {

                    "id": user["id"],

                    "name": user["name"],

                    "email": user["email"]

                }

            })

        return jsonify({

            "success": False,

            "message": "Invalid Email or Password"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })
    
# ==========================================
# School Guidance API (Random Forest)
# ==========================================

@app.route("/school-guidance", methods=["POST"])

def school_guidance():

    try:

        data = request.get_json()

        interest = clean(
            data.get("interest")
        )

        subject = clean(
            data.get("subject")
        )

        activity = clean(
            data.get("preferred_activity")
        )

        # ==================================
        # Encode User Input
        # ==================================

        interest_value = school_encoders[
            "interest_encoder"
        ].transform([interest])[0]

        subject_value = school_encoders[
            "subject_encoder"
        ].transform([subject])[0]

        activity_value = school_encoders[
            "activity_encoder"
        ].transform([activity])[0]

        # ==================================
        # Predict Recommended Stream
        # ==================================

        prediction = school_model.predict([

            [

                interest_value,

                subject_value,

                activity_value

            ]

        ])

        predicted_stream = school_encoders[

            "stream_encoder"

        ].inverse_transform(

            prediction

        )[0]

        # ==================================
        # Search Matching Record
        # ==================================

        result = school_df[

            (school_df["Interest"] == interest)

            &

            (school_df["Favourite_Subject"] == subject)

            &

            (school_df["Preferred_Activity"] == activity)

            &

            (school_df["Recommended_Stream"] == predicted_stream)

        ]

        if result.empty:

            return jsonify({

                "success": False,

                "message":
                "No recommendation found."

            })

        row = result.iloc[0]

        # ==================================
        # Return Response
        # ==================================

        return jsonify({

            "success": True,

            "interest":
            row["Interest"],

            "favourite_subject":
            row["Favourite_Subject"],

            "preferred_activity":
            row["Preferred_Activity"],

            "recommended_stream":
            row["Recommended_Stream"],

            "recommended_course":
            row["Recommended_Course"],

            "career_path":
            row["Career_Path"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
            str(e)

        })
    
# ==========================================
# College Guidance API (Random Forest)
# ==========================================

@app.route("/college-guidance", methods=["POST"])

def college_guidance():

    try:

        data = request.get_json()

        skill = clean(
            data.get("skill")
        )

        technology = clean(
            data.get("technology")
        )

        certification = clean(
            data.get("certification")
        )

        preferred_work = clean(
            data.get("preferred_work")
        )

        # ==================================
        # Encode User Input
        # ==================================

        skill_value = college_encoders[
            "skills_encoder"
        ].transform([skill])[0]

        technology_value = college_encoders[
            "technology_encoder"
        ].transform([technology])[0]

        certification_value = college_encoders[
            "certification_encoder"
        ].transform([certification])[0]

        preferred_work_value = college_encoders[
            "work_encoder"
        ].transform([preferred_work])[0]

        # ==================================
        # Predict Domain
        # ==================================

        prediction = college_model.predict([

            [

                skill_value,

                technology_value,

                certification_value,

                preferred_work_value

            ]

        ])

        predicted_domain = college_encoders[

            "domain_encoder"

        ].inverse_transform(

            prediction

        )[0]

        # ==================================
        # Search Matching Record
        # ==================================

        result = college_df[

            (college_df["Skills"] == skill)

            &

            (college_df["Technologies"] == technology)

            &

            (college_df["Certification"] == certification)

            &

            (college_df["Preferred_Work"] == preferred_work)

            &

            (college_df["Recommended_Domain"] == predicted_domain)

        ]

        # If exact combination is unavailable,
        # search using predicted domain

        if result.empty:

            result = college_df[

                college_df["Recommended_Domain"]

                == predicted_domain

            ]

        if result.empty:

            return jsonify({

                "success": False,

                "message":
                "No recommendation found."

            })

        row = result.iloc[0]

        # ==================================
        # Return Response
        # ==================================

        return jsonify({

            "success": True,

            "skill":
            row["Skills"],

            "technology":
            row["Technologies"],

            "certification":
            row["Certification"],

            "preferred_work":
            row["Preferred_Work"],

            "recommended_domain":
            row["Recommended_Domain"],

            "recommended_role":
            row["Recommended_Role"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })
# ==========================================
# Skill Gap API (Rule-Based Expert System)
# ==========================================

@app.route("/skill-gap", methods=["POST"])

def skill_gap():

    try:

        data = request.get_json()

        target_role = clean(
            data.get("target_role")
        )

        current_skills = split_skills(

            data.get("current_skills")

        )

        # ==================================
        # Check Target Role
        # ==================================

        if target_role not in ROLE_RULES:

            return jsonify({

                "success": False,

                "message":
                "Target role not found."

            })

        rule = ROLE_RULES[target_role]

        required_skills = [

            skill.lower()

            for skill in

            rule["required_skills"]

        ]

        # ==================================
        # Compare Skills
        # ==================================

        matched_skills = []

        missing_skills = []

        for skill in required_skills:

            if skill in current_skills:

                matched_skills.append(

                    skill.title()

                )

            else:

                missing_skills.append(

                    skill.title()

                )

        # ==================================
        # Return Response
        # ==================================

        return jsonify({

            "success": True,

            "target_role":
            target_role,

            "required_skills":

            rule["required_skills"],

            "current_skills":

            [

                skill.title()

                for skill in current_skills

            ],

            "matched_skills":

            matched_skills,

            "missing_skills":

            missing_skills,

            "recommended_course":

            rule["recommended_course"],

            "learning_resource":

            rule["learning_resource"],

            "career_level":

            rule["career_level"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
            str(e)

        })


# ==========================================
# Run Application
# ==========================================



if __name__ == "__main__":

    print("\n====================================")

    print(" CareerPath AI Backend Started")

    print(" School Guidance : Random Forest")

    print(" College Guidance : Random Forest")

    print(" Skill Gap : Rule Based Expert System")

    print("====================================\n")

    port = int(os.environ.get("PORT", 5000))

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )

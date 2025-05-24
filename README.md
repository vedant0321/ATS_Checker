# 📘 Academic Fit: AI-Powered Resume Analysis and Job Match Visualizer

**Bridging the Gap Between Academia and Industry with AI**

Academic Fit is an AI-powered platform designed to enhance employability by aligning student resumes with job market demands. Built using cutting-edge Natural Language Processing (NLP) and Large Language Models (LLMs), Academic Fit helps both students and academic institutions understand skill gaps, improve resumes, and make data-driven decisions for better placement outcomes.

---

## 🚀 Features

### 🎓 For Students:
- **Resume Analysis**: Extracts and analyzes resume content using NLP techniques.
- **Job Description Matching**: Compares uploaded resumes with job descriptions.
- **Skill Gap Identification**: Highlights missing skills based on job requirements.
- **Resume Enhancement Suggestions**: Recommends certifications and improvements.
- **ATS Score Evaluation**: Rates resume compatibility with industry ATS systems.

### 🏢 For Academic Institutions:
- **Bulk Resume Upload**: Analyze multiple resumes simultaneously.
- **Attribute-Based Filtering**: Filter students by skills, academic performance, etc.
- **Skill Gap Visualization**: Identify common training needs across the student body.
- **Interactive Dashboard**: Visual summaries and analytics for better guidance.

---

## 🧠 Technologies Used

| Component | Technology |
|----------|------------|
| NLP & Embedding | SpaCy, Transformers, Sentence-BERT |
| Backend | Python |
| Frontend | Streamlit |
| Visualization | Plotly / Matplotlib / Dashboards |
| Model Evaluation | BLEU, ROUGE Scores |
| Authentication | Fire-Base |

---
## Install

1. Clone this repository.

```shell
git clone https://github.com/vedant0321/ATS_Checker
```
2. Install packages.

```shell
conda create -n afit python=3.10
conda activate afit
pip install -r requirements.txt
```
4. Create a .env file in the root directory
This file should include the following keys and values:
```shell
API_KEY=your_api_key
AUTH_DOMAIN=your_auth_domain
DATABASE_URL=your_database_url
PROJECT_ID=your_project_id
STORAGE_BUCKET=your_storage_bucket
APP_ID=your_app_id
MEASUREMENT_ID=your_measurement_id
GEMINI_API_KEY=your_gemini_api_key
```
5. Add Firebase Service Account Key
Place the Firebase service account key file in the following path:
```shell
etc/secret/service_account_key.json
```
6. Run the application
```shell
streamlit run main.py

```

## 🏗️ System Architecture
![System Architecture](https://github.com/vedant0321/ATS_Checker/blob/main/arch.png)



## LICENSE
![License ](https://github.com/vedant0321/ATS_Checker/blob/main/LICENSE)
Our code is released under the MIT License. Our model is intended for academic research purposes only and may **NOT** be used for commercial purposes.

You are free to use, modify, and distribute this model in academic settings, provided that the following condition should met:

- **Non-commercial use**: The model may not be used for any commercial purposes.

### Commercial Use Restriction

For any commercial use inquiries or to obtain a commercial license, please contact <code>vedantbirewar8@gmail.com</code>.

# Cover Letter & Resume Optimizer

This is a Python-based GUI application that helps job seekers tailor their resumes and cover letters for specific job descriptions. The application extracts text from resumes, modifies them to align with job postings, and generates personalized cover letters using AI.

**Features**

Resume Optimization: Adjusts the resume content to highlight relevant skills and experience.

Cover Letter Generation: Creates a tailored cover letter based on the job description and updated resume.

Supports Multiple File Formats: Works with PDF, DOCX, DOC, and TXT files.

Clipboard Copying: Quickly copy the generated cover letter and resume text for further formatting.

User-Friendly GUI: Built with Tkinter for ease of use.

**Requirements**

Ensure you have the following dependencies installed:

`pip install tkinter ollama PyPDF2 docx2txt`

**Usage**

Run the script:

`python cover_letter_generator.py`

Select your resume by clicking the "Browse" button.

Paste the job description into the provided text box.

Click "Generate Cover Letter & Resume."

Copy the modified resume and cover letter for further formatting or saving as a document.

**Notes**

This program modifies the resume text but does not save it automatically. You will need to copy and paste the modified text into a document editor.

The cover letter and resume are generated using the llama3 model in Ollama.

Ensure you have an internet connection for AI processing.

**License**

This project is licensed under the MIT License.

**Author**

Developed by Robert Pickett

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import ollama
import PyPDF2
import docx2txt
import subprocess


def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = '\n'.join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    elif file_path.lower().endswith(('.docx', '.doc')):
        return docx2txt.process(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


def modify_resume_for_job(resume_text, job_description):
    prompt = f"""You are a professional resume writer. Modify the following resume to better fit the provided job description while keeping it truthful. 
    Ensure that:
    - Key skills and experiences from the resume that match the job are highlighted.
    - Keywords from the job description are naturally integrated.
    - The structure remains professional and ATS-friendly.

    Job Description:
    {job_description}

    Original Resume:
    {resume_text}

    Please return the updated resume text.
    """
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']


def generate_cover_letter():
    result_text.delete(1.0, tk.END)
    resume_path = resume_entry.get()
    job_description = job_desc_text.get("1.0", tk.END).strip()

    try:
        resume_content = extract_text_from_file(resume_path)

        # Modify the resume to match the job
        updated_resume = modify_resume_for_job(resume_content, job_description)

        # Generate the cover letter
        cover_letter_prompt = f"""You are an experienced HR professional creating a tailored cover letter. 
        Ensure that:
        - The letter is concise (under 2kb)
        - It directly addresses the job requirements
        - Achievements and quantifiable results from the resume are included
        - It expresses enthusiasm for the role and company

        Job Description:
        {job_description}

        Updated Resume:
        {updated_resume}

        Generate a compelling cover letter.
        """
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': cover_letter_prompt}]
        )
        generated_cover_letter = response['message']['content']

        # Display the updated resume and cover letter
        result_text.insert(tk.END, "Updated Resume:\n" + updated_resume + "\n\n")
        result_text.insert(tk.END, "Generated Cover Letter:\n" + generated_cover_letter)

    except FileNotFoundError:
        result_text.insert(tk.END, "Error: Resume file not found!")
    except Exception as e:
        result_text.insert(tk.END, f"An error occurred: {str(e)}")


def copy_to_clipboard():
    cover_letter = result_text.get("1.0", tk.END).strip()
    if cover_letter:
        try:
            subprocess.run(['xclip', '-selection', 'clipboard'], input=cover_letter.encode('utf-8'), check=True)
            messagebox.showinfo("Copied", "Text copied to clipboard!")
        except FileNotFoundError:
            try:
                subprocess.run(['xsel', '--clipboard', '--input'], input=cover_letter.encode('utf-8'), check=True)
                messagebox.showinfo("Copied", "Text copied to clipboard!")
            except FileNotFoundError:
                messagebox.showerror("Error", "No clipboard utility found. Install xclip or xsel.")
    else:
        messagebox.showwarning("Warning", "No text to copy!")


def select_resume():
    filename = filedialog.askopenfilename(title="Select Resume",
                                          filetypes=[("PDF Files", "*.pdf"), ("Word Documents", "*.docx *.doc"),
                                                     ("Text Files", "*.txt")])
    resume_entry.delete(0, tk.END)
    resume_entry.insert(0, filename)


root = tk.Tk()
root.title("Resume & Cover Letter Optimizer")
root.geometry("800x700")

resume_frame = tk.Frame(root)
resume_frame.pack(pady=10, padx=10, fill='x')

resume_label = tk.Label(resume_frame, text="Resume:")
resume_label.pack(side=tk.LEFT)
resume_entry = tk.Entry(resume_frame, width=50)
resume_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=5)
resume_button = tk.Button(resume_frame, text="Browse", command=select_resume)
resume_button.pack(side=tk.RIGHT)

job_desc_frame = tk.Frame(root)
job_desc_frame.pack(pady=10, padx=10, fill='x')
job_desc_label = tk.Label(job_desc_frame, text="Job Description:")
job_desc_label.pack(side=tk.TOP)
job_desc_text = scrolledtext.ScrolledText(job_desc_frame, wrap=tk.WORD, height=5)
job_desc_text.pack(expand=True, fill='x', padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)
generate_button = tk.Button(button_frame, text="Generate Cover Letter & Resume", command=generate_cover_letter)
generate_button.pack(side=tk.LEFT, padx=5)
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT, padx=5)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15)
result_text.pack(padx=10, pady=10, expand=True, fill='both')

root.mainloop()

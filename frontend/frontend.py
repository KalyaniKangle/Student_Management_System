import gradio as gr
import requests

# Base URL of your running FastAPI backend
API_URL = "http://127.0.0.1:8000"


# ---------- Helper functions that call your FastAPI endpoints ----------
# All raw JSON handling stays here in Python — the UI only ever gets
# clean, human-readable text or table data.

def create_student(name, course, marks):
    if not name or not course or marks is None:
        return "⚠️ Please fill in all fields before creating a student."
    try:
        r = requests.post(
            f"{API_URL}/students",
            params={"name": name, "course": course, "marks": int(marks)},
        )
        r.raise_for_status()
        return f"✅ Student **{name}** added successfully to **{course}**."
    except Exception as e:
        return f"❌ Failed to create student: {e}"


def _rows_from_students(students):
    """Convert backend records into rows for the Dataframe widget."""
    rows = []
    for s in students:
        rows.append([
            s.get("id", ""),
            s.get("name", ""),
            s.get("course", ""),
            s.get("marks", ""),
        ])
    return rows


def get_all_students():
    try:
        r = requests.get(f"{API_URL}/students")
        r.raise_for_status()
        students = r.json().get("data", [])
        if not students:
            return [], "ℹ️ No students found yet."
        return _rows_from_students(students), f"✅ Loaded {len(students)} student(s)."
    except Exception as e:
        return [], f"❌ Failed to fetch students: {e}"


def get_student(student_id):
    if student_id is None:
        return "⚠️ Please enter a student ID."
    try:
        r = requests.get(f"{API_URL}/students/{int(student_id)}")
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data:
            return f"ℹ️ No student found with ID {int(student_id)}."
        s = data[0]
        return (
            f"### 🧑‍🎓 Student #{s.get('id')}\n"
            f"- **Name:** {s.get('name')}\n"
            f"- **Course:** {s.get('course')}\n"
            f"- **Marks:** {s.get('marks')}"
        )
    except Exception as e:
        return f"❌ Failed to fetch student: {e}"


def update_student(student_id, name, course, marks):
    if student_id is None or not name or not course or marks is None:
        return "⚠️ Please fill in the ID and all fields before updating."
    try:
        r = requests.put(
            f"{API_URL}/students/{int(student_id)}",
            params={"name": name, "course": course, "marks": int(marks)},
        )
        r.raise_for_status()
        return f"✅ Student #{int(student_id)} updated successfully."
    except Exception as e:
        return f"❌ Failed to update student: {e}"


def delete_student(student_id):
    if student_id is None:
        return "⚠️ Please enter a student ID to delete."
    try:
        r = requests.delete(f"{API_URL}/students/{int(student_id)}")
        r.raise_for_status()
        return f"🗑️ Student #{int(student_id)} deleted successfully."
    except Exception as e:
        return f"❌ Failed to delete student: {e}"


# ---------- Look & feel ----------

theme = gr.themes.Soft(
    primary_hue="violet",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Poppins"), "sans-serif"],
).set(
    button_primary_background_fill="linear-gradient(90deg, #7C3AED, #06B6D4)",
    button_primary_background_fill_hover="linear-gradient(90deg, #6D28D9, #0891B2)",
    button_primary_text_color="white",
    block_border_width="1px",
    block_shadow="0 4px 14px rgba(124, 58, 237, 0.12)",
)

custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #F5F3FF 0%, #ECFEFF 100%);
}
#title {
    text-align: center;
    padding: 12px 0 0 0;
}
#title h1 {
    background: linear-gradient(90deg, #7C3AED, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}
.status-box textarea, .status-box {
    font-size: 15px !important;
}
button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: transform 0.15s ease-in-out !important;
}
button:hover {
    transform: translateY(-2px);
}
button.stop, [data-testid="button"].stop {
    background: linear-gradient(90deg, #F43F5E, #EC4899) !important;
    color: white !important;
    border: none !important;
}
button.stop:hover, [data-testid="button"].stop:hover {
    background: linear-gradient(90deg, #E11D48, #DB2777) !important;
}
.gr-tab-item {
    font-weight: 600 !important;
}
"""


# ---------- Gradio UI ----------

with gr.Blocks(title="Kalyani's Student Management Portal", theme=theme, css=custom_css) as demo:
    with gr.Column(elem_id="title"):
        gr.Markdown("# 🎓 Kalyani's Student Management Portal")
        gr.Markdown("A friendly frontend for your FastAPI + Supabase backend")

    with gr.Tab("➕ Add Student"):
        with gr.Row():
            c_name = gr.Textbox(label="Name", placeholder="e.g. Priya Sharma")
            c_course = gr.Textbox(label="Course", placeholder="e.g. B.E. CSE")
            c_marks = gr.Number(label="Marks", precision=0)
        c_btn = gr.Button("Add Student", variant="primary")
        c_out = gr.Markdown(elem_classes="status-box")
        c_btn.click(create_student, inputs=[c_name, c_course, c_marks], outputs=c_out)

    with gr.Tab("📋 All Students"):
        r_btn = gr.Button("Refresh List", variant="primary")
        r_status = gr.Markdown(elem_classes="status-box")
        r_table = gr.Dataframe(
            headers=["ID", "Name", "Course", "Marks"],
            label="Students",
            interactive=False,
            wrap=True,
        )
        r_btn.click(get_all_students, outputs=[r_table, r_status])

    with gr.Tab("🔍 Find Student"):
        g_id = gr.Number(label="Student ID", precision=0)
        g_btn = gr.Button("Search", variant="primary")
        g_out = gr.Markdown(elem_classes="status-box")
        g_btn.click(get_student, inputs=g_id, outputs=g_out)

    with gr.Tab("✏️ Update Student"):
        with gr.Row():
            u_id = gr.Number(label="Student ID", precision=0)
            u_name = gr.Textbox(label="Name")
            u_course = gr.Textbox(label="Course")
            u_marks = gr.Number(label="Marks", precision=0)
        u_btn = gr.Button("Update Student", variant="primary")
        u_out = gr.Markdown(elem_classes="status-box")
        u_btn.click(update_student, inputs=[u_id, u_name, u_course, u_marks], outputs=u_out)

    with gr.Tab("🗑️ Delete Student"):
        d_id = gr.Number(label="Student ID", precision=0)
        d_btn = gr.Button("Delete Student", variant="stop")
        d_out = gr.Markdown(elem_classes="status-box")
        d_btn.click(delete_student, inputs=d_id, outputs=d_out)


if __name__ == "__main__":
    demo.launch()
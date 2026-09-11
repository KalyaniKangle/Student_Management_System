
// =====================================================
// FASTAPI BACKEND URL
// =====================================================

// Empty string means use the same server that served this page.
// Browser → FastAPI → Supabase
const API_URL = "https://student-management-system-2i9y.onrender.com";


// =====================================================
// GET HTML ELEMENTS
// =====================================================

const navButtons =
    document.querySelectorAll(".nav-button");

const sections =
    document.querySelectorAll(".section");

const messageBox =
    document.getElementById("message");


// =====================================================
// NAVIGATION
// =====================================================

navButtons.forEach(button => {

    button.addEventListener("click", () => {

        const sectionId =
            button.getAttribute("data-section");


        // Remove active class from all buttons

        navButtons.forEach(btn => {

            btn.classList.remove("active");

        });


        // Hide all sections

        sections.forEach(section => {

            section.classList.remove(
                "active-section"
            );

        });


        // Activate clicked button

        button.classList.add("active");


        // Show selected section

        document
            .getElementById(sectionId)
            .classList.add("active-section");

    });

});


// =====================================================
// ADD STUDENT
// POST /students
// =====================================================

const addForm =
    document.getElementById("add-form");


addForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const name =
            document
                .getElementById("add-name")
                .value
                .trim();


        const course =
            document
                .getElementById("add-course")
                .value
                .trim();


        const marks =
            document
                .getElementById("add-marks")
                .value;


        if (!name || !course || marks === "") {

            showMessage(
                "Please fill in all fields.",
                "error"
            );

            return;

        }


        try {

            // Your FastAPI backend expects
            // these values as query parameters.

            const params =
                new URLSearchParams();


            params.append(
                "name",
                name
            );


            params.append(
                "course",
                course
            );


            params.append(
                "marks",
                marks
            );


            const response =
                await fetch(
                    `${API_URL}/students?${params.toString()}`,
                    {
                        method: "POST"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Failed to create student"
                );

            }


            const result =
                await response.json();


            showMessage(
                `✅ Student ${name} added successfully!`,
                "success"
            );


            addForm.reset();


        } catch (error) {

            console.error(error);

            showMessage(
                "❌ Failed to create student. Make sure FastAPI is running.",
                "error"
            );

        }

    }
);


// =====================================================
// GET ALL STUDENTS
// GET /students
// =====================================================

const refreshButton =
    document.getElementById(
        "refresh-button"
    );


refreshButton.addEventListener(
    "click",
    getAllStudents
);


async function getAllStudents() {

    const tableBody =
        document.getElementById(
            "student-table-body"
        );


    tableBody.innerHTML = `
        <tr>
            <td
                colspan="4"
                class="no-data"
            >
                Loading students...
            </td>
        </tr>
    `;


    try {

        const response =
            await fetch(
                `${API_URL}/students`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to fetch students"
            );

        }


        const result =
            await response.json();


        const students =
            result.data || [];


        if (students.length === 0) {

            tableBody.innerHTML = `
                <tr>
                    <td
                        colspan="4"
                        class="no-data"
                    >
                        No students found yet.
                    </td>
                </tr>
            `;


            showMessage(
                "No students found.",
                "info"
            );


            return;

        }


        tableBody.innerHTML = "";


        students.forEach(student => {

            const row =
                document.createElement("tr");


            const idCell =
                document.createElement("td");

            idCell.textContent =
                student.id;


            const nameCell =
                document.createElement("td");

            nameCell.textContent =
                student.name;


            const courseCell =
                document.createElement("td");

            courseCell.textContent =
                student.course;


            const marksCell =
                document.createElement("td");

            marksCell.textContent =
                student.marks;


            row.appendChild(idCell);

            row.appendChild(nameCell);

            row.appendChild(courseCell);

            row.appendChild(marksCell);


            tableBody.appendChild(row);

        });


        showMessage(
            `✅ Loaded ${students.length} student(s).`,
            "success"
        );


    } catch (error) {

        console.error(error);


        tableBody.innerHTML = `
            <tr>
                <td
                    colspan="4"
                    class="no-data"
                >
                    Failed to load students.
                </td>
            </tr>
        `;


        showMessage(
            "❌ Failed to fetch students. Make sure FastAPI is running.",
            "error"
        );

    }

}


// =====================================================
// FIND STUDENT
// GET /students/{student_id}
// =====================================================

const findForm =
    document.getElementById(
        "find-form"
    );


findForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const studentId =
            document
                .getElementById("find-id")
                .value;


        const resultBox =
            document.getElementById(
                "student-result"
            );


        if (!studentId) {

            showMessage(
                "Please enter a student ID.",
                "error"
            );

            return;

        }


        try {

            resultBox.classList.remove(
                "hidden"
            );


            resultBox.innerHTML =
                "<p>🔍 Searching...</p>";


            const response =
                await fetch(
                    `${API_URL}/students/${studentId}`
                );


            if (!response.ok) {

                throw new Error(
                    "Failed to find student"
                );

            }


            const result =
                await response.json();


            const students =
                result.data || [];


            if (students.length === 0) {

                resultBox.innerHTML = `
                    <h3>Student Not Found</h3>

                    <p>
                        No student found with ID
                        <strong>${studentId}</strong>.
                    </p>
                `;


                showMessage(
                    "No student found with this ID.",
                    "info"
                );


                return;

            }


            const student =
                students[0];


            resultBox.innerHTML = `
                <h3>
                    🎓 Student #${student.id}
                </h3>

                <div class="student-detail">

                    <span>Name</span>

                    <span>${student.name}</span>

                </div>

                <div class="student-detail">

                    <span>Course</span>

                    <span>${student.course}</span>

                </div>

                <div class="student-detail">

                    <span>Marks</span>

                    <span>${student.marks}</span>

                </div>
            `;


            showMessage(
                "✅ Student found successfully.",
                "success"
            );


        } catch (error) {

            console.error(error);


            resultBox.classList.remove(
                "hidden"
            );


            resultBox.innerHTML = `
                <p>
                    ❌ Failed to find student.
                </p>
            `;


            showMessage(
                "Failed to find student.",
                "error"
            );

        }

    }
);


// =====================================================
// UPDATE STUDENT
// PUT /students/{student_id}
// =====================================================

const updateForm =
    document.getElementById(
        "update-form"
    );


updateForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const studentId =
            document
                .getElementById("update-id")
                .value;


        const name =
            document
                .getElementById("update-name")
                .value
                .trim();


        const course =
            document
                .getElementById("update-course")
                .value
                .trim();


        const marks =
            document
                .getElementById("update-marks")
                .value;


        if (
            !studentId ||
            !name ||
            !course ||
            marks === ""
        ) {

            showMessage(
                "Please fill in all fields.",
                "error"
            );

            return;

        }


        try {

            const params =
                new URLSearchParams();


            params.append(
                "name",
                name
            );


            params.append(
                "course",
                course
            );


            params.append(
                "marks",
                marks
            );


            const response =
                await fetch(
                    `${API_URL}/students/${studentId}?${params.toString()}`,
                    {
                        method: "PUT"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Failed to update student"
                );

            }


            const result =
                await response.json();


            showMessage(
                `✅ Student #${studentId} updated successfully.`,
                "success"
            );


            updateForm.reset();


        } catch (error) {

            console.error(error);


            showMessage(
                "❌ Failed to update student.",
                "error"
            );

        }

    }
);


// =====================================================
// DELETE STUDENT
// DELETE /students/{student_id}
// =====================================================

const deleteForm =
    document.getElementById(
        "delete-form"
    );


deleteForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const studentId =
            document
                .getElementById("delete-id")
                .value;


        if (!studentId) {

            showMessage(
                "Please enter a student ID.",
                "error"
            );

            return;

        }


        const confirmation =
            confirm(
                `Are you sure you want to delete student #${studentId}?`
            );


        if (!confirmation) {

            return;

        }


        try {

            const response =
                await fetch(
                    `${API_URL}/students/${studentId}`,
                    {
                        method: "DELETE"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Failed to delete student"
                );

            }


            const result =
                await response.json();


            showMessage(
                `🗑️ Student #${studentId} deleted successfully.`,
                "success"
            );


            deleteForm.reset();


        } catch (error) {

            console.error(error);


            showMessage(
                "❌ Failed to delete student.",
                "error"
            );

        }

    }
);


// =====================================================
// SHOW MESSAGE
// =====================================================

function showMessage(
    message,
    type
) {

    messageBox.textContent =
        message;


    messageBox.className =
        `message show ${type}`;


    setTimeout(
        () => {

            messageBox.className =
                "message";

            messageBox.textContent =
                "";

        },
        3500
    );

}


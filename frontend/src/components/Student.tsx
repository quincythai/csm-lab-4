import React, { useEffect, useState } from "react";
import { Student as StudentType } from "../utils/types";
import { Attendance } from "../utils/types";
import { useParams } from "react-router";
import Cookies from "js-cookie";

export const Student = () => {
  const [student, setStudent] = useState<StudentType>(undefined as never);
  const [attendances, setAttendances] = useState<Attendance[]>([]);
  const { id } = useParams<string>();

  useEffect(() => {
    fetch(`/api/students/${id}/details`)
      .then((res) => res.json())
      .then((data) => {
        setStudent(data);
      });

    // from urls.py
    console.log("Fetching attendances...");
    fetch(`/api/students/${id}/attendances`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Attendances:", data);
        setAttendances(data);
      });
  }, []);

  // - format: { "id": int, "presence": PR | EX | UN }
  const handleAttendanceChange = (
    attendanceId: number,
    newAttendanceValue: string
  ) => {
    // Update the state locally
    const newAttendances = attendances.map((attendance) =>
      attendance.id === attendanceId
        ? { ...attendance, presence: newAttendanceValue }
        : attendance
    );
    setAttendances(newAttendances);

    // Update the database
    fetch(`/api/students/${id}/attendances/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken") ?? "",
      },
      body: JSON.stringify({ presence: newAttendanceValue }),
    }).then((res) => {
      if (!res.ok) {
        console.error("Failed to update attendance in the database");
        // Optionally handle errors
      }
    });
  };

  return (
    <div>
      <h1>Student</h1>
      {student && (
        <div>
          <p>
            {student.user.first_name} {student.user.last_name} (id: {id})
          </p>
          <p>
            Course: {student.course.name} (id: {student.course.id})
          </p>
          <p>
            Mentor: {student.section.mentor.user.first_name}{" "}
            {student.section.mentor.user.last_name}
          </p>
          <p>Attendances: </p>
          <ul>
            {attendances.map((attendance) => (
              <li key={attendance.id}>
                {attendance.date}:
                <select
                  name="presence"
                  id="presence"
                  value={attendance.presence}
                  onChange={(e) =>
                    handleAttendanceChange(attendance.id, e.target.value)
                  }
                >
                  {/* - format: { "id": int, "presence": PR | EX | UN } */}
                  <option value="PR">Present</option>
                  <option value="EX">Excused absence</option>
                  <option value="UN">Unexcused absence</option>
                </select>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

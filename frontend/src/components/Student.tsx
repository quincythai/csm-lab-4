import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Attendance, Student as StudentType } from "../utils/types";
import Cookies from "js-cookie";

export const Student = () => {
  const [student, setStudent] = useState<StudentType>(undefined as never);
  const [attendances, setAttendances] = useState<Attendance[]>([]);
  const { id } = useParams();

  useEffect(() => {
    fetch(`/api/students/${id}/details/`)
      .then((res) => res.json())
      .then((data) => {
        setStudent(data);
      });

    fetch(`/api/students/${id}/attendances/`)
      .then((res) => res.json())
      .then((data) => {
        // sort by date
        data.sort((a: Attendance, b: Attendance) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return dateA.getTime() - dateB.getTime();
        });
        setAttendances(data);
      });
  }, []);

  const handleAttendanceChange = (
    e: React.ChangeEvent<HTMLSelectElement>,
    attendanceId: number
  ) => {
    const newAttendances = [...attendances];
    const attendance = newAttendances.find((a) => a.id === attendanceId);
    if (attendance) {
      attendance.presence = e.target.value;
    }
    setAttendances(newAttendances);

    // update database
    fetch(`/api/students/${id}/attendances/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken") ?? "",
      },
      body: JSON.stringify({
        id: attendanceId,
        presence: e.target.value,
      }),
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
          <p>Attendances:</p>
          <ul>
            {attendances.map((attendance) => (
              <li key={attendance.id}>
                {attendance.date}:{" "}
                <select
                  defaultValue={attendance.presence}
                  onChange={(e) => handleAttendanceChange(e, attendance.id)}
                >
                  <option value="PR">Present</option>
                  <option value="EX">Excused Absence</option>
                  <option value="UN">Unexcused Absence</option>
                </select>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

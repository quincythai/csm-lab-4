import React, { useState, useEffect } from "react";
import { Section as SectionType, Student } from "../utils/types";
import { Link, useParams } from "react-router-dom";
import Cookies from "js-cookie";

export const Section = () => {
  const [section, setSection] = useState<SectionType>(undefined as never);
  const [students, setStudents] = useState<Student[]>([]);
  const { id } = useParams();

  useEffect(() => {
    fetch(`/api/sections/${id}/details/`)
      .then((res) => res.json())
      .then((data) => {
        setSection(data);
      });
    fetch(`/api/sections/${id}/students/`)
      .then((res) => res.json())
      .then((data) => {
        setStudents(data);
      });
  }, []);

  const handleDrop = (student_id: number) => {
    const newStudents = students.filter((s) => s.id !== student_id);
    setStudents(newStudents);

    // update database
    fetch(`/api/students/${student_id}/drop/`, {
      method: "PATCH",
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken") ?? "",
      },
    });
  };

  return (
    <div>
      <h1>Section</h1>
      {section && (
        <div>
          <p>
            {section.mentor.course.name} (id: {id})
          </p>
          <p>
            Mentor: {section.mentor.user.first_name}{" "}
            {section.mentor.user.last_name}
          </p>
        </div>
      )}
      <p>Students:</p>
      <ul>
        {students.map((student) => (
          <li key={student.id}>
            <button onClick={() => handleDrop(student.id)}>Drop</button>{" "}
            <Link to={`/students/${student.id}`}>
              {student.user.first_name} {student.user.last_name} (id:{" "}
              {student.id})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

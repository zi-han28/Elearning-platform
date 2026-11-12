import {useState, useEffect} from "react"
import { Link } from "react-router-dom";
import api from "../api"

function Home(){
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let cancelled = false;

        api.get("/api/courses/")
            .then((res) => {
                if (!cancelled) setCourses(res.data);
            })
            .catch(() => {
                if (!cancelled) setError("Could not load courses. Please try again.");
            })
            .finally(() => {
                if (!cancelled) setLoading(false);
            });

        return () => { cancelled = true; };
    }, []);

    if (loading) return <div className="container mt-4">Loading...</div>;

    return (
        <div className="container mt-4">
            <h2 className="mb-4">All Courses</h2>

            {error && <div className="alert alert-danger">{error}</div>}

            {!error && courses.length === 0 && (
                <div className="alert alert-info">No courses have been created yet.</div>
            )}

            <div className="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
                {courses.map((course) => (
                    <div className="col" key={course.id}>
                        <div className="card h-100">
                            {course.course_picture && (
                                <img
                                    src={course.course_picture}
                                    alt={course.title}
                                    className="card-img-top"
                                    style={{ height: 180, objectFit: "cover" }}
                                />
                            )}
                            <div className="card-body d-flex flex-column">
                                <h5 className="card-title">
                                    <Link to={`/courses/${course.slug}`} className="stretched-link text-decoration-none">
                                        {course.title}
                                    </Link>
                                </h5>
                                <p className="text-muted small mb-2">By {course.teacher ?? "Unknown teacher"}</p>
                                <p
                                    className="card-text"
                                    style={{ display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden" }}
                                >
                                    {course.overview}
                                </p>
                                <div className="mt-auto d-flex justify-content-between text-muted small">
                                    <span>{new Date(course.created).toLocaleDateString()}</span>
                                    <span>&hearts; {course.like_count}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Home;

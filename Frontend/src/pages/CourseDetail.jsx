import {useState, useEffect} from "react"
import { Link, useNavigate , useParams} from "react-router-dom";
import api from "../api"


function CourseDetail() {
    const { slug } = useParams();
    const [course, setCourse] = useState(null)
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    

    useEffect(() => {
        let cancelled = false;
        setLoading(true);
        setError("");

        api.get(`/api/courses/${slug}/`)
            .then((res) => {
                if (!cancelled) setCourse(res.data);
            })
            .catch((err) => {
                if (cancelled) return;
                if (err.response?.status === 404) {
                    setError("Course not found.");
                } else {
                    setError("Could not load course. Please try again.");
                }
            })
            .finally(() => {
                if (!cancelled) setLoading(false);
            });

        return () => { cancelled = true; };
    }, [slug]);

    if (loading) return <div className="container mt-4">Loading...</div>;

    if (error) {
        return (
            <div className="container mt-4">
                <div className="alert alert-danger">{error}</div>
                <Link to="/" className="btn btn-secondary">Back to courses</Link>
            </div>
        );
    }

    if (!course) return null;
    return(
        <div className="container mt-4">
            <Link to="/" className="btn btn-link mb-3">&larr; Back to courses</Link>

            <div className="card">
                {course.course_picture && (
                    <img
                        src={course.course_picture}
                        alt={course.title}
                        className="card-img-top"
                        style={{ maxHeight: 300, objectFit: "cover" }}
                    />
                )}
                <div className="card-body">
                    <div className="d-flex justify-content-between align-items-start">
                        <h2 className="card-title mb-1">{course.title}</h2>
                        <span className="badge bg-secondary">{course.slug}</span>
                    </div>

                    <p className="text-muted mb-3">
                        By {course.teacher?.username ?? "Unknown teacher"}
                    </p>

                    <p className="card-text" style={{ whiteSpace: "pre-wrap" }}>
                        {course.overview}
                    </p>

                    <div className="d-flex gap-2">
                        {course.enrolled && (
                            <span className="badge bg-success align-self-center">
                                Enrolled
                            </span>
                        )}
                        <Link
                            to={`/courses/${course.slug}/modules/`}
                            className="btn btn-primary"
                        >
                            View modules
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default CourseDetail;
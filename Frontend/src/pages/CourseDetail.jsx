import {useState, useEffect} from "react"
import { Link, useNavigate , useParams} from "react-router-dom";
import api from "../api"
import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "../constants";


function CourseDetail() {
    const { slug } = useParams();
    const [course, setCourse] = useState(null)
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const navigate = useNavigate()
    const token = localStorage.getItem(ACCESS_TOKEN);
    const currentUserId = token ? jwtDecode(token).user_id : null;
    const isOwner = currentUserId != null && String(course?.teacher?.id) === String(currentUserId);

    const handleDeleteSubmit = async(e) =>{
        api.delete(`/api/courses/${slug}/`)
        navigate("/")
    }

    const handleModuleDelete = async (module) => {
        if (!window.confirm(`Delete module "${module.title}"?`)) return;
        try {
            await api.delete(`/api/modules/${module.id}/`);
            setCourse((c) => ({ ...c, modules: c.modules.filter((m) => m.id !== module.id) }));
        } catch {
            setError("Could not delete module. Please try again.");
        }
    }


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
        <div className="container mt-4" >
            <Link to="/" className="btn btn-link mb-3">&larr; Back to courses</Link>

            <div className="card">
                {course.course_picture && (
                    <img
                        src={course.course_picture}
                        alt={course.title}
                        className="img-thumbnail justify-content-center" 
                        style={{ maxHeight: 300, width:'18rem', }}
                    />
                )}
                <div className="card-body">
                    <div className="justify-content-between align-items-start">
                        <h2 className="card-title">{course.title}</h2>
                        <span className="badge bg-secondary mb-3">{course.slug}</span>
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
                        {isOwner && (
                            <button className="btn btn-outline-danger w-100" onClick={handleDeleteSubmit}>
                                Delete Course
                            </button>
                        )}
                    </div>
                </div>
            </div>

            <div className="card mt-4">
                <div className="card-header d-flex justify-content-between align-items-center">
                    <h4 className="mb-0">Modules</h4>
                    {isOwner && (
                        <Link to={`/courses/${course.slug}/modules/create`} className="btn btn-primary btn-sm">
                            + Add a new module
                        </Link>
                    )}
                </div>
                <ul className="list-group list-group-flush">
                    {course.modules.length === 0 && (
                        <li className="list-group-item text-muted">No modules yet.</li>
                    )}
                    {course.modules.map((module) => (
                        <li key={module.id} className="list-group-item">
                            <div className="d-flex justify-content-between align-items-start">
                                <div>
                                    <h5 className="mb-1">{module.order}. {module.title}</h5>
                                    {module.description && (
                                        <p className="mb-1" style={{ whiteSpace: "pre-wrap" }}>
                                            {module.description}
                                        </p>
                                    )}
                                    {module.file && (
                                        <a href={module.file} target="_blank" rel="noreferrer" className="small">
                                            View {module.file_type || "file"}
                                        </a>
                                    )}
                                </div>
                                {isOwner && (
                                    <div className="d-flex gap-2">
                                        <Link to={`/modules/${module.id}/edit`} className="btn btn-outline-secondary btn-sm">
                                            Edit
                                        </Link>
                                        <button className="btn btn-outline-danger btn-sm" onClick={() => handleModuleDelete(module)}>
                                            Delete
                                        </button>
                                    </div>
                                )}
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}

export default CourseDetail;
import {useState, useEffect} from "react"
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api"
import { useNotification } from "../components/Notifications";

function CourseCreate(){
    const { slug } = useParams();
    const isEdit = Boolean(slug);
    const [error, setError] = useState("");
    const [picture, setPicture] = useState(null);
    const [currentPicture, setCurrentPicture] = useState("");
    const [overview, setOverview] = useState("");
    const [preview, setPreview] = useState("");
    const [title, setTitle] = useState("")
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [fieldErrors, setFieldErrors] = useState({});
    const {notify} = useNotification()
    const navigate = useNavigate();


    // for preview pic effect
    useEffect(() => {
        if (!picture) {
            setPreview("");
            return;
        }
        const url = URL.createObjectURL(picture);
        setPreview(url);
        return () => URL.revokeObjectURL(url);
    }, [picture]);

    // edit course effect
    useEffect(() => {
        let cancelled = false;
        setLoading(true);
        setError("");
        if (!isEdit) {
            setLoading(false);
            return;
        }   
        
        api.get(`/api/courses/${slug}/`).then((res) => {
                if (cancelled) return;
                const m = res.data;
                setCurrentPicture(res.data.course_picture || "");
                setTitle(m.title);
                setOverview(m.overview);
            }).catch((err) => {
            if (cancelled) return;
            setError(err.response?.status === 404
                ? (isEdit ? "Module not found." : "Course not found.")
                : "Could not load data. Please try again.");
        }).finally(() => {
            if (!cancelled) setLoading(false);
        });

        return () => { cancelled = true; };
    }, [ slug, isEdit]);
    
    const handleSubmit = async (e) =>{
        e.preventDefault();
        setSaving(true);
        setFieldErrors({});
        setError("");
        const fd = new FormData();
        fd.append("title", title);
        fd.append("overview", overview);
        if (picture) fd.append("course_picture", picture); 

        try{
            const res = isEdit
                ? await api.patch(`/api/courses/${slug}/update/`, fd)
                : await api.post("/api/courses/create/", fd);
            navigate(`/courses/${res.data.slug}`);
            notify(`${res.data.title} has been created!`)
        }catch(err){
            const data = err.response?.data;
            if (data && typeof data === "object") {
                setFieldErrors(data);
            } else if (err.response?.status === 403) {
                setError("Only teachers can create courses.");
            } else {
                setError("Something went wrong. Please try again.");
            }
        }finally{
            setSaving(false)
        }
    }
    
    // Bootstrap invalid styling + message for one field, like crispy forms does
    const invalid = (name) => (fieldErrors[name] ? " is-invalid" : "");
    const feedback = (name) =>
        fieldErrors[name] && (
            <div className="invalid-feedback">{fieldErrors[name].join(" ")}</div>
        );

    

    return (
        <div className="container mt-4">
            <div className="card">
                <div className="card-header">
                    <h2>Create New Course</h2>
                </div>
                <div className="card-body">
                    {error && <div className="alert alert-danger">{error}</div>}

                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <label htmlFor="title" className="form-label">
                                Title<span className="text-danger">*</span>
                            </label>
                            <input
                                id="title"
                                type="text"
                                className={"form-control" + invalid("title")}
                                maxLength={200}
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                required
                            />
                            {feedback("title")}
                        </div>

                        <div className="mb-3">
                            <label htmlFor="overview" className="form-label">
                                Overview<span className="text-danger">*</span>
                            </label>
                            <textarea
                                id="overview"
                                rows={4}
                                className={"form-control" + invalid("overview")}
                                value={overview}
                                onChange={(e) => setOverview(e.target.value)}
                                required
                            />
                            {feedback("overview")}
                        </div>

                        <div className="mb-3">
                            <label htmlFor="course_picture" className="form-label">
                                Course picture
                            </label>
                            <input
                                id="course_picture"
                                type="file"
                                accept="image/*"
                                className={"form-control" + invalid("course_picture")}
                                onChange={(e) => setPicture(e.target.files[0] || null)}
                                required
                            />
                            {feedback("course_picture")}
                            {preview && (
                                <img
                                    src={preview}
                                    alt="Course picture preview"
                                    className="img-thumbnail mt-2"
                                    style={{ maxHeight: 200 }}
                                />
                            )}
                        </div>

                        <button type="submit" className="btn btn-primary mt-3" disabled={saving}>
                            {saving ? "Creating..." : "Create"}
                        </button>
                        <Link to="/" className="btn btn-secondary mt-3 ms-2">
                            Cancel
                        </Link>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default CourseCreate;
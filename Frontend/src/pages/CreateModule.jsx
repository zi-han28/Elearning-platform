import {useState, useEffect} from "react"
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../api"
import { useNotification } from "../components/Notifications";

const FILE_TYPES = [
    ["pdf", "PDF"],
    ["image", "Image"],
    ["document", "document"],
];

// handles both "add module" (/courses/:slug/modules/create) and "update module" (/modules/:id/edit)
function CreateModule(){
    const { slug, id } = useParams();
    const isEdit = Boolean(id);
    const [courseSlug, setCourseSlug] = useState(slug || "");
    const [courseTitle, setCourseTitle] = useState("");
    const [moduleTitle, setModuleTitle] = useState("");
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [order, setOrder] = useState(1);
    const [file, setFile] = useState(null);
    const [currentFile, setCurrentFile] = useState("");
    const [fileType, setFileType] = useState("");
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [fieldErrors, setFieldErrors] = useState({});
    const {notify} = useNotification()
    const navigate = useNavigate();

    useEffect(() => {
        let cancelled = false;
        setLoading(true);
        setError("");

        const request = isEdit
            ? api.get(`/api/modules/${id}/`).then((res) => {
                if (cancelled) return;
                const m = res.data;
                setCourseSlug(m.course);
                setModuleTitle(m.title);
                setTitle(m.title);
                setDescription(m.description);
                setOrder(m.order);
                setFileType(m.file_type);
                setCurrentFile(m.file || "");
            })
            : api.get(`/api/courses/${slug}/`).then((res) => {
                if (cancelled) return;
                setCourseTitle(res.data.title);
                // default the order to the next position
                setOrder(res.data.modules.length + 1);
            });

        request.catch((err) => {
            if (cancelled) return;
            setError(err.response?.status === 404
                ? (isEdit ? "Module not found." : "Course not found.")
                : "Could not load data. Please try again.");
        }).finally(() => {
            if (!cancelled) setLoading(false);
        });

        return () => { cancelled = true; };
    }, [slug, id, isEdit]);

    const handleSubmit = async (e) =>{
        e.preventDefault();
        setSaving(true);
        setFieldErrors({});
        setError("");
        const fd = new FormData();
        fd.append("title", title);
        fd.append("description", description);
        fd.append("order", order);
        fd.append("file_type", fileType);
        // only send a file when a new one was picked, so updating keeps the old file
        if (file) fd.append("file", file);

        try{
            const res = isEdit
                ? await api.patch(`/api/modules/${id}/`, fd)
                : await api.post(`/api/courses/${slug}/modules/`, fd);
            navigate(`/courses/${courseSlug}`);
            notify(`${res.data.title} has been ${isEdit ? "updated" : "added"}!`)
        }catch(err){
            const data = err.response?.data;
            if (err.response?.status === 403) {
                setError("Only the course teacher can manage modules.");
            } else if (data && typeof data === "object") {
                setFieldErrors(data);
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
            <div className="invalid-feedback">{[].concat(fieldErrors[name]).join(" ")}</div>
        );

    if (loading) return <div className="container mt-4">Loading...</div>;

    return (
        <div className="container mt-4">
            <div className="card">
                <div className="card-header">
                    <h2>
                        {isEdit
                            ? `Update Module "${moduleTitle}"`
                            : `Add Module to "${courseTitle}"`}
                    </h2>
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
                            <label htmlFor="description" className="form-label">
                                Description
                            </label>
                            <textarea
                                id="description"
                                rows={3}
                                className={"form-control" + invalid("description")}
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                            />
                            {feedback("description")}
                        </div>

                        <div className="mb-3">
                            <label htmlFor="order" className="form-label">
                                Order<span className="text-danger">*</span>
                            </label>
                            <input
                                id="order"
                                type="number"
                                min={1}
                                className={"form-control" + invalid("order")}
                                value={order}
                                onChange={(e) => setOrder(e.target.value)}
                                required
                            />
                            {feedback("order")}
                        </div>

                        <div className="mb-3">
                            <label htmlFor="file" className="form-label">
                                File
                            </label>
                            {currentFile && (
                                <div className="small mb-1">
                                    Currently: <a href={currentFile} target="_blank" rel="noreferrer">
                                        {decodeURIComponent(currentFile.split("/").pop())}
                                    </a>
                                </div>
                            )}
                            <input
                                id="file"
                                type="file"
                                accept=".pdf,.docx,.pptx,.txt,.mp4,.jpg,.png"
                                className={"form-control" + invalid("file")}
                                onChange={(e) => setFile(e.target.files[0] || null)}
                            />
                            <div className="form-text">Upload images or pdfs.</div>
                            {feedback("file")}
                        </div>

                        <div className="mb-3">
                            <label htmlFor="file_type" className="form-label">
                                File type
                            </label>
                            <select
                                id="file_type"
                                className={"form-select" + invalid("file_type")}
                                value={fileType}
                                onChange={(e) => setFileType(e.target.value)}
                            >
                                <option value="">---------</option>
                                {FILE_TYPES.map(([value, label]) => (
                                    <option key={value} value={value}>{label}</option>
                                ))}
                            </select>
                            {feedback("file_type")}
                        </div>

                        <button type="submit" className="btn btn-primary mt-3" disabled={saving}>
                            {saving
                                ? (isEdit ? "Updating..." : "Adding...")
                                : (isEdit ? "Update Module" : "Add Module")}
                        </button>
                        <Link to={`/courses/${courseSlug}`} className="btn btn-secondary mt-3 ms-2">
                            Cancel
                        </Link>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default CreateModule;

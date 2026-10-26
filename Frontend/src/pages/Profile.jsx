import {useState, useEffect} from "react"
import { data, Link, useNavigate } from "react-router-dom";
import api from "../api"

const STATUS_OPTIONS = [
    { value: "active", label: "Active" },
    { value: "not_active", label: "Not Active" },
    { value: "busy", label: "Busy" },
    { value: "anonymous", label: "Anonymous" },
];

function Profile(){
    const [profile, setProfile] = useState(null);
    const [form, setForm] = useState({ status: "active", bio: "" });
    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);
    const [fileKey, setFileKey] = useState(0);
    const [errors, setErrors] = useState({});
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    useEffect(()=>{
        api
        .get("/api/profile/")
        .then((res)=> {
            setProfile(res.data)
            setForm({ status: res.data.status, bio: res.data.bio })
        }).catch((err)=>alert(err)).finally(setLoading(false));
    }, [])

    useEffect(()=>{
        if (!image){
            setPreview(null)
            return;
        }
        const url = URL.createObjectURL(image);
        setPreview(url);
        return () => URL.revokeObjectURL(url);
    },[image]);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async(e) =>{
        e.preventDefault();
        setSaving(true);
        setErrors({});
        setSuccess("");

        const data = new FormData();
        data.append("status", form.status);
        data.append("bio", form.bio);
        if (image) data.append("profile_picture", image);

        try{
            const res = await api.patch("/api/profile/", data);
            setProfile(res.data)
            setImage(null)
            setFileKey((k)=>k+1);
            setSuccess("Your account has been updated!");
        }catch(err){
            const d = err.response?.data;
            setErrors(
                d && typeof d === "object" 
                ? d : { non_field_errors: ["Update failed. Please try again."] }
            );
        }finally{
            setSaving(false);
        }
    };

    const msg = (name) => errors[name] && [].concat(errors[name]).join(" ");

    if (loading) return <div>Loading...</div>;
    if (!profile) {
        return <div className="alert alert-danger">{msg("non_field_errors")}</div>;
    }


    return(
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header"><h2>Profile</h2></div>
                    <div className="card-body">
                        {success && <div className="alert alert-success">{success}</div>}
                        {msg("non_field_errors") && (<div className="alert alert-danger">{msg("non_field_errors")}</div>)}
                        <div className="d-flex align-items-center mb-4">
                            <img 
                                src={preview || profile.profile_picture}
                                alt="Profile"
                                className="rounded-circle me-3"
                                style={{width:120, height: 120, objectFit:"cover"}}
                            />
                            <div>
                                <h4 className="mb-0">{profile.username}</h4>
                                <small className="text-muted">{profile.email}</small>
                            </div>
                        </div>
                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="profile_picture">Profile Picture</label>
                                <input 
                                    key={fileKey}
                                    id="profile_picture"
                                    type="file"
                                    accept="image/*"
                                    className={`form-control ${msg("profile_picture")? "is-Invalid": ""}`}
                                    onChange={(e)=> setImage(e.target.files[0]) || null}/>
                                {msg("profile_picture") && (<div className="invalid-feedback">{msg("profile_picture")}</div>)}
                            </div>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="status">Status</label>
                                <select
                                id="status"
                                name="status"
                                className={`form-select ${msg("status") ? "is-invalid" : ""}`}
                                value={form.status}
                                onChange={handleChange}
                                >
                                {STATUS_OPTIONS.map((o) => (
                                    <option key={o.value} value={o.value}>{o.label}</option>
                                ))}
                                </select>
                                {msg("status") && <div className="invalid-feedback">{msg("status")}</div>}
                            </div>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="bio">Bio</label>
                                <textarea
                                id="bio"
                                name="bio"
                                rows={4}
                                maxLength={500}
                                className={`form-control ${msg("bio") ? "is-invalid" : ""}`}
                                value={form.bio}
                                onChange={handleChange}
                                />
                                <div className="form-text">{form.bio.length}/500</div>
                                {msg("bio") && <div className="invalid-feedback">{msg("bio")}</div>}
                            </div>
                            <button type="submit" className="btn btn-primary" disabled={saving}>
                                {saving ? "Saving..." : "Save changes"}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;
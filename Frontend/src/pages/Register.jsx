import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";

function Field({ label, name, type = "text", form, errors, onChange }) {
    const msg = errors[name] && [].concat(errors[name]).join(" ");
    return (
        <div className="mb-3">
        <label className="form-label" htmlFor={name}>{label}</label>
        <input
            id={name}
            name={name}
            type={type}
            className={`form-control ${msg ? "is-invalid" : ""}`}
            value={form[name]}
            onChange={onChange}
            required
        />
        {msg && <div className="invalid-feedback">{msg}</div>}
        </div>
    );
}

function Register() {
    const [form, setForm] = useState({
        username: "", email: "", password: "", password2: "", is_teacher: false,
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, type, value, checked } = e.target;
        setForm({ ...form, [name]: type === "checkbox" ? checked : value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setErrors({});
        try {
        await api.post("/api/user/register/", form);
        navigate("/login");
        } catch (err) {
        const data = err.response?.data;
        if (data && typeof data === "object") {
            setErrors(data);
        } else {
            setErrors({ non_field_errors: ["Registration failed. Please try again."] });
        }
        } finally {
        setLoading(false);
        }
    };

    return (
        <div className="row justify-content-center">
        <div className="col-md-6">
            <div className="card">
            <div className="card-header"><h2>Register</h2></div>
            <div className="card-body">
                {errors.non_field_errors && (
                <div className="alert alert-danger">
                    {[].concat(errors.non_field_errors).join(" ")}
                </div>
                )}
                <form onSubmit={handleSubmit}>
                <Field label="Username" name="username" form={form} errors={errors} onChange={handleChange} />
                <Field label="Email" name="email" type="email" form={form} errors={errors} onChange={handleChange} />
                <Field label="Password" name="password" type="password" form={form} errors={errors} onChange={handleChange} />
                <Field label="Confirm password" name="password2" type="password" form={form} errors={errors} onChange={handleChange} />
                <div className="form-check mb-3">
                    <input
                    id="is_teacher"
                    name="is_teacher"
                    type="checkbox"
                    className="form-check-input"
                    checked={form.is_teacher}
                    onChange={handleChange}
                    />
                    <label className="form-check-label" htmlFor="is_teacher">
                    Register as instructor
                    </label>
                </div>
                <button type="submit" className="btn btn-primary w-100 mt-3" disabled={loading}>
                    {loading ? "Signing up..." : "Sign Up"}
                </button>
                </form>
                <div className="mt-3 text-center">
                <small className="text-muted">
                    Already have an account? <Link to="/login">Login</Link>
                </small>
                </div>
            </div>
            </div>
        </div>
        </div>
    );
}

export default Register;
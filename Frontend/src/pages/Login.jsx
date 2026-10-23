import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        try {
        const res = await api.post("/api/token/", { username, password });
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
        } catch {
        setError("Invalid username or password");
        } finally {
        setLoading(false);
        }
    };

    return (
            <div className="row justify-content-center">
            <div className="col-md-6">
                <div className="card">
                <div className="card-header"><h2>Login</h2></div>
                <div className="card-body">
                    {error && <div className="alert alert-danger">{error}</div>}
                    <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="form-label" htmlFor="username">Username</label>
                        <input id="username" className="form-control" value={username}
                        onChange={(e) => setUsername(e.target.value)} required />
                    </div>
                    <div className="mb-3">
                        <label className="form-label" htmlFor="password">Password</label>
                        <input id="password" type="password" className="form-control" value={password}
                        onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    <button type="submit" className="btn btn-primary w-100 mt-3" disabled={loading}>
                        {loading ? "Logging in..." : "Login"}
                    </button>
                    </form>
                    <div className="mt-3 text-center">
                    <small className="text-muted">
                        Do not have an account with us? <Link to="/register">Register</Link>
                    </small>
                    </div>
                </div>
                </div>
            </div>
            </div>
        );
    }

export default Login;
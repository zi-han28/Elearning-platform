import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api";


function UserProfile() {
    const { id } = useParams();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let ignore = false;
        setLoading(true);
        setError("");
        setUser(null);

        api.get(`/api/users/${id}/`)
            .then((res)=>{
                if(!ignore) setUser(res.data)
            })
            .catch((err)=>{
                if (!ignore) {
                    setError(
                    err.response?.status === 404 ? "User not found." : "Could not load this profile."
                    );
                }
            }).finally(() => {
                if (!ignore) setLoading(false);
            });
            return ()=>{
                ignore = true
            }
    },[id])

    if (loading) return <div>Loading...</div>;

        if (error) {
        return (
            <div>
                <div className="alert alert-danger">{error}</div>
                <Link to="/users/search">← Back to search</Link>
            </div>
            );
        }
    return (
        <div>
            <Link to="/users/search" className="d-inline-block mb-3">← Back to search</Link>
            <div className="card">
                <div className="card-body">
                <div className="row">
                    <div className="col-md-3 text-center">
                    <img
                        src={user.profile_picture}
                        alt={`${user.username}'s profile picture`}
                        className="rounded-circle mb-3"
                        style={{ width: 150, height: 150, objectFit: "cover" }}
                    />
                    <h4>{user.username}</h4>
                    <p>
                        <span className={`badge ${user.is_teacher ? "bg-info" : "bg-success"}`}>
                        {user.is_teacher ? "Teacher" : "Student"}
                        </span>
                    </p>
                    <p className="text-muted text-capitalize">{user.status?.replace("_", " ")}</p>
                    </div>
        
                    <div className="col-md-9">
                    <h5>About</h5>
                    <p>{user.bio || "No bio provided"}</p>
                    <hr />
                    <h5>Contact Information</h5>
                    <p><strong>Email:</strong> {user.email}</p>
                    </div>
                </div>
                </div>
            </div>
            </div>
    )
}

export default UserProfile;
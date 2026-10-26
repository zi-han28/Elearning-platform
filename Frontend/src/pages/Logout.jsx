import { useEffect } from "react";
import { Link } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Logout(){

    useEffect(() => {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
    }, []);

    return (
        <div className="row justify-content-center">
            <div className="col-md-6">
                <div className="card">
                    <div className="card-header">
                        <h2>Logged Out</h2>
                    </div>
                    <div className="card-body text-center">
                        <p>You have been successfully logged out.</p>
                        <div className="d-grid gap-2">
                            <Link to="/login" className="btn btn-primary">Log in again</Link>
                            <Link to="/" className="btn btn-secondary">Return to homepage</Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}

export default Logout;

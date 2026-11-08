import {useState} from "react"
import { data, Link, useNavigate } from "react-router-dom";
import api from "../api"

const USER_TYPES = [
        { value: "all", label: "Any" },
        { value: "students", label: "Students" },
        { value: "teachers", label: "Teachers" },
    ];

function UserSearch(){
    const[query, setQuery] = useState("");
    const[loading, setLoading] = useState(false);
    const[category, setCategory] = useState("any");
    const [error, setError] = useState("");
    const [searched, setSearched] = useState(false);
    const [results, setResults] = useState([])


    const handleSubmit= async(e)=>{
        e.preventDefault();
        setLoading(true);
        setError("");
        try{
            const res = await api.get("/api/users/search/", {params: { search_query: query.trim(), user_type: category }});
            setResults(res.data);
            setSearched(true);
        }catch{
            setError("Search failed")
        }finally{
            setLoading(false)
        }
    }
    const clear = () => {
        setQuery("");
        setResults([]);
        setSearched(false);
    };


    return (
        <div className="container mt-4">
            <h2>Search Users</h2>
            <form onSubmit={handleSubmit}>
                <div className="card mb-4">
                    <div className="card-body">
                            <div className="row g-3">
                                <div className="col-md-8">
                                    <label htmlFor="sizesInputLarge" className="form-label"> Search </label>
                                    <input 
                                        type="search"
                                        className="form-control form-control-lg" 
                                        id="sizesInputLarge" 
                                        aria-label="Large input example" 
                                        value={query} 
                                        onChange={(e)=> setQuery(e.target.value)} 
                                        placeholder="Type to search..."/>
                                </div>
                                <div className="col-md-2">
                                    <label htmlFor="user_type" className="form-label">Category</label>
                                    <select id="user_type" className="form-select form-select-lg" value={category} onChange={(e) => setCategory(e.target.value)}>
                                        {USER_TYPES.map((o)=>(
                                            <option key={o.value} value={o.value}>{o.label}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="col-md-2 d-flex align-items-end">
                                    <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                                        {loading ? "Searching..." : "Search"}
                                    </button>
                                </div>
                            </div>
                    </div>
                </div>
            </form>
            
            {error && <div className="alert alert-danger">{error}</div>}

            {searched && !error && (
                results.length > 0 ? (
                <div className="card">
                    <div className="card-body">
                    <h5 className="card-title">Search Results</h5>
                    <ul className="list-group">
                        {results.map((u) => (
                        <li
                            key={u.id}
                            className="list-group-item list-group-item-action d-flex align-items-center gap-3"
                        >
                            {u.profile_picture ? (
                            <img
                                src={u.profile_picture}
                                alt=""
                                className="rounded-circle"
                                style={{ width: 40, height: 40, objectFit: "cover" }}
                            />
                            ):(
                                <span className="rounded-circle me-2 bg-secondary d-inline-flex align-items-center justify-content-center"
                                    style={{ width: 28, height: 28, fontSize: 12, color: "#6d29e4" }}>
                                    {u.username?.[0]?.toUpperCase() ?? "?"}
                            </span>
                            )}
                            <Link to={`/users/${u.id}`} className="stretched-link text-decoration-none fw-semibold">
                            {u.username}
                            </Link>
                            <span className={`badge ${u.is_teacher ? "bg-info" : "bg-success"}`}>
                            {u.is_teacher ? "Teacher" : "Student"}
                            </span>
                            <span className="badge bg-secondary text-capitalize">
                            {u.status?.replace("_", " ")}
                            </span>
                        </li>
                        ))}
                    </ul>
                    </div>
                </div>
                ) : (
                <div className="alert alert-info">No users found matching your search criteria.</div>
                )
            )}
            </div>
        );
        }
        
export default UserSearch;

import { Link, Outlet, useLocation } from "react-router-dom";
import { Navbar, Nav, Container } from "react-bootstrap";
import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN } from "../constants";

function Layout() {
    useLocation();
    const token = localStorage.getItem(ACCESS_TOKEN);
    const user = token ? jwtDecode(token) : null;

    return (
            <>
            <Navbar expand="lg" bg="dark" variant="dark">
                <Container>
                <Navbar.Brand as={Link} to="/">eLearning</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarNav" />
                <Navbar.Collapse id="navbarNav">
                    <Nav className="me-auto">
                    <Nav.Link as={Link} to="/">Courses</Nav.Link>
                    {user?.is_teacher && (
                        <Nav.Link as={Link} to="/courses/new">Create Course</Nav.Link>
                    )}
                    {user && <Nav.Link as={Link} to="/users/search">Search Users</Nav.Link>}
                    </Nav>
                    <Nav>
                    {user ? (
                        <>
                        <Nav.Link as={Link} to="/profile">Profile</Nav.Link>
                        <Nav.Link as={Link} to="/logout">Logout</Nav.Link>
                        </>
                    ) : (
                        <>
                        <Nav.Link as={Link} to="/login">Login</Nav.Link>
                        <Nav.Link as={Link} to="/register">Register</Nav.Link>
                        </>
                    )}
                    </Nav>
                </Navbar.Collapse>
                </Container>
            </Navbar>

            <div className="container mt-4">
                <Outlet />
            </div>

            <footer className="bg-dark text-white mt-5 py-4">
                <div className="container text-center">
                <p>&copy; Xu Zihan eLearning Platform</p>
                </div>
            </footer>
            </>
        );
    }

export default Layout;
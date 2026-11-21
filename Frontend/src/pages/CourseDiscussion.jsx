import { useState, useEffect, useRef } from "react";
import { Link, useParams } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";

const WS_BASE = import.meta.env.VITE_WS_URL ?? "ws://localhost:8000";

function CourseDiscussion() {
    const { slug } = useParams();
    const [messages, setMessages] = useState([]);
    const [text, setText] = useState("");
    const [status, setStatus] = useState("connecting"); // connecting | connected | disconnected
    const wsRef = useRef(null);
    const bottomRef = useRef(null);

    const token = localStorage.getItem(ACCESS_TOKEN);
    const me = token ? jwtDecode(token).username : null; // added by CustomTokenSerializer

    // 1. load past messages over HTTP (needs the history endpoint, see below)
    useEffect(() => {
        let cancelled = false;
        api.get(`/chat/api/${slug}/messages/`)
            .then((res) => {
                // prepend, in case a live message arrived first
                if (!cancelled) setMessages((prev) => [...res.data, ...prev]);
            })
            .catch(() => {}); // chat still works without history
        return () => { cancelled = true; };
    }, [slug]);

    // 2. open the WebSocket
    useEffect(() => {
        const ws = new WebSocket(`${WS_BASE}/ws/chat/${slug}/?token=${token}`);
        wsRef.current = ws;

        ws.onopen = () => setStatus("connected");
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            setMessages((prev) => [
                ...prev,
                { username: data.username, message: data.message, timestamp: data.timestamp },
            ]);
        };
        ws.onclose = () => {
            // ignore the close of a socket we replaced or cleaned up ourselves
            if (wsRef.current === ws) setStatus("disconnected");
        };

        return () => {
            wsRef.current = null;
            ws.close();
        };
    }, [slug, token]);

    // keep the newest message in view
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = (e) => {
        e.preventDefault();
        const msg = text.trim();
        if (!msg || wsRef.current?.readyState !== WebSocket.OPEN) return;
        wsRef.current.send(JSON.stringify({ message: msg }));
        setText(""); // our own message comes back through the group broadcast
    };

    const formatTime = (ts) =>
        ts ? new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "";

    const badge = {
        connecting: "bg-warning text-dark",
        connected: "bg-success",
        disconnected: "bg-danger",
    }[status];

    return (
        <div className="container mt-4">
            <Link to={`/courses/${slug}`} className="btn btn-link mb-3">
                &larr; Back to course
            </Link>

            <div className="card">
                <div className="card-header d-flex justify-content-between align-items-center">
                    <h4 className="mb-0">Course Discussion</h4>
                    <span className={`badge ${badge}`}>{status}</span>
                </div>

                <div className="card-body" style={{ height: 400, overflowY: "auto" }}>
                    {messages.length === 0 && (
                        <p className="text-muted">No messages yet. Say hello!</p>
                    )}
                    {messages.map((m, i) => {
                        const mine = m.username === me;
                        return (
                            <div
                                key={m.id ?? `live-${i}`}
                                className={`d-flex mb-2 ${mine ? "justify-content-end" : "justify-content-start"}`}
                            >
                                <div
                                    className={`px-3 py-2 rounded ${mine ? "bg-primary text-white" : "bg-light border"}`}
                                    style={{ maxWidth: "75%" }}
                                >
                                    <div className="small fw-bold">
                                        {mine ? "You" : m.username}
                                        <span className="ms-2 fw-normal opacity-75">{formatTime(m.timestamp)}</span>
                                    </div>
                                    <div style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
                                        {m.message}
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                    <div ref={bottomRef} />
                </div>

                <form onSubmit={handleSend} className="card-footer d-flex gap-2">
                    <input
                        type="text"
                        className="form-control"
                        placeholder={status === "connected" ? "Type a message..." : "Connecting..."}
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        maxLength={2000}
                        disabled={status !== "connected"}
                    />
                    <button type="submit" className="btn btn-primary" disabled={status !== "connected" || !text.trim()}>
                        Send
                    </button>
                </form>
            </div>

            {status === "disconnected" && (
                <div className="alert alert-warning mt-3">
                    Connection lost. Your login may have expired, so refresh the page to reconnect.
                </div>
            )}
        </div>
    );
}

export default CourseDiscussion;
import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
import {  Toast, ToastContainer } from "react-bootstrap";

const NotificationContext = createContext(null);

export function NotificationProvider({children}){
    const [Notification, setNotification] = useState(null);

    const notify= useCallback((message, variant="success")=>{
        setNotification({message, variant});
    }, []);

    const clear = useCallback(()=> setNotification(null), [])

    return (
        <NotificationContext.Provider value={{Notification, notify, clear}}>
            {children}
        </NotificationContext.Provider>
    )
}

export function useNotification(){
    const ctx = useContext(NotificationContext);
    if (!ctx) throw new Error("useNotification must be used inside NotificationProvider")
    return ctx;
}

export function NotificationAlert(){
    const { Notification, clear } = useNotification();

    useEffect(()=>{
        if(!Notification) return;
        const timer = setTimeout(clear, 5000);
        return ()=> clearTimeout(timer)
    }, [Notification,  clear])

    if (!Notification) return null;

    return(
        <ToastContainer
        position="top-end"
        className="p-3"
        style={{ position: "fixed", zIndex: 1080 }}
        >
        <Toast
            key={Notification.id}
            show={Notification.show}
            onClose={clear}
            delay={4000}
            autohide
            className={`text-bg-${Notification.variant} border-0`}
        >
            <div className="d-flex">
            <Toast.Body>{Notification.message}</Toast.Body>
            <button
                type="button"
                className="btn-close btn-close-white me-2 m-auto"
                aria-label="Close"
                onClick={clear}
            />
            </div>
        </Toast>
        </ToastContainer>
    )
}


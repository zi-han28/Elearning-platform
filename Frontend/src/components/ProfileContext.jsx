import { createContext, useContext, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";

const ProfileContext = createContext(null);

export function ProfileProvider({ children }) {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const { pathname } = useLocation();

    // Re-check on navigation so login/logout are picked up without a reload.
    useEffect(() => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setProfile(null);
            setLoading(false);
            return;
        }
        if (profile) return;

        setLoading(true);
        api
            .get("/api/profile/")
            .then((res) => setProfile(res.data))
            .catch(() => setProfile(null))
            .finally(() => setLoading(false));
    }, [pathname]);

    return (
        <ProfileContext.Provider value={{ profile, setProfile, loading }}>
            {children}
        </ProfileContext.Provider>
    );
}

export function useProfile() {
    return useContext(ProfileContext);
}

import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const SearchBar = () => {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);
    const navigate = useNavigate();
    const timeoutRef = useRef(null);

    const API_URL = import.meta.env.VITE_API_URL;

    const handleSearch = (e) => {
        const value = e.target.value;
        setQuery(value);

        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }

        if (value.trim() === "") {
            setResults([]);
            return;
        }

        timeoutRef.current = setTimeout(async () => {
            try {
                const response = await axios.get(
                    `${API_URL}/search?query=${encodeURIComponent(value)}`
                );

                if (response.data && Array.isArray(response.data.results)) {
                    setResults(response.data.results);
                } else {
                    setResults([]);
                }
            } catch (err) {
                console.error("Search error:", err);
                setResults([]);
            }
        }, 300);
    };

    const handleSelect = (item) => {
        if (item.type === "user") {
            navigate(`/users/${item.id}`);
        } else if (item.type === "class") {
            navigate(`/classes/${item.id}`);
        } else if (item.type === "plan") {
            navigate(`/plans/${item.id}`);
        }

        setQuery("");
        setResults([]);
    };

    return (
        <div className="search-bar-container">
            <input
                type="text"
                className="search-input glass"
                placeholder="Search members, classes..."
                value={query}
                onChange={handleSearch}
            />

            {results.length > 0 && (
                <div className="search-results glass">
                    {results.map((item) => (
                        <div
                            key={`${item.type}-${item.id}`}
                            className="search-item"
                            onClick={() => handleSelect(item)}
                        >
                            {item.type === "user" && <p>👤 {item.name}</p>}
                            {item.type === "class" && <p>📘 {item.class_name}</p>}
                            {item.type === "plan" && <p>📄 {item.plan_name}</p>}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SearchBar;

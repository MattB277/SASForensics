import React, {useState, useEffect} from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const ReviewDocuments = () => {
    const [documents, setDocuments] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const response = await axios.get("/api/documents-to-review");
                setDocuments(response.data)
            } catch (err) {
                console.error("Error fetching Documents: ", err);
                setError("Failed to load documents.")
            } finally {
                setLoading(false);
            }
        };

        fetchDocuments();
    }, []);

    const filteredDocuments = documents.filter(doc =>
        doc.file.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        doc.case_id.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div style={{ padding: "20px" }}>
            <h2>Analysis to Review</h2>
            <input
                type="text"
                placeholder="Search by document name or case number"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
            />

            {loading ? <p>Loading documents...</p> : null}
            {error ? <p style={{ color: "red" }}>{error}</p> : null}

            <ul>
                {filteredDocuments.length > 0 ? (
                    filteredDocuments.map((doc) => (
                        <li key={doc.file_id} style={{ marginBottom: "10px" }}>
                            <Link to={`/review/${doc.file_id}`}>
                                {doc.file_name} (Case: {doc.case_id})
                            </Link> - Uploaded on {doc.uploaded_at}
                        </li>
                    ))
                ) : (
                    <p>No documents found.</p>
                )}
            </ul>
        </div>
    );
};

export default ReviewDocuments;
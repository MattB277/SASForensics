import React, {useState, useEffect} from "react";
import axios from '../utils/axiosConfig';
import { Link } from "react-router-dom";
import Sidebar from "../components/common/Sidebar";
import '../styles/pages/ReviewDocuments.css';

const ReviewDocuments = () => {
    const [documents, setDocuments] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const response = await axios.get(`/api/documents-to-review/`);
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
        doc.file_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        doc.case_id.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="review-documents">
            <Sidebar />

            <div className="list-documents" style={{ padding: "20px" }}>
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
                                    {doc.file_name} <br/> {doc.case_id}
                                </Link> <span style={{ marginLeft: "50px" }}> - Uploaded on {doc.uploaded_at}</span>
                            </li>
                        ))
                    ) : (
                        <p>No documents found.</p>
                    )}
                </ul>
            </div>
        </div>
    );
};

export default ReviewDocuments;
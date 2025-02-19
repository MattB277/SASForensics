import React, { useState, useEffect} from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import {JSONEditor} from "react-json-editor-viewer";
import FileViewer from "../components/FileViewer";
import Sidebar from "../components/common/Sidebar";
import { useNavigate } from "react-router-dom";
import '../styles/pages/ReviewAnalysis.css';

const ReviewAnalysis = () => {
    const {fileId} = useParams(); // Get file ID from URL params
    const [fileUrl, setFileUrl] = useState("");
    const navigate = useNavigate();
    const [jsonData, setJsonData] = useState({});
    const [reviewed, setReviewed] = useState(false);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const fetchAnalysis = async () => {
            //try to fet analysis through file id
            try{
                const response = await axios.get(`http://localhost:8000/api/api/get-analysis/${fileId}/`);
                setFileUrl(response.data.file_url);
                setJsonData(response.data.json_data);
                setReviewed(response.data.reviewed);
                setLoading(false);
            } catch (error) {
                console.error("Error while fetching analysis", error);
                setLoading(false);
            }
        };

        fetchAnalysis();
    }, [fileId]);

    const handleCancel = () => {
        navigate("/review-documents");
    };

    const handleJsonChange = (key, value, parent, data) => {
        console.log("Key:", key, "Value:", value, "Parent:", parent, "Updated Data:", data);
        setJsonData(data);
    };

    const handleApprove = async () => {
        try {
            await axios.put(`http://localhost:8000/api/api/update-analysis/${fileId}/`, {    // save changes made to JSON
            json_data: jsonData,
            reviewed: true,
            });
            alert("Analysis Approved!")
            setReviewed(true)
        } catch (error) {
            console.error("Error while approving analysis:", error)
        }
    };

    if (loading) return <p>Loading document and analysis...</p>

    return(
        <div className="review-analysis" >
            <Sidebar />
            
            <div className="review-content">
                <div className="file-viewer-container">
                {/* Left side: Display Original File */}
                    <h3>Original Document</h3>
                    <FileViewer fileUrl={fileUrl}/>
                </div>

                <div className="json-editor-container">
                {/* Right side: JSON Analysis Editor */}
                    <h3>JSON Analysis</h3>
                    <div className="scrollable-content">
                        <JSONEditor
                            data={jsonData}
                            onChange={handleJsonChange} // Capture changes
                            editable={true} // Allow editing
                        />
                    </div>
                    <br />
                    <div className="button-container">
                    <button className="approve-button" onClick={handleApprove} disabled={reviewed}>
                        {reviewed ? "Already Approved" : "Approve and save any changes"}
                    </button>
                    <button className="cancel-button" onClick={handleCancel}>Cancel and delete any changes</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ReviewAnalysis;
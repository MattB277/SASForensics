import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const ReviewAnalysis = () => {
    const {fileId} = useParams(); // Get file ID from URL params
    const [fileUrl, setFileUrl] = useState("");
    const [jsonData, setJsonData] = useState({});
    const [reviewed, setReviewed] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
    fetchAnalysis();
    }, []);
    
    const fetchAnalysis = async () => {
        //try to fet analysis through file id
        // set response data
        // handle errors
    }
    }
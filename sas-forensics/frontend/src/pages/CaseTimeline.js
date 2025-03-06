import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import CaseTabs from '../components/CaseTabs';
import axios from '../utils/axiosConfig';
import { Chrono } from 'react-chrono';
import '../styles/pages/CaseDashboard.css';

const Timeline = () => {
  const { caseId } = useParams();
  const [chronoItems, setChronoItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const parseDateTime = (dateStr) => {
    if (!dateStr) return new Date(0);
    const [dateSplit, timeSplit] = dateStr.trim().split(" ");
    const [day, month, year] = dateSplit.split("/").map(Number);
    let hours = 0, minutes = 0;
    if (timeSplit) {
      [hours, minutes] = timeSplit.split(":").map(Number);
    }
    return new Date(year, month - 1, day, hours, minutes);
  };

  useEffect(() => {
    const fetchTimelineData = async () => {
      try {
        const docsResponse = await axios.get(`/cases/${caseId}/files/`);
        const docs = docsResponse.data;
        const json_events = await Promise.all(
          docs.map(async (doc) => {
            const json_url = doc.analysis_json_url;
            if (!json_url) return [];
            try {
              const jsonResponse = await axios.get(json_url);
              return jsonResponse.data.events || [];
            } catch (err) {
              console.error(`Error fetching JSON for ${doc}:`, err);
              return [];
          }
        })
      );
        const eventsArrays = await Promise.all(json_events);
        let allEvents = eventsArrays.flat();
        allEvents.sort((a, b) => parseDateTime(a.time_of_event) - parseDateTime(b.time_of_event));
        const items = allEvents.map((event) => ({
          title: event.time_of_event,
          cardTitle: event.event_type,
          cardSubtitle: event.details
        }));
        setChronoItems(items);
      } catch (err) {
        console.error("Error fetching timeline data:", err);
        setError("Failed to load timeline events.");
      } finally {
        setLoading(false);
      }
    };
    fetchTimelineData();
  }, [caseId]);

  return (
    <div className="case-dashboard">
      <Sidebar />
      <div className="main-content">
        <header className="header">
          <h2>Case Number: {caseId} Timeline</h2>
        </header>
        <CaseTabs caseId={caseId} activeTab="timeline" />
        <div className="case-content">
          <section className="timeline-section">
            {loading ? (
              <p>Loading timeline...</p>
            ) : error ? (
              <p className="error">{error}</p>
            ) : chronoItems.length > 0 ? (
              <Chrono items={chronoItems} mode="VERTICAL_ALTERNATING" />
            ) : (
              <p>No timeline events available.</p>
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default Timeline;

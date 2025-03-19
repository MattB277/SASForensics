import React from "react";
import "../styles/components/DisplayAnalysis.css";
import { Link } from "react-router-dom";

// insert a newline after every ". "
const formatText = (text) => {
  if (text === null || text === undefined) return "";
  return text.toString().replace(/\. /g, ".\n");
};

// Format keys by replacing underscores with spaces and capitalizing each word.
const formatKey = (key) =>
  key
    .replace(/_/g, " ")
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");


const isArrayOfObjects = (val) =>
  Array.isArray(val) && val.length > 0 && typeof val[0] === "object";

// Renders an array of objects as a table. (used for evidence and people)
const renderTable = (data) => {
  const headers = Object.keys(data[0]);
  return (
    <table className="json-table">
      <thead>
        <tr>
          {headers.map((header) => (
            <th key={header}>{formatKey(header)}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {headers.map((header) => (
              <td key={header}>{formatText(row[header])}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const DisplayAnalysis = ({ jsonData, keysToDisplay, reviewed, fileId }) => {
  // If no data exists
  console.log(fileId)
  if (!jsonData || Object.keys(jsonData).length === 0) {
    return <p className="error-message">Error: No analysis found for this document!</p>;
  }

  // If data exists but hasn't been reviewed
  if (!reviewed) {
    return <p className="waiting-message">This document is waiting for review. <Link to={`/review/${fileId}`}> Click here to review it.</Link></p>;
  }

  // Determine which keys to display. If keysToDisplay is "all", use all top-level keys.
  const keys = keysToDisplay === "all" ? Object.keys(jsonData) : keysToDisplay;

  return (
    <div className="display-analysis">
      <p className="disclaimer">
        Disclaimer: This content is AI-generated.
      </p>
      {keys.map((key) => {
        const value = jsonData[key];
        // Skip rendering if value is null, undefined, an empty array, or an empty object.
        if (
          value === null ||
          value === undefined ||
          (Array.isArray(value) && value.length === 0) ||
          (typeof value === "object" && !Array.isArray(value) && Object.keys(value).length === 0)
        ) {
          return null;
        }

        // If the value is an array of objects, render it as a table.
        if (isArrayOfObjects(value)) {
          return (
            <div key={key}>
              <h2>{formatKey(key)}</h2>
              {renderTable(value)}
            </div>
          );
        }


        /*
        This code snippet may have future value but currently it does not improve over the normal key-val pair rendering.
        // If the value is an object (but not an array of objects), render it as a JSON string.
        if (typeof value === "object") {
          return (
            <div key={key}>
              <h2>{formatKey(key)}</h2>
              <pre className="json-pre">{JSON.stringify(value, null, 2)}</pre>
            </div>
          );
        }
        */


        // Otherwise, render as a normal key-value pair.
        return (
          <div key={key}>
            <h2>{formatKey(key)}</h2>
            <p className="json-paragraph">{formatText(value)}</p>
          </div>
        );
      })}
    </div>
  );
};

export default DisplayAnalysis;

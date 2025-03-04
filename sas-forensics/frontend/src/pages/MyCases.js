import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import '../styles/pages/MyCases.css';
import axios from '../utils/axiosConfig';

const MyCases = () => {
    const [cases, setCases] = useState([]);
    const [filteredCases, setFilteredCases] = useState([]);
    const [error, setError] = useState(null);
    const [sortField, setSortField] = useState('case_number');
    const [sortOrder, setSortOrder] = useState('asc');
    const [filters, setFilters] = useState({
        location: '',
        crimeType: '',
        status: '',
        dateRange: { start: '', end: '' },
    });

    useEffect(() => {
        axios
            .get('/cases/')
            .then((response) => {
                setCases(response.data);
                setFilteredCases(response.data);
            })
            .catch(() => setError('Failed to load cases.'));
    }, []);

    const getStatusIcon = (status) => {
        const statusIcons = {
            new_evidence: require('../assets/ic_case_red.png'),
            new_collaboration: require('../assets/ic_case_yellow.png'),
            no_changes: require('../assets/ic_case_green.png'),
        };
        return statusIcons[status] || statusIcons.no_changes;
    };

    const handleSort = (field, order) => {
        const sortedCases = [...filteredCases].sort((a, b) => {
            if (order === 'asc') {
                return a[field]?.toString().localeCompare(b[field]?.toString());
            } else {
                return b[field]?.toString().localeCompare(a[field]?.toString());
            }
        });
        setFilteredCases(sortedCases);
        setSortField(field);
        setSortOrder(order);
    };

    const applyFilters = () => {
        const { location, crimeType, status, dateRange } = filters;
        let result = [...cases];

        if (location) {
            result = result.filter((c) =>
                c.location?.toLowerCase().includes(location.toLowerCase())
            );
        }
        if (crimeType) {
            result = result.filter((c) =>
                c.type_of_crime?.toLowerCase().includes(crimeType.toLowerCase())
            );
        }
        if (status) {
            result = result.filter((c) => c.status === status);
        }
        if (dateRange.start && dateRange.end) {
            const startDate = new Date(dateRange.start);
            const endDate = new Date(dateRange.end);
            result = result.filter((c) => {
                const caseDate = new Date(c.date_opened);
                return caseDate >= startDate && caseDate <= endDate;
            });
        }

        setFilteredCases(result);
    };

    const handleFilterChange = ({ target: { name, value } }) => {
        if (name === 'start' || name === 'end') {
            setFilters((prev) => ({
                ...prev,
                dateRange: { ...prev.dateRange, [name]: value },
            }));
        } else {
            setFilters((prev) => ({ ...prev, [name]: value }));
        }
    };

    return (
        <div className="my-cases">
            <Sidebar />
            <div className="main-content">
                <h2>My Cases</h2>
                {error ? (
                    <p className="error">{error}</p>
                ) : (
                    <>
                        <div className="filters">
                            <input
                                type="text"
                                name="location"
                                placeholder="Filter by Location"
                                value={filters.location}
                                onChange={handleFilterChange}
                            />
                            <input
                                type="text"
                                name="crimeType"
                                placeholder="Filter by Crime Type"
                                value={filters.crimeType}
                                onChange={handleFilterChange}
                            />
                            <select name="status" value={filters.status} onChange={handleFilterChange}>
                                <option value="">Filter by Status</option>
                                <option value="new_evidence">New Evidence</option>
                                <option value="new_collaboration">New Collaboration</option>
                                <option value="no_changes">No Changes</option>
                            </select>
                            <div className="date-range">
                                <label>
                                    Date Opened From:
                                    <input
                                        type="date"
                                        name="start"
                                        value={filters.dateRange.start}
                                        onChange={handleFilterChange}
                                    />
                                </label>
                                <label>
                                    Date Opened To:
                                    <input
                                        type="date"
                                        name="end"
                                        value={filters.dateRange.end}
                                        onChange={handleFilterChange}
                                    />
                                </label>
                            </div>
                            <button onClick={applyFilters}>Apply Filters</button>
                        </div>

                        <div className="sort-filter">
                            <label htmlFor="sortField">Sort By:</label>
                            <select
                                id="sortField"
                                value={sortField}
                                onChange={(e) => handleSort(e.target.value, sortOrder)}
                            >
                                <option value="case_number">Case Number</option>
                                <option value="type_of_crime">Crime Type</option>
                                <option value="location">Location</option>
                                <option value="date_opened">Date Opened</option>
                            </select>
                            <button onClick={() => handleSort(sortField, 'asc')}>Ascending</button>
                            <button onClick={() => handleSort(sortField, 'desc')}>Descending</button>
                        </div>

                        <div className="case-items-grid">
                            {filteredCases.map((caseItem) => (
                                <div key={caseItem.case_id} className="case-item">
                                    <img
                                        src={getStatusIcon(caseItem.status)}
                                        alt="Case Icon"
                                        className="case-icon"
                                    />
                                    <p><strong>Case Number:</strong> {caseItem.case_number}</p>
                                    <p><strong>Type of Crime:</strong> {caseItem.type_of_crime}</p>
                                    <p><strong>Location:</strong> {caseItem.location}</p>
                                    <p>
                                        <strong>Status:</strong>{' '}
                                        <span
                                            className={
                                                caseItem.status === 'new_evidence'
                                                    ? 'status-red'
                                                    : caseItem.status === 'new_collaboration'
                                                    ? 'status-orange'
                                                    : 'status-green'
                                            }
                                        >
                                            {caseItem.status.replace('_', ' ')}
                                        </span>
                                    </p>
                                    <Link to={`/case-dashboard/${caseItem.case_id}`} className="view-case-link">
                                        View Case
                                    </Link>
                                </div>
                            ))}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default MyCases;

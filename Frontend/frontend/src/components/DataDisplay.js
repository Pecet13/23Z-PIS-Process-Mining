import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function DataDisplay() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('https://pis2023-pm.azurewebsites.net/')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
      console.log(data)
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h1 className="text-2xl font-semibold mb-4">Received Data</h1>
      <ul className="list-disc list-inside">
        {data.map((item, index) => (
          <li key={index} className="text-gray-700">{JSON.stringify(item)}</li>
        ))}
      </ul>
      <div>
          <Link to="/">
          <button className="custom-btn">
            Go Home
          </button>
        </Link>
        </div>

    </div>

  );
}

export default DataDisplay;

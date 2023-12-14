import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="text-center mt-10">
      <h1 className="text-4xl font-bold mb-6">Hello World</h1>
      <Link to="/data">
        <button className="custom-btn">
          Show Data
        </button>
      </Link>
    </div>
  );
}

export default Home;

import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import DataDisplay from './components/DataDisplay';
import Home from './components/Home'; 
import './tailwind.css';

function App() {
  return (

    <Router>
      <div className="App min-h-screen bg-gray-100">
        <header className="bg-blue-600 text-white p-4 shadow-md">
        <nav className="container mx-auto">
    <ul className="flex justify-center space-x-6 list-none">
      <li className="hover:underline">
        <Link to="/">Home</Link>
      </li>
      <li className="hover:underline">
        <Link to="/data">Show Data</Link>
      </li>
    </ul>
  </nav>
        </header>


        <div className="text-center my-10">
  <h1 className="text-5xl font-extrabold text-blue-600">
    Data Miner
  </h1>
  <p className="text-base text-gray-600">
    perfect place for analyze mining data
  </p>
</div>

        <main className="container mx-auto py-8">
          <Routes>
            <Route path="/" element={<Home />} exact />
            <Route path="/data" element={<DataDisplay />} />
          </Routes>
        </main>
      </div>
    </Router>

  );
}

export default App;

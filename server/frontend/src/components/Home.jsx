import React from 'react';
import Header from './Header/Header';

const Home = () => {
  return (
    <div>
      <Header />
      <div style={{ margin: '20px', textAlign: 'center' }}>
        <h1>Welcome to Dealerships</h1>
        <p>Find the best car dealers and browse their inventory.</p>
        <a href="/dealers" className="btn" style={{backgroundColor: 'aqua', margin: '10px'}}>View Dealerships</a>
      </div>
    </div>
  );
};

export default Home;
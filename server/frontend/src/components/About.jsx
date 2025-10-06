import React from 'react';
import Header from './Header/Header';

const About = () => {
  return (
    <div>
      <Header />
      <div style={{ margin: '20px' }}>
        <h1>About Dealerships</h1>
        <p>Welcome to our car dealership platform. We provide comprehensive information about car dealers and their inventory.</p>
        <a href="/dealers" className="btn btn-primary">View Dealerships</a>
      </div>
    </div>
  );
};

export default About;
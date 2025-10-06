import React from 'react';
import Header from './Header/Header';

const Contact = () => {
  return (
    <div>
      <Header />
      <div style={{ margin: '20px' }}>
        <h1>Contact Us</h1>
        <p>Get in touch with us for any questions about our dealership platform.</p>
        <a href="/dealers" className="btn btn-primary">View Dealerships</a>
      </div>
    </div>
  );
};

export default Contact;
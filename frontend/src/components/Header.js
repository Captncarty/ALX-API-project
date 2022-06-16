import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {
  navTo(uri) {
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <div className='App-header'>
        <h1
          onClick={() => {
            this.navTo('');
          }}
        >
          Udacitrivia
        </h1>
        <h2
          onClick={() => {
            this.navTo('');
          }}
          className="nav-item"
        >
          List
        </h2>
        <h2
          onClick={() => {
            this.navTo('/add');
          }}
          className="nav-item"
        >
          Add
        </h2>
        <h2
          onClick={() => {
            this.navTo('/play');
          }}
          className="nav-item"
        >
          Play
        </h2>
      </div>
    );
  }
}

export default Header;

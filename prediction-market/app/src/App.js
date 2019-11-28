import React, { Component } from "react";
import { DrizzleProvider } from "@drizzle/react-plugin";
import { LoadingContainer } from "@drizzle/react-components";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import drizzleOptions from "./drizzleOptions";
import { MainContainer, AboutContainer } from "./MyContainers";
import './index.css';

class App extends Component {
  render() {
    return (
      <Router>
        <div style={headerStyle}>
          <h1 style={headingStyle}>
            CHARJE
          </h1>
          <Link to="/about" style={navStyle}>
            <h4 style={headingStyle}>
              ABOUT
            </h4>
          </Link>
          <Link to="/" style={navStyle}>
            <h4 style={headingStyle}>
              DASHBOARD
            </h4>
          </Link>
        </div>

        <Switch>
          <Route exact path="/">
            <Dashboard />
          </Route>
          <Route path="/about">
            <About />
          </Route>
        </Switch>
      </Router>
    );
  }
}

function Dashboard() {
  return (
    <DrizzleProvider options={drizzleOptions}>
      <LoadingContainer>
        <MainContainer />
      </LoadingContainer>
    </DrizzleProvider>
  );
}

function About() {
  return (
    <DrizzleProvider options={drizzleOptions}>
      <LoadingContainer>
        <AboutContainer />
      </LoadingContainer>
    </DrizzleProvider>
  );
}

const headerStyle = {
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'center',
  background: 'linear-gradient(to right bottom, #4e036e, #d91a1a)',
  borderRadius: 0,
  paddingLeft: 50,
};

const navStyle = {
  textDecoration: 'none'
};

const headingStyle = {
  fontFamily: 'Poppins',
  color: 'white',
  paddingLeft: 55
};

export default App;

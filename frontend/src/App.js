import React from 'react'
import { Container } from 'react-bootstrap';
import { HashRouter, Route } from "react-router-dom"
import HomeScreen from "./screens/HomeScreen"
import NavBar from "./components/NavBar"
import Footer from "./components/Footer"
//import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <HashRouter>
      <NavBar/>
      <main classname="py-3">
        <Container>
          <Route path="/" component={HomeScreen} exact/>
        </Container>
      </main>
      <Footer/>
    </HashRouter>
  );
}

export default App;

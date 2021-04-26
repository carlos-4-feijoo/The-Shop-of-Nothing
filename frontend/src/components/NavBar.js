import React from 'react'
import { Navbar, Nav, Container, Row, Col } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faShoppingCart } from '@fortawesome/free-solid-svg-icons'
import { faUser } from '@fortawesome/free-solid-svg-icons'

//style={{marginLeft:"36.5%"}}
function NavBar() {
    return (
        <header>
            <Navbar bg="light" variant="light" expand="lg" style={{padding:0}} collapseOnSelect>

                    <Row style={{backgroundColor:"white", width:"100%", margin:0}} className="align-items-center" >            
                        <Col xs={{span:12}} sm={{span:5, order:"first"}}>
                            Here will be Search bar
                        </Col>
                        <Col xs={{span:12, order:"first"}} sm={{span:2}}>
                            
                            <LinkContainer to='/' style={{margin:"5px"}}>
                                <Navbar.Brand>
                                    <p style={{fontSize: "1rem", margin: 0}}><small>The Shop of</small></p> 
                                    <h3 style={{fontSize: "1.6rem", margin: 0}}><strong>Nothing</strong></h3>
                                </Navbar.Brand>
                            </LinkContainer>
                        </Col>      
                        <Col xs={{span:12, order:"last"}} sm={{span:3, offset:2}}>   
                            <Nav className="justify-content-center" style={{flexDirection:"row"}}>
                                <LinkContainer to='/' style={{margin:"0px 10px 0px 10px"}}>
                                    <Nav.Link><FontAwesomeIcon icon={faUser} /></Nav.Link>
                                </LinkContainer>
                                <LinkContainer to='/' style={{margin:"0px 10px 0px 10px"}}>
                                    <Nav.Link><FontAwesomeIcon icon={faShoppingCart}/></Nav.Link>
                                </LinkContainer>
                            </Nav>                        
                        </Col>    
                    </Row>                    
                
            </Navbar>
            <Navbar style={{backgroundColor:"#100f11", paddingTop:0, paddingBottom:0}}  variant="dark" expand="sm" collapseOnSelect>
                <Container >
                    <Navbar.Toggle className="custom-toggler" aria-controls="responsive-navbar-nav" />
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav style={{fontSize: "0.8rem"}}>
                            <LinkContainer to='/'>
                                <Nav.Link>Promotions</Nav.Link>
                            </LinkContainer>
                            <LinkContainer to='/'>
                                <Nav.Link>Categories</Nav.Link>
                            </LinkContainer>
                            <LinkContainer to='/'>
                                <Nav.Link>Browsing History</Nav.Link>
                            </LinkContainer>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </header>

    )
}

export default NavBar

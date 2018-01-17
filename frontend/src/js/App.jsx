import React, {Component} from 'react';
import {Col, Row, Grid} from 'react-bootstrap';
import BestPriceFinder from "./components/BestPriceFinder";
import '../styles/App.less';

class App extends Component {
  render() {
    return (
        <div className="application-root">
            <Grid>
                <Row>
                    <Col lg={4} md={4} xs={4}/>
                    <Col lg={4} md={4} xs={4}>
                        <BestPriceFinder/>
                    </Col>
                    <Col lg={4} md={4} xs={4}/>
                </Row>
            </Grid>
        </div>
    );
  }
}

export default App;

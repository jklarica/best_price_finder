import React, {Component} from 'react';
import { Button, ButtonGroup, Col, ControlLabel, DropdownButton, FormControl, FormGroup, MenuItem, Row } from 'react-bootstrap';
import axios from 'axios';
import '../../styles/components/BestPriceFinder.less';

/**
 * Component which renders a small widget, used retrieve best price based on provided start date,
 * number of nights and product type
 *
 * Improvement ideas:
 *  1.) Security (i.e. add CSRF token to each Ajax call)
 *  2.) Pass environment-dependant variables from webpack
 *  3.) Better error handling and messaging
 *  4.) Better input validation
 *  5.) Move product filtering to the server-side (i.e. if published or not)
 *  6.) Datepicker is missing
 *  7.) Localization
 *  8.) Add linters for ES and React
 *  8.) Etc.
 *
 */
class BestPriceFinder extends Component {
    constructor(props) {
        super(props);
        this.state = {
            products: [],                                  // Available products
            selectedProduct: { value: null, valid: null }, // Selected product
            startDate: { value: null, valid: null },       // Start dates
            numberOfNights: { value: null, valid: null },  // How many nights to stay
            error: null,                                   // Used to indicate that something went wrong with the API request
            isLoading: false,                              // Used to indicate that we're waiting response from the server
            bestOffer: null                                // Best offer; contains price, currency and a combination of pricing blocks
        };
    }

    // Should be defined via webpack
    static CONFIG = {
        API_SERVER: 'http://127.0.0.1:8000'
    };

    componentDidMount() {
        this.getProducts();
    }

    handleProductSelect(product) {
        this.updateValidateInput(
            'selectedProduct',
            this.state.selectedProduct,
            product,
            function(value) { return value !== null; }
        );
    }

    handleStartDateChange(evt) {
        this.updateValidateInput(
            'startDate',
            this.state.startDate,
            evt.target.value,
            BestPriceFinder.isValidDate
        );
    }

    handleNumberOfNightsChange(evt) {
        this.updateValidateInput(
            'numberOfNights',
            this.state.numberOfNights,
            evt.target.value,
            function(value) { return value && !isNaN(value); }
        )
    }

    handleGetBestPrice() {
        let self = this;
        self.setState({ isLoading: true, error: null });

        let resourceUrl = BestPriceFinder.fillQueryParams(
            BestPriceFinder.CONFIG.API_SERVER + '/best_price/',
            {
                start_date: this.state.startDate.value,
                num_nights: this.state.numberOfNights.value,
                product_id: this.state.selectedProduct.value
            }
        );

        this.getBestPrice(resourceUrl);
	}

    renderProductItems() {
        return this.state.products.map((product) =>
            {
                // Might be better to filter in the backend
                if (product.published === true) {
                    return (
                        <MenuItem key={product.id} eventKey={product.id} active={product.id === this.state.selectedProduct.value}>
                            {product.name}
                        </MenuItem>
                    );
                }
            }
        )
    }

    renderProductSelectionControl() {
        let selectedProduct = this.state.selectedProduct.value ? this.state.products.find(product => product.id === this.state.selectedProduct.value).name : "Name";
        return (
            <Row className="grid-row">
                <FormGroup controlId="productSelectionForm" validationState={this.state.selectedProduct.valid ? 'success' : 'error'}>
                    <Col md={4}>
                         <ControlLabel className="product-label">Product</ControlLabel>
                    </Col>
                    <Col md={8}>
                        <ButtonGroup bsClass="product-button-group">
                            <DropdownButton
                                id="product-dropdown"
                                title={selectedProduct}
                                onSelect={this.handleProductSelect.bind(this)}
                            >
                                {this.renderProductItems()}
                            </DropdownButton>
                        </ButtonGroup>
                    </Col>
                </FormGroup>
            </Row>
        );
    }

    renderStartDateControl() {
        return (
            // Missing a datepicker like this one: https://github.com/Hacker0x01/react-datepicker
            <Row className="grid-row">
                <FormGroup controlId="startDateForm" validationState={this.state.startDate.valid ? 'success' : 'error'}>
                    <Col md={4}>
                        <ControlLabel className="start-date-label">Start Date</ControlLabel>
                    </Col>
                    <Col md={8}>
                        <FormControl
                            type="text"
                            value={this.state.value}
                            placeholder="YYYY-MM-DD"
                            onChange={this.handleStartDateChange.bind(this)}
                        />
                    </Col>
                </FormGroup>
            </Row>
        );
    }

    renderNumberOfNightsControl() {
        return (
            <Row className="grid-row">
                <FormGroup controlId="numberOfNightsForm" validationState={this.state.numberOfNights.valid ? 'success' : 'error'}>
                    <Col md={4}>
                        <ControlLabel className="num-nights-label">Nights</ControlLabel>
                    </Col>
                    <Col md={8}>
                        <FormControl
                            type="text"
                            value={this.state.value}
                            onChange={this.handleNumberOfNightsChange.bind(this)}
                        />
                    </Col>
                </FormGroup>
            </Row>
        );
    }

    renderGetBestPriceControl() {
        let isLoading = this.state.isLoading;
        let inputParamsValid = this.state.startDate.valid && this.state.numberOfNights.valid && this.state.selectedProduct.valid;
        let message;

        if (this.state.error !== null) {
            message = (<span className="error">{this.state.error}</span>);
        } else {
            if (this.state.bestOffer !== null) {
                if (Object.keys(this.state.bestOffer).length > 0) {
                    message = (<span className="success">Best Price: {this.state.bestOffer.price} {this.state.bestOffer.currency}</span>);
                } else {
                    message = (<span className="none">Haven't found any offers</span>);
                }
            } else {
                message = (<span/>);
            }
        }

        return (
            <Row className="grid-row">
                <FormGroup controlId="bestPriceForm">
                    <Row className="grid-row">
                        <Col md={4} className="calculate">
                            <Button
                                bsStyle="primary"
                                disabled={isLoading || !inputParamsValid}
                                onClick={!isLoading ? this.handleGetBestPrice.bind(this) : null}
                            > {isLoading ? 'Loading...' : 'Calculate'}
                            </Button>
                        </Col>
                        <Col md={8} className="calculate">
                            <div className="best-price"> {message} </div>
                        </Col>
                    </Row>
                </FormGroup>
            </Row>
        );
    }

    /**
     * Clone previous state, set new values and update it
     */
    updateValidateInput(property, previousState, value, validator) {
        this.setState({[property]: { ...previousState, value: value, valid: validator(value)}});
    }

    /**
     * Retrieve products from the endpoint
     */
    getProducts() {
        let self = this;
        axios.get(BestPriceFinder.CONFIG.API_SERVER + '/product/')
            .then(function (response) {
                self.setState({ products: response.data });
            })
            .catch(function (error) {
                self.setState({error: "Unable to retrieve products!"})
            });
    }

    /**
     * Retrieve best price from the endpoint
     */
    getBestPrice(resourceUrl) {
        let self = this;
        axios.get(resourceUrl)
            .then(function (response) {
                self.setState({ bestOffer: response.data, isLoading: false });
            })
            .catch(function (error) {
                // Show error message in the UI
                self.setState(
                    {
                        error: "Unable to retrieve the best price!",
                        isLoading: false
                    }
                )
            });
    }

    /**
     * Produce full GET request URL
     */
    static fillQueryParams(URI, params) {
      let query = [];
      Object.keys(params).forEach(
        function (paramName) {
          let paramValue = params[paramName];
          if (Array.isArray(paramValue)) {
            paramValue.forEach(function (value) {
              query.push(paramName + '=' + value);
            });
          } else {
            query.push(paramName + '=' + paramValue);
          }
        });
      return URI + ((URI.toString().indexOf('?') < 0) ? '?' : '&') + query.join('&');
    };

    /**
     * Check if the date input is valid (very basic)
     */
    static isValidDate(dateString) {
        if (!dateString) return false;
        let dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if(!dateString.match(dateRegex)) return false;
        let date = new Date(dateString);

        return !(!date.getTime() && date.getTime() !== 0);
    }

    render() {
        return (
            <div className="price-finder-app">
                <div className="header">
                  <h3 className="title">Best Price Finder</h3>
                </div>
                <div className="grid">
                    {this.renderProductSelectionControl()}
                    {this.renderStartDateControl()}
                    {this.renderNumberOfNightsControl()}
                    {this.renderGetBestPriceControl()}
                </div>
            </div>
        );
    }
}

export default BestPriceFinder;

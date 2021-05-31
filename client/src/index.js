import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'

const API_URL = process.env.REACT_APP_API_URL

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      fruits: [],
      predict_response: null,
      model_input: `{"data":["Hello model"]}`
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    fetch(API_URL.concat("/fruits"))
      .then(async res => await res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            fruits: result.items,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  handleSubmit(event) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: this.state.model_input
    };
    fetch(API_URL.concat("/predict"), requestOptions)
      .then(async response => {
        // const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = await response.json();
        // check for error response
        if (!response.ok) {
          // get error message from body or default to response status
          const error = (data && data.message) || response.status;
          return Promise.reject(error);
        }
        this.setState({ predict_response: data })
      })
      .catch(error => {
        this.setState({ error });
        console.error('There was an error!', error);
      });

      event.preventDefault();
  }

  handleChange(event) {
    this.setState({ model_input: event.target.value });
  }

  render() {
    const { error, isLoaded, fruits, predict_response} = this.state;
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (        
        <div>
          <header><b>ML Boilerplate Machine Learning Template</b></header>
          <p>
            <label>
            Fruits (Postgres integration):
            </label>
            <ul>
              {fruits.map(item => (
                <li key={item.name}>
                  {item.name}: {item.price}$
                </li>
              ))}
            </ul>
          </p>

          <form onSubmit={this.handleSubmit}>
            <label>
              Model input:
              <br/>
              <textarea name="model_input" value={this.state.model_input} onChange={this.handleChange} />
            </label>
            <br/>
            <input type="submit" value="Predict" />
          </form>

          <p>
            <label>
              Prediction result:
              <br/>
              {predict_response}
            </label>
          </p>

        </div>
      );
    }
  }
}


ReactDOM.render(
  <App/>,
  document.getElementById('root')
);
import React, { useState, useEffect } from 'react';
import './index.css'

const API_URL = process.env.REACT_APP_API_URL;

const Error = (props) => {
  return <div style={{ color: 'red' }}>Error: {props.message}</div>;
}
const Loading = () => {
  return <div>Loading...</div>;
}
const ItemList = (props) => {
  return (
    <ul>
      {props.items.map(item => (
        <li key={item.name}>
          {item.name}: {item.price}
        </li>
      ))}
    </ul>
  )
}

const AddItem = (props) => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');

  const { setError, setFetchNewItems } = props;

  const nameChange = (event) => setName(event.target.value.trim());
  const priceChange = (event) => setPrice(event.target.value.trim());

  const handleSubmit = (event) => {
    event.preventDefault();
    setError(null);
    const submitBody = {};
    submitBody.name = name;
    submitBody.price = price;
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(submitBody)
    };
    fetch(`${API_URL}/fruits`, requestOptions)
      .then(async response => {
        // const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = await response.json();
        // check for error response
        if (!response.ok) {
          // get error message from body or default to response status
          const error = (data && data.message) || response.status;
          setError(`Error when calling ${API_URL}/fruits`);
          console.error(`Error when calling ${API_URL}/fruits`, error);
        } else {
          console.log(data);
          setFetchNewItems(data);
        }
      })
      .catch(error => {
        setError(`Error when calling ${API_URL}/fruits`);
        console.error(`Error when calling ${API_URL}/fruits`, error);
      });
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="name"
          value={name}
          onChange={nameChange}
        />
        <input
          type="number"
          placeholder="price"
          value={price}
          onChange={priceChange}
        />
        <input type="submit" value="AddItem" />
      </form>
    </div>
  )
}
const SubmitForm = (props) => {
  console.log(props);

  const { setError, setPredict, modelInput, setModelInput } = props;

  const handleSubmit = (event) => {
    event.preventDefault();
    setError(null);
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: modelInput
    };
    fetch(`${API_URL}/predict`, requestOptions)
      .then(async response => {
        // const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = await response.json();
        // check for error response
        if (!response.ok) {
          // get error message from body or default to response status
          const error = (data && data.message) || response.status;
          setError(`Error when calling ${API_URL}/predict`);
          console.log(`Error when calling ${API_URL}/predict`, error);
        } else {
          console.log(data);
          setPredict(data);
        }
      })
      .catch(error => {
        setError(`Error when calling ${API_URL}/predict`);
        console.log(`Error when calling ${API_URL}/predict`, error);
      });
  }

  const handleChange = (event) => {
    setModelInput(event.target.value);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Model input:
        <br/>
        <textarea name="model_input" value={modelInput} onChange={handleChange} />
      </label>
      <br/>
      <input type="submit" value="Predict" />
    </form>
  )
}

const App = () => {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const [fetchNewItems, setFetchNewItems] = useState(null);
  const [predict_response, setPredict_response] = useState([]);
  const [model_input, setModel_input] = useState('{"data":["Hello model"]}');

  useEffect(() => {
    fetch(`${API_URL}/fruits`)
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result)
          setItems(result.items);
          setIsLoaded(true);
        },
        (error) => {
          setError(`Error when calling ${API_URL}/fruits`);
          console.error(`Error when calling ${API_URL}/fruits`, error);
          setIsLoaded(true);
        }
      )
      .catch(error => {
        setError(`Error when calling ${API_URL}/fruits`);
        console.error(`Error when calling ${API_URL}/fruits`, error);
      });
  }, [fetchNewItems]);

  return (
    <div>
      <header><b>ML Boilerplate Machine Learning Template</b></header>
      {error ? <Error message={error} /> : null }
      {!error & !isLoaded ? 
        <Loading /> 
        : 
        <>
          <div>
            <label>Fruits (Postgres integration):</label>
            <ItemList items={items} />
          </div>
          <AddItem 
            setError={setError}
            setFetchNewItems={setFetchNewItems}
          />
          <br />
          <SubmitForm 
            modelInput={model_input}
            setPredict={setPredict_response}
            setModelInput={setModel_input}
            setError={setError}
          />
          <p>
            <label>
              Prediction result:
              <br/>
              {predict_response}
            </label>
          </p>
        </>
      }
    </div>
  )
}

export default App;
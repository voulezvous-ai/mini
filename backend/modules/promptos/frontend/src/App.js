import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  // Essa chave deve corresponder à variável API_KEY definida no .env do backend
  const API_KEY = 'your_api_key';  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(
        'http://localhost:8000/prompt',
        { prompt },
        {
          headers: {
            'x-api-key': API_KEY,
            'Content-Type': 'application/json'
          }
        }
      );
      setResponse(res.data.message);
    } catch (error) {
      console.error(error);
      setResponse('Erro ao processar o prompt.');
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>PromptOS Frontend</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="4"
          cols="50"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Digite seu prompt aqui..."
        ></textarea>
        <br />
        <button type="submit" disabled={loading}>
          {loading ? 'Processando...' : 'Enviar Prompt'}
        </button>
      </form>
      <div style={{ marginTop: '20px' }}>
        <h3>Resposta:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
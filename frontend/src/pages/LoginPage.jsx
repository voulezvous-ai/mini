import React, { useState } from 'react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    // Simulação de login: em produção, faça chamada à API
    if(email === 'admin@example.com' && senha === 'changeme') {
      window.location.href = '/app';
    } else {
      alert('Credenciais inválidas');
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '4rem' }}>
      <h1>Login</h1>
      <form onSubmit={handleLogin}>
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required style={{ margin: '0.5rem', padding: '0.5rem' }} />
        <input type="password" placeholder="Senha" value={senha} onChange={e => setSenha(e.target.value)} required style={{ margin: '0.5rem', padding: '0.5rem' }} />
        <button type="submit" style={{ padding: '0.5rem 1rem', margin: '0.5rem' }}>Entrar</button>
      </form>
    </div>
  );
}
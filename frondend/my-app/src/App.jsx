
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { LoginForm } from './components/LoginForms';
import { Home } from './components/Home';
import AIDocumentForm from './components/AIDocumentForm';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/home" element={<Home/>} />
        <Route path="/data" element={<AIDocumentForm/>} />
      </Routes>
    </Router>
  );
}

export default App;

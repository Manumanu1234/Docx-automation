import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AIDocumentForm from './AIDocumentForm';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../styles/home.css';
export function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [aiDetails, setAIDetails] = useState(null);
  const navigate = useNavigate();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    if (selectedFile.type !== "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
      toast.error("Only .docx files are accepted.");
      return;
    }
    setIsSubmitting(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      const response = await axios.post('http://localhost:8000/sample_docx_editing/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.data && response.data.result === 'success') {
        console.log(response.data)
        toast.success('Document submitted successfully!');
        setSelectedFile(null);
        if (response.data.details) {
          setAIDetails(response.data.details);
          navigate('/data');
        }
      } else {
        toast.error('Upload failed.');
      }
    } catch (error) {
      if (error.response && error.response.data && error.response.data.error) {
        toast.error(error.response.data.error);
      } else {
        toast.error('An error occurred while uploading.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="home-container" style={{ paddingTop: 40 }}>
      {isSubmitting && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0,0,0,0.35)',
          zIndex: 9999,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <div className="amazing-loader" style={{ marginBottom: 24 }}>
            <svg width="80" height="80" viewBox="0 0 50 50">
              <circle cx="25" cy="25" r="20" fill="none" stroke="#10b981" strokeWidth="5" strokeDasharray="31.4 31.4" strokeLinecap="round">
                <animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite" />
              </circle>
              <circle cx="25" cy="25" r="12" fill="none" stroke="#3b82f6" strokeWidth="4" strokeDasharray="18.8 18.8" strokeLinecap="round">
                <animateTransform attributeName="transform" type="rotate" from="360 25 25" to="0 25 25" dur="1.2s" repeatCount="indefinite" />
              </circle>
            </svg>
          </div>
          <div style={{ color: '#fff', fontSize: 22, fontWeight: 600, letterSpacing: 1, textShadow: '0 2px 8px #000' }}>
            AI is Extracting Details...
          </div>
        </div>
      )}
      <ToastContainer position="top-right" autoClose={3000} hideProgressBar={false} newestOnTop closeOnClick pauseOnFocusLoss draggable pauseOnHover />
      <div className="home-header">
        <div className="avatar-container">
          <img 
            src="https://images.pexels.com/photos/771742/pexels-photo-771742.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&fit=crop&crop=face" 
            alt="User Avatar" 
            className="avatar"
          />
          <div className="avatar-status"></div>
        </div>
      </div>

      <div className="home-content">
        {aiDetails ? (
          <AIDocumentForm
            details={aiDetails}
            onSuccess={(newDetails) => {
              if (newDetails && typeof newDetails === 'object') {
                setAIDetails(newDetails);
              } else {
                setAIDetails(null);
              }
            }}
          />
        ) : (
          <div className="upload-card">
            <div className="upload-header">
              <h1>Submit Your Template</h1>
              <p>Upload your sample template file to get started</p>
            </div>
            <form onSubmit={handleSubmit} className="upload-form">
              <div 
                className={`upload-area ${dragActive ? 'drag-active' : ''} ${selectedFile ? 'has-file' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                {!selectedFile ? (
                  <>
                    <div className="upload-icon">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7,10 12,15 17,10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                    </div>
                    <h3>Drop your template here</h3>
                    <p>or click to browse files</p>
                    <input
                      type="file"
                      onChange={handleFileSelect}
                      accept=".docx"
                      className="file-input"
                    />
                  </>
                ) : (
                  <div className="file-preview">
                    <div className="file-info">
                      <div className="file-icon">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                        </svg>
                      </div>
                      <div className="file-details">
                        <h4>{selectedFile.name}</h4>
                        <p>{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                      </div>
                    </div>
                    <button type="button" onClick={removeFile} className="remove-file">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                      </svg>
                    </button>
                  </div>
                )}
              </div>
              <button 
                type="submit" 
                className={`submit-btn ${isSubmitting ? 'submitting' : ''}`}
                disabled={!selectedFile || isSubmitting}
              >
                <span>Submit Template</span>
                <div className="submit-loader"></div>
                <svg className="submit-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22,2 15,22 11,13 2,9 22,2"/>
                </svg>
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
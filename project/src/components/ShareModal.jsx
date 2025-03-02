import { useState, useEffect, useRef } from 'react';
import apiService from '../services/api';
import '../styles/Modal.css';

function ShareModal({ isOpen, onClose }) {
  const [username, setUsername] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const shareUrlRef = useRef(null);
  
  // Generate share URL with the current username as referrer
  const shareUrl = `${window.location.origin}?referrer=${encodeURIComponent(username)}`;

  useEffect(() => {
    if (isOpen) {
      fetchUserData();
    }
  }, [isOpen]);

  const fetchUserData = async () => {
    setIsLoading(true);
    try {
      const userData = await apiService.getUserProfile();
      setUsername(userData.username);
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyLink = () => {
    if (shareUrlRef.current) {
      shareUrlRef.current.select();
      document.execCommand('copy');
      setCopied(true);
      
      // Reset copied state after 2 seconds
      setTimeout(() => {
        setCopied(false);
      }, 2000);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          text: `Globetrotter Challenge!! ${username} has challenged you to beat their score in Globetrotter! Can you identify more destinations? Visit ${shareUrl} to play now!`,
        });
      } catch (error) {
        console.error('Error sharing:', error);
      }
    } else {
      handleCopyLink();
      alert(`Share this link with your friends: <a href="${shareUrl}" target="_blank">${shareUrl}</a>`);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>×</button>
        
        <h2 className="modal-title">Challenge Your Friends</h2>
        
        {isLoading ? (
          <div className="modal-loading">
            <div className="spinner"></div>
            <p>Loading share info...</p>
          </div>
        ) : (
          <>
            <div className="share-message">
              <p>Challenge your friends to beat your score in Globetrotter!</p>
            </div>
            
            <div className="share-preview">
              <div className="share-preview-content">
                <div className="share-avatar">{username.charAt(0).toUpperCase()}</div>
                <p><strong>{username}</strong> has challenged you to a game of Globetrotter!</p>
              </div>
            </div>
            
            <div className="share-url-container">
              <input
                ref={shareUrlRef}
                type="text"
                value={shareUrl}
                readOnly
                className="share-url-input"
                onClick={(e) => e.target.select()}
              />
              <button 
                className={`copy-btn ${copied ? 'copied' : ''}`}
                onClick={handleCopyLink}
              >
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            
            <div className="share-buttons">
              <button className="share-btn primary" onClick={handleShare}>
                <span className="share-icon">📤</span> Share Challenge
              </button>
              
              <button className="share-btn secondary" onClick={onClose}>
                Maybe Later
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ShareModal;
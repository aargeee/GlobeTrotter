import { useState, useEffect } from 'react';
import apiService from '../services/api';
import '../styles/Modal.css';

function ProfileModal({ isOpen, onClose }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [originalUsername, setOriginalUsername] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [stats, setStats] = useState({
    score: 0,
    gamesPlayed: 0
  });

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
      setOriginalUsername(userData.username);
      setStats({
        score: userData.high_score,
        gamesPlayed: userData.games_played
      });
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    if (username.trim() === '') return;
    
    setIsSaving(true);
    try {
      await apiService.updateUserProfile({ username, password });
      setOriginalUsername(username);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating username:', error);
    } finally {
      setIsSaving(false);
      await fetchUserData();
    }
  };

  const handleCancel = () => {
    setUsername(originalUsername);
    setIsEditing(false);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>×</button>
        
        <h2 className="modal-title">Your Profile</h2>
        
        {isLoading ? (
          <div className="modal-loading">
            <div className="spinner"></div>
            <p>Loading profile...</p>
          </div>
        ) : (
          <>
            <div className="profile-section">
              <div className="profile-avatar">
                <div className="avatar-placeholder">
                  {username.charAt(0).toUpperCase()}
                </div>
              </div>
              
              <div className="profile-details">
                <div className="username-section">
                  {isEditing ? (
                    <div className="username-edit">
                      <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="username-input"
                        placeholder="Enter username"
                        autoFocus
                      />
                      <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="username-input"
                        placeholder="Enter password"
                        autoFocus
                      />
                      <div className="edit-actions">
                        <button 
                          className="save-btn" 
                          onClick={handleSave}
                          disabled={isSaving || username.trim() === ''}
                        >
                          {isSaving ? 'Saving...' : 'Log In'}
                        </button>
                        <button className="cancel-btn" onClick={handleCancel}>
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="username-display">
                      <h3>{username}</h3>
                        <button 
                          className="edit-btn"
                          onClick={() => setIsEditing(true)}
                        >
                          Edit
                        </button>
                    </div>
                  )}
                </div>
                
                <div className="stats-section">
                  <div className="stat-item">
                    <span className="stat-label">High Score</span>
                    <span className="stat-value">{stats.score}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Games Played</span>
                    <span className="stat-value">{stats.gamesPlayed}</span>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ProfileModal;
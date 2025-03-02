import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import './App.css'
import GamePage from './pages/GamePage'
import ProfileModal from './components/ProfileModal'
import ShareModal from './components/ShareModal'
import apiService from './services/api'

function App() {
  const navigate = useNavigate()
  const location = useLocation()
  const [animating, setAnimating] = useState(false)
  const [highScore, setHighScore] = useState(null)
  const [referrerName, setReferrerName] = useState(null)
  const [loading, setLoading] = useState(false)
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false)
  const [isShareModalOpen, setIsShareModalOpen] = useState(false)

  useEffect(() => {
    fetchHighScore()
    
    // Check if we should show the share modal (coming from inactive game)
    const params = new URLSearchParams(location.search)
    if (params.get('showShare') === 'true') {
      setIsShareModalOpen(true)
    }
  }, [location.search])

  useEffect(() => {
    // Reset animating state when location changes
    setAnimating(false);
  }, [location]);

  const fetchHighScore = async () => {
    setLoading(true)
    try {
      // Get the referrer parameter from the URL
      const params = new URLSearchParams(location.search)
      const referrer = params.get('referrer')
      
      const data = await apiService.getHighScore(referrer)
      if (referrer){
        setReferrerName(referrer)
      }
      setHighScore(data.high_score)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching high score:', error)
      setLoading(false)
    }
  }

  const handlePlayNow = async () => {
    try {
      const response = await apiService.startNewGame();
      const { game_id } = response;
      navigate(`/game/${game_id}`);
    } catch (error) {
      console.error('Failed to start a new game:', error);
    }
  };

  const handlePlayWithFriends = () => {
    setIsShareModalOpen(true)
  }

  const handleProfile = () => {
    setIsProfileModalOpen(true)
  }

  return (
    <>
      <Routes>
        <Route path="/" element={
          <div className={`app ${animating ? 'fade-out' : ''}`}>
            <div className="header">
              <div className="creator-info animate-slide-in-left">
                Created by <a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer">Your Name</a>
              </div>
              <button className="profile-btn animate-slide-in-right" onClick={handleProfile}>Profile</button>
            </div>
            
            <div className="main-content">
              <h1 className="title animate-pop-in">Globetrotter</h1>
              <p className="subtitle animate-fade-in">Solve cryptic clues about famous destinations around the world and unlock fascinating facts!</p>
              
              {loading ? (
                <div className="high-score-loading animate-pulse">
                  Loading challenge data...
                </div>
              ) : highScore && (
                <div className="high-score animate-fade-in-delay">
                  {referrerName 
                    ? <span><strong>{referrerName}</strong> scored <strong>{highScore}</strong> points. Can you beat them?</span>
                    : <span>Current high score: <strong>{highScore}</strong> points. Think you can top that?</span>
                  }
                </div>
              )}
              
              <div className="buttons">
                <button className="btn btn-primary animate-slide-up" onClick={handlePlayNow}>Play Now</button>
                <button className="btn btn-secondary animate-slide-up-delay" onClick={handlePlayWithFriends}>Challenge a friend</button>
              </div>
            </div>
            
            <div className="globe-animation">
              <div className="globe"></div>
            </div>
            
            {/* Floating elements */}
            <div className="floating-element"></div>
            <div className="floating-element"></div>
            <div className="floating-element"></div>
            <div className="floating-element"></div>
          </div>
        } />
        <Route path="/game/*" element={<GamePage />} />
      </Routes>
      
      {/* Modals */}
      <ProfileModal 
        isOpen={isProfileModalOpen} 
        onClose={() => setIsProfileModalOpen(false)} 
      />
      
      <ShareModal 
        isOpen={isShareModalOpen} 
        onClose={() => setIsShareModalOpen(false)} 
      />
    </>
  )
}

export default App

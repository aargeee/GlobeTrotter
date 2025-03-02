import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/GamePage.css';
import apiService from '../services/api';

function GamePage() {
  const navigate = useNavigate();
  const game_id = useLocation().pathname.substring(6); // Get game_id from URL
  const [clues, setClues] = useState([]);
  const [cities, setCities] = useState([]);
  const [filteredCities, setFilteredCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [gameState, setGameState] = useState('playing'); // playing, correct, incorrect, inactive
  const [facts, setFacts] = useState([]);
  const [trivia, setTrivia] = useState([]);
  const [loading, setLoading] = useState(true);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [animationClass, setAnimationClass] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [score, setScore] = useState(0);

  // Fetch clues and cities from backend
  useEffect(() => {
    fetchGameData();
    fetchGameScore();
  }, [game_id]);

  useEffect(() => {
    if (!isActive || clues.length === 0) {
      setGameState('inactive');
    } else {
      setGameState('playing');
    }
  }, [isActive, clues]);

  const fetchGameData = async () => {
    try {
      setLoading(true);
      
      const data = await apiService.getGameData(game_id); // Pass game_id to the service
      const cities = await apiService.getCitiesList();
      
      setClues(data.clues);
      setCities(cities.cities);
      setIsActive(data.is_active);
      
      if (!data.is_active) {
        setGameState('inactive');
      }
    } catch (error) {
      console.error('Failed to fetch game data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchGameScore = async () => {
    try {
      const data = await apiService.getGameScore(game_id); // Pass game_id to the service
      setScore(data.correct_answers);
    } catch (error) {
      console.error('Failed to fetch game score:', error);
    }
  };

  const handleNext = async () => {
    // Fetch new game data for the next question
    await fetchGameData();
    await fetchGameScore();
    setSelectedCity('');
    setSearchTerm('');
  };

  // Filter cities based on search term
  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredCities(cities)
    } else {
      const filtered = cities.filter(city => 
        city.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredCities(filtered)
    }
  }, [searchTerm, cities])

  const handleCitySelect = (city) => {
    setSelectedCity(city)
  }

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value)
  }

  const handleSubmit = async () => {
    if (!selectedCity) return
    
    try {
      const result = await apiService.checkAnswer(game_id, selectedCity)
      
      setFacts(result.fun_facts)
      setTrivia(result.trivia)
      setCorrectAnswer(result.correct_city)
      
      const newScore = await apiService.getGameScore(game_id)
      setScore(newScore.correct_answers)

      if (result.is_answered_correctly) {
        setAnimationClass('fade-out')
        setTimeout(() => {
          setGameState('correct')
          setAnimationClass('fade-in')
        }, 500)
      } else {
        setAnimationClass('shake')
        setTimeout(() => {
          setGameState('incorrect')  // Change 'gaveUp' to 'incorrect'
          setAnimationClass('fade-in')
        }, 600)
      }
    } catch (error) {
      console.error('Error checking answer:', error)
    }
  }

  const handleBackToHome = () => {
    setAnimationClass('fade-out')
    setTimeout(() => {
      navigate('/')
    }, 500)
  }

  const handleChallengeClick = () => {
    setAnimationClass('fade-out')
    setTimeout(() => {
      navigate('/?showShare=true')
    }, 500)
  }

  if (loading) {
    return (
      <div className="game-page">
        <div className="loading">
          <h2>Loading challenge...</h2>
          <div className="spinner"></div>
        </div>
      </div>
    )
  }

  console.log(gameState)

  return (
    <div className="game-page">
      {/* Floating background elements */}
      <div className="floating-element"></div>
      <div className="floating-element"></div>
      <div className="floating-element"></div>
      
      <div className="game-header">
        <button className="back-btn" onClick={handleBackToHome}>← Back to Home</button>
        <h1>Globetrotter Challenge</h1>
        <div className="score-display">
          <span className="score-label">Score:</span>
          <span className="score-value">{score}</span>
        </div>
      </div>
      <div className={`game-content ${animationClass}`}>
        {gameState === 'playing' && isActive && (
          <>
            <div className="clues-section">
              <h2>Clues</h2>
              <ul className="clues-list">
                {clues.map((clue, index) => (
                  <li key={index} className="clue-item">{clue}</li>
                ))}
              </ul>
            </div>

            <div className="guess-section">
              <h2>Make Your Guess</h2>
              <p>Search and select a city from the list below:</p>
              
              <div className="search-container">
                <input
                  type="text"
                  className="search-input"
                  placeholder="Search for a city..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                />
              </div>
              
              <div className="cities-list-container">
                <ul className="cities-list">
                  {filteredCities.map((city) => (
                    <li 
                      key={city} 
                      className={`city-item ${selectedCity === city ? 'selected' : ''}`}
                      onClick={() => handleCitySelect(city)}
                    >
                      {city}
                    </li>
                  ))}
                </ul>
              </div>

              <button 
                className="submit-btn" 
                disabled={!selectedCity}
                onClick={handleSubmit}
              >
                Submit Answer
              </button>
            </div>
          </>
        )}

        {((gameState === 'inactive') || (gameState === 'active' && clues.length === 0)) && (
          <div className="result-section inactive">
            <div className="inactive-icon">🌎</div>
            <h2>You've Explored It All!</h2>
            <p>You've exhausted our current collection of destination challenges.</p>
            <p className="inactive-message">Our travel experts are busy creating new challenges for you. Please check back soon for more geographical adventures!</p>
            
            <div className="inactive-actions">
              <button className="home-btn" onClick={handleBackToHome}>
                Return Home
              </button>
              <button className="challenge-btn" onClick={handleChallengeClick}>
                Challenge Friends
              </button>
            </div>
          </div>
        )}

        {gameState === 'correct' && (
          <div className="result-section correct">
            <h2>Correct! 🎉</h2>
            <p>You've successfully identified {correctAnswer}!</p>
            
            <div className="facts-section">
              <h3>Fun Facts about {correctAnswer}</h3>
              <div className="facts-grid">
                {facts.map((fact, index) => (
                  <div key={index} className="fact-card">
                    <span className="fact-number">{index + 1}</span>
                    <p>{fact}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="facts-section">
              <h3>Trivia about {correctAnswer}</h3>
              <div className="facts-grid">
                {trivia.map((trivia, index) => (
                  <div key={index} className="fact-card">
                    <span className="fact-number">{index + 1}</span>
                    <p>{trivia}</p>
                  </div>
                ))}
              </div>
            </div>
            
            <button className="play-again-btn" onClick={handleNext}>
              Next Question
            </button>
          </div>
        )}

        {gameState === 'incorrect' && (
          <div className="result-section gave-up">
            <h2>The answer was {correctAnswer}</h2>
            
            <div className="facts-section">
              <h3>Fun Facts about {correctAnswer}</h3>
              <div className="facts-grid">
                {facts.map((fact, index) => (
                  <div key={index} className="fact-card">
                    <span className="fact-number">{index + 1}</span>
                    <p>{fact}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="facts-section">
              <h3>Trivia about {correctAnswer}</h3>
              <div className="facts-grid">
                {trivia.map((trivia, index) => (
                  <div key={index} className="fact-card">
                    <span className="fact-number">{index + 1}</span>
                    <p>{trivia}</p>
                  </div>
                ))}
              </div>
            </div>
            
            <button className="play-again-btn" onClick={handleNext}>
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default GamePage
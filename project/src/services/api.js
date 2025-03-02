import axios from 'axios';

// Mock user data
const mockUserData = {
  username: "traveler2025",
  score: 3500,
  gamesPlayed: 12
};

// API service object
const apiService = {
  // Fetch token
  fetchToken: async () => {
    const response = await axios.post('http://localhost:8000/api/token/');
    const { access, refresh } = response.data;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    return { access, refresh };
  },

  // Refresh token
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    const response = await axios.post('http://localhost:8000/api/token/refresh/', { refresh: refreshToken });
    const { access } = response.data;
    localStorage.setItem('access_token', access);
    return access;
  },

  // Start a new game
  startNewGame: async () => {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.post('http://localhost:8000/api/game/', {}, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  },

  // Get game clues and data
  getGameData: async (game_id) => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      throw new Error('No access token available');
    }
    const response = await axios.get(`http://localhost:8000/api/game/${game_id}/questions/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  },

  getCitiesList: async () => {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.get('http://localhost:8000/api/cities/', {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  },
  
  // Get high score data
  getHighScore: async (referrer) => {
    const accessToken = localStorage.getItem('access_token');
    const url = referrer ? `http://localhost:8000/api/game/high_score/${referrer}` : 'http://localhost:8000/api/game/high_score';
    const response = await axios.get(url, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  },
  
  // Get user profile data
  getUserProfile: async () => {
    // Simulate API delay
    
    // Real implementation would be:
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.get(`http://localhost:8000/api/profile/`, {
      headers: {
      Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  },
  
  // Update user profile
  updateUserProfile: async (userData) => {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.post('http://localhost:8000/api/signup/', userData, {
      headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
      }
    });
    const { access_token, refresh_token } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return response.data;
  },
  
  // Check answer
  checkAnswer: async (game_id, answer) => {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.post(`http://localhost:8000/api/game/${game_id}/response/`, { 'city': answer }, {
      headers: {
      Authorization: `Bearer ${accessToken}`
      }
    });
    return response.data;
  }
};

export default apiService;

// Initialize token on page load
const initializeToken = async () => {
  let accessToken = localStorage.getItem('access_token');
  if (!accessToken) {
    await apiService.fetchToken();
  } else {
    try {
      await apiService.refreshToken();
    } catch (error) {
      console.error('Failed to refresh token:', error);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      await apiService.fetchToken();
    }
  }

  // Set up token refresh interval
  const refreshInterval = setInterval(async () => {
    try {
      await apiService.refreshToken();
    } catch (error) {
      console.error('Failed to refresh token:', error);
    }
  }, 15 * 60 * 1000); // 15 minutes

  // Clear interval when window is destroyed
  window.addEventListener('beforeunload', () => {
    clearInterval(refreshInterval);
  });
};

// Call initializeToken on page load
initializeToken();
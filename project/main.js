import './style.css'

document.querySelector('#app').innerHTML = `
  <div class="header">
    <div class="creator-info">
      Created by <a href="https://github.com/yourusername" target="_blank">Your Name</a>
    </div>
    <button class="profile-btn">Profile</button>
  </div>
  
  <div class="main-content">
    <h1 class="title">Globetrotter</h1>
    <p class="subtitle">Solve cryptic clues about famous destinations around the world and unlock fascinating facts!</p>
    
    <div class="buttons">
      <button class="btn btn-primary">Play Now</button>
      <button class="btn btn-secondary">Play with Friends</button>
    </div>
  </div>
`

// Add event listeners
document.querySelector('.btn-primary').addEventListener('click', () => {
  console.log('Play Now clicked')
  // Add navigation to game page here
})

document.querySelector('.btn-secondary').addEventListener('click', () => {
  console.log('Play with Friends clicked')
  // Add multiplayer functionality here
})

document.querySelector('.profile-btn').addEventListener('click', () => {
  console.log('Profile clicked')
  // Add profile page navigation here
})
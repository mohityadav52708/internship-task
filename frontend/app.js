// frontend/app.js

const API_URL = 'http://localhost:5000';
let token = '';

// Function to register a new user
async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    alert(data.message || 'Registration successful');
}

// Function to login
async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (data.token) {
        token = data.token;
        alert('Login successful');
    } else {
        alert(data.message || 'Login failed');
    }
}

// Function to fetch all webtoons
async function fetchWebtoons() {
    const response = await fetch(`${API_URL}/webtoons`);
    const webtoons = await response.json();

    const list = document.getElementById('webtoons-list');
    list.innerHTML = '';

    webtoons.forEach(webtoon => {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="webtoon-item">
                <div class="webtoon-details">
                    <strong>${webtoon.title}</strong>
                    <p>${webtoon.description}</p>
                    <p><em>Characters:</em> ${webtoon.characters.map(char => char.name).join(', ')}</p>
                </div>
                <button class="delete-button" onclick="deleteWebtoon('${webtoon._id}')">Delete</button>
            </div>
        `;
        list.appendChild(li);
    });
}

// Function to add a new webtoon
async function addWebtoon() {
    const title = document.getElementById('webtoon-title').value;
    const description = document.getElementById('webtoon-description').value;
    const charactersInput = document.getElementById('webtoon-characters').value;

    // Convert comma-separated string to array of character objects
    const charactersArray = charactersInput.split(',').map(char => ({
        name: char.trim(),
        role: 'Supporting', // Default role, can be modified as needed
        traits: ['Trait1', 'Trait2'] // Default traits, can be modified as needed
    }));

    const response = await fetch(`${API_URL}/webtoons`, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title, description, characters: charactersArray })
    });

    const data = await response.json();
    if (response.status === 201) {
        alert('Webtoon added successfully');
        fetchWebtoons();
    } else {
        alert(data.message || 'Failed to add webtoon');
    }
}

// Function to delete a webtoon
async function deleteWebtoon(id) {
    if (!confirm('Are you sure you want to delete this webtoon?')) return;

    const response = await fetch(`${API_URL}/webtoons/${id}`, {
        method: 'DELETE',
        headers: { 
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message || 'Webtoon deleted successfully');
        fetchWebtoons();
    } else {
        alert(data.message || 'Failed to delete webtoon');
    }
}

// Initial fetch of webtoons when the page loads
window.onload = fetchWebtoons;

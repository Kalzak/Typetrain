const API_BASE_URL = "http://localhost:5000";


function toggleAuthElements(isLoggedIn) {
    document.getElementById('auth-form').style.display = isLoggedIn ? 'none' : 'block';
    document.getElementById('logout-button').style.display = isLoggedIn ? 'block' : 'none';
}

// Fetch current user
async function fetchUser() {
    if(localStorage.getItem('token') === null) {
        document.getElementById('greeting').textContent = 'Hello Guest';
        toggleAuthElements(false);
        return;
    }    
    try {
        const response = await fetch(`${API_BASE_URL}/user`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if(response.status === 401 && localStorage.getItem('token') !== null) {
            alert('session expired, please login again');
            localStorage.removeItem('token');
            document.getElementById('greeting').textContent = 'Hello Guest';
            toggleAuthElements(false);  
            return;
        }

        const data = await response.json();

        console.log(localStorage.getItem('token'))
        document.getElementById('greeting').textContent = `Hello ${data.user}`;
        console.log("data.user", data)
        toggleAuthElements(data.user !== 'Guest'); // Update visibility based on login status
    } catch (error) {
        console.error('Error fetching user:', error);
        console.log(error, "hello!!")
        document.getElementById('greeting').textContent = 'Hello Guest';
    }
}

// Handle login/signup
document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) throw new Error('Failed to log in');
        const data = await response.json();
        localStorage.setItem('token', data.access_token); // Save JWT
        fetchUser(); // Refresh user display
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Check your credentials or try signing up.');
    }
});


document.getElementById('logout-button').addEventListener('click', () => {
    localStorage.removeItem('token'); // Clear JWT token
    document.getElementById('greeting').textContent = 'Hello Guest';
    // Clear text fields in username and password textboxes
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    fetchUser(); // Refresh the user display
});

// Initialize greeting
fetchUser();

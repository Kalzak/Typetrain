const API_BASE_URL = "http://localhost:5000";

document.getElementById('text-submit-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('text').value;

    try {
        const response = await fetch(`${API_BASE_URL}/submittext`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify({ text }),
        });

        if (response.ok) {
            fetchUserTexts();
        } else {
            const data = await response.json();
            alert(data.message || 'Submision failed');
        }
    } catch (error) {
        console.error('Submission error:', error);
        alert('An error occurred. Please try again.');
    }
});

function checkLoginState() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('You must be logged in to submit a text');
        window.location.href = 'index.html';
    }
}

async function fetchUserTexts() {
    const token = localStorage.getItem('token');   
    if (!token) {
        document.getElementById('user-texts').textContent = 'You must be logged in to see your texts';
        window.location.href = 'index.html';
    }

    try {
        const response = await fetch(`${API_BASE_URL}/mytexts`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        
        if (!response.ok) throw new Error("failed to fetch texts");

        const data = await response.json();
        const texts = data.texts
        console.log(texts)
        const list = document.getElementById('user-texts');
        list.innerHTML = '';

        if (texts.length === 0) {
            list.innerHTML = '<li>You have not submitted any texts yet.</li>';
        } else {
            texts.forEach(text => {
                const li = document.createElement('li');
                li.textContent = `${text.text}  `;
                li.innerHTML += `<button onclick="deleteText(${text.id})">Delete</button>`;
                list.appendChild(li);
            });
        }
    } catch (error) {
        console.error('Error fetching user texts:', error);
        document.getElementById('user-texts').textContent = '<li>An error occurred. Please try again.</li>';
    }
}

async function deleteText(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/deletetext/${id}`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (response.ok) {
            fetchUserTexts();
        } else {
            const data = await response.json();
            alert(data.message || 'Failed to delete text');
        }
    } catch (error) {
        console.error('Error deleting text:', error);
        alert('An error occurred. Please try again.');
    }
}

checkLoginState();
fetchUserTexts();
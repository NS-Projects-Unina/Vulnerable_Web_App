document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.querySelector("form[action='/login']");
    if (loginForm) {
        loginForm.addEventListener("submit", (event) => {
            event.preventDefault(); // Previene l'invio del modulo

            const formData = new FormData(loginForm);
            fetch('/login', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Login successful!');
                    window.location.reload(); // Ricarica la pagina dopo il login
                } else {
                    alert(data.error);
                }
            });
        });
    }

    // Funzione per avviare una sfida
    window.startChallenge = function(challengeId) {
        fetch(`/challenge/${challengeId}/start`, {
            method: 'POST',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Challenge started!');
            } else {
                alert(data.error);
            }
        });
    };

    // Funzione per fermare una sfida
    window.stopChallenge = function(challengeId) {
        fetch(`/challenge/${challengeId}/stop`, {
            method: 'POST',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Challenge stopped!');
            } else {
                alert(data.error);
            }
        });
    };

    // Funzione per completare una sfida
    window.completeChallenge = function(challengeId) {
        fetch(`/challenge/${challengeId}/complete`, {
            method: 'POST',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Challenge completed!');
            } else {
                alert(data.error);
            }
        });
    };
});

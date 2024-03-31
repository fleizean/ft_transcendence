export function initializeProfileSettings() {

    document.getElementById('profile_submit').addEventListener('click', function() {
        var formData = new FormData(); // FormData nesnesi oluştur
        var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    
        // Form verilerini al
        formData.append('username', document.getElementById('id_username_profile').value);
        formData.append('email', document.getElementById('id_email_profile').value);
        formData.append('displayname', document.getElementById('id_displayname_profile').value);
        formData.append('profile_form', 'profile_form');
    
        // CSRF token'ı eklemek
    
        fetch('{% url "profile_settings" username=user_info.username %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.text())
        .then(data => {
            document.body.innerHTML = data;
            if(data.message)
                showToast(data.message, 'text-bg-success', 'bi bi-check-circle-fill');
            else
                showToast(data.error, 'text-bg-danger', 'bi bi-x-circle-fill');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    document.getElementById('password_submit').addEventListener('click', function() {
        var formData = new FormData(); // FormData nesnesi oluştur
        var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
        formData.append('old_password', document.getElementById('id_old_password').value);
        formData.append('new_password1', document.getElementById('id_new_password1').value);
        formData.append('new_password2', document.getElementById('id_new_password2').value);
        formData.append('password_form', 'password_form');
        fetch('{% url "profile_settings" username=user_info.username %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.text())
        .then(data => {
            document.body.innerHTML = data;
            if (data.message) {
                    showToast(data.message, 'text-bg-success', 'bi bi-check-circle-fill');
                } else if (data.error) {
                    // Hata mesajlarını göster
                    for (let platform in data.error) {
                        showToast(data.error[platform][0], 'text-bg-danger', 'bi bi-x-circle-fill');
                    }
                } else {
                    if (selectedLanguage === 'tr') {
                        showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
                    } else if (selectedLanguage === 'hi') {
                        showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
                    } else if (selectedLanguage === 'pt')
                        showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
                    else {
                        showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
                    }
                }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    document.getElementById('social_submit').addEventListener('click', function() {
        var formData = new FormData(); // FormData nesnesi oluştur
        var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
        formData.append('linkedin', document.getElementById('id_linkedin').value);
        formData.append('twitter', document.getElementById('id_twitter').value);
        formData.append('intra42', document.getElementById('id_intra42').value);
        formData.append('github', document.getElementById('id_github').value);
        formData.append('social_form', 'social_form');
    
        fetch('{% url "profile_settings" username=user_info.username %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.text())
        .then(data => {    
            document.body.innerHTML = data;
            if (data.message) {
                showToast(data.message, 'text-bg-success', 'bi bi-check-circle-fill');
            } else if (data.error) {
                // Hata mesajlarını göster
                for (let platform in data.error) {
                    showToast(data.error[platform][0], 'text-bg-danger', 'bi bi-x-circle-fill');
                }
            } else {
                showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
            }
    }   )
    
        .catch(error => {
            console.error('Error:', error);
        });
    
    });
    
    document.getElementById('delete_account_submit').addEventListener('click', function() {
        var formData = new FormData(); // FormData nesnesi oluştur
        formData.append('email', document.getElementById('id_email').value);
        formData.append('delete_account_form', 'delete_account_form');
        var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    
        fetch('{% url "profile_settings" username=user_info.username %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.text())
        .then(data => {
            document.body.innerHTML = data;
            if (data.message) {
                showToast(data.message, 'text-bg-success', 'bi bi-check-circle-fill');
            } else if (data.error) {
                // Hata mesajlarını göster
                for (let platform in data.error) {
                    showToast(data.error[platform][0], 'text-bg-danger', 'bi bi-x-circle-fill');
                }
            } else {
                if (selectedLanguage === 'tr') {
                    showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
                } else if (selectedLanguage === 'hi') {
                    showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
                } else if (selectedLanguage === 'pt')
                    showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
                else {
                    showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    document.querySelectorAll('button.btn-block').forEach(item => {
        item.addEventListener('click', event => {
            var blocked_username = event.target.dataset.username;
            // Handle blocking logic here
            console.log('Blocked user:', blocked_username);
        });
    });
    
    const fileInput = document.getElementById('id_avatar');
    fileInput.addEventListener('change', function(event) {
        var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
        var file = this.files[0];
        if (file.size > 2 * 1024 * 1024) { // 1MB
            showToast("Photo must be under 2MB!", "text-bg-danger", "bi bi-image");
        }
        else {
            var formData = new FormData(); // FormData nesnesini oluştur
    
            formData.append('avatar', file);
    
            // avatar_form verisini ekle
            formData.append('avatar_form', 'avatar_form');
    
            // CSRF token'ı eklemek
            fetch('{% url "profile_settings" username=user_info.username %}', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrftoken
                },
            })
            .then(response => response.text())
            .then(data => {
                document.body.innerHTML = data;
                if (data.message) {
                    showToast(data.message, 'text-bg-success', 'bi bi-check-circle-fill');
                } else if (data.error) {
                    // Hata mesajlarını göster
                    for (let platform in data.error) {
                        showToast(data.error[platform][0], 'text-bg-danger', 'bi bi-x-circle-fill');
                    }
                } else {
                    if (selectedLanguage === 'tr') {
                        showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
                    } else if (selectedLanguage === 'hi') {
                        showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
                    } else if (selectedLanguage === 'pt')
                        showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
                    else {
                        showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    function showToast(content, status, iconClass) {
        const liveToast = document.getElementById('liveToast');
        var toastContent = document.querySelector('#liveToast .fw-semibold');
        var toastIcon = document.querySelector('.toast-body .i-class i');
    
        toastIcon.className = iconClass;
        liveToast.classList.remove('text-bg-danger'); 
        liveToast.className = 'toast'; 
        liveToast.classList.add(status);
    
        toastContent.textContent = content;
        const toast = new bootstrap.Toast(liveToast);
        toast.show();
        setTimeout(function() {
            toast.hide();
        }, 8000);
    }
}
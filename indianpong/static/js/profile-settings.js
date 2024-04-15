function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

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

export function editProfile(username) {
    if (!username)
        return;

    var formData = new FormData(); // FormData nesnesi oluştur
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    const lang = getCookie('selectedLanguage');

    // Form verilerini al
    formData.append('username', document.getElementById('id_username_profile').value);
    formData.append('email', document.getElementById('id_email_profile').value);
    formData.append('displayname', document.getElementById('id_displayname_profile').value);
    formData.append('profile_form', 'profile_form');
    // CSRF token'ı eklemek
    
    fetch(`/profile/${username}/settings`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        },
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
        const message = document.querySelector('.container-top').dataset.message;
        if (message)
            showToast(message, 'text-bg-success', 'bi bi-check-circle-fill');
        else {
            
            if (lang === 'tr') {
                showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'hi') {
                showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'pt')
                showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
            else {
                showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
            }
        }
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

export function editPassword(username) {
    if (!username)
        return;

    var formData = new FormData(); // FormData nesnesi oluştur
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    formData.append('old_password', document.getElementById('id_old_password').value);
    formData.append('new_password1', document.getElementById('id_new_password1').value);
    formData.append('new_password2', document.getElementById('id_new_password2').value);
    formData.append('password_form', 'password_form');
    const lang = getCookie('selectedLanguage');
    fetch(`/profile/${username}/settings`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
        const message = document.querySelector('.container-top').dataset.message;
        var currentFragment = window.location.hash.substring(1);
        displaySection(currentFragment);
        if (message) {
            showToast(message, 'text-bg-success', 'bi bi-check-circle-fill');
        } else {
            if (lang === 'tr') {
                showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'hi') {
                showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'pt')
                showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
            else {
                showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

export function editSocial(username) {
    if (!username)
        return;

    var formData = new FormData(); // FormData nesnesi oluştur
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    formData.append('linkedin', document.getElementById('id_linkedin').value);
    formData.append('twitter', document.getElementById('id_twitter').value);
    formData.append('intra42', document.getElementById('id_intra42').value);
    formData.append('github', document.getElementById('id_github').value);
    formData.append('social_form', 'social_form');
    const lang = getCookie('selectedLanguage');
    fetch(`/profile/${username}/settings`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
        const message = document.querySelector('.container-top').dataset.message;
        var currentFragment = window.location.hash.substring(1);
        displaySection(currentFragment);
        if (message) {
            showToast(message, 'text-bg-success', 'bi bi-check-circle-fill');
        } else {
            if (lang === 'tr') {
                showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'hi') {
                showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'pt')
                showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
            else {
                showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

};

export function deleteAccount(username) {
    if (!username)
        return;

    var formData = new FormData(); // FormData nesnesi oluştur
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    formData.append('email', document.getElementById('id_email').value);
    formData.append('delete_account_form', 'delete_account_form');
    const lang = getCookie('selectedLanguage');
    fetch(`/profile/${username}/settings`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
};

export function changeAvatar(username) {

    if (!username)
        return;

    const fileInput = document.getElementById('id_avatar');
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    var file = fileInput.files[0];  
    const lang = getCookie('selectedLanguage');
    if (file.size > 2 * 1024 * 1024) { // 1MB
        showToast("Photo must be under 2MB!", "text-bg-danger", "bi bi-image");
    }
    else {
        var formData = new FormData(); // FormData nesnesini oluştur
        formData.append('avatar', file);
        // avatar_form verisini ekle
        formData.append('avatar_form', 'avatar_form');
        // CSRF token'ı eklemek
        fetch(`/profile/${username}/settings`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.text())
        .then(data => {
            document.body.innerHTML = data;
            const message = document.querySelector('.container-top').dataset.message;
            const error = document.querySelector('.container-top').dataset.error;
            if (message) {
                showToast(message, 'text-bg-success', 'bi bi-check-circle-fill');
            } else {
                if (lang === 'tr') {
                    showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
                } else if (lang === 'hi') {
                    showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
                } else if (lang === 'pt') {
                    showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
                } else {
                    showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        }
}

export function unblockButon(username, blockedusername) {
    if (!blockedusername || !username)
        return;

    var formData = new FormData(); // FormData nesnesi oluştur
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
    formData.append('blockedusername', blockedusername);
    formData.append('unblock_form', 'unblock_form');
    const lang = getCookie('selectedLanguage');
    fetch(`/profile/${username}/settings`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data;
        var currentFragment = window.location.hash.substring(1);
        displaySection(currentFragment);
        const message = document.querySelector('.container-top').dataset.message;
        if (message) {
            showToast(message, 'text-bg-success', 'bi bi-check-circle-fill');
        } else {
            if (lang === 'tr') {
                showToast('Bir hata oluştu.', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'hi') {
                showToast('कोई त्रुटि हुई।', 'text-bg-danger', 'bi bi-x-circle-fill');
            } else if (lang === 'pt')
                showToast('Ocorreu um erro.', 'text-bg-danger', 'bi bi-x-circle-fill');
            else {
                showToast('An error occurred.', 'text-bg-danger', 'bi bi-x-circle-fill');
            }
        }
    })
}

export function displaySection(sectionId) {
    var sections = ["editProfile", "addSocial", "closeAccount", "blockedUsers", "changePassword"];
    if (!sectionId)
        return;
    for (var i = 0; i < sections.length; i++) {
        var section = document.getElementById(sections[i]);
        if (sections[i] === sectionId) {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    }
}
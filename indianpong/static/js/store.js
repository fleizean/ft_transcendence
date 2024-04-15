function initializeStore() {

    const storeInfos = document.getElementsByClassName('store-info'); // .store-info'ya erişim
    const smallWalletNames = document.getElementsByClassName('small-wallet-name');

    for (let i = 0; i < smallWalletNames.length; i++) {
        smallWalletNames[i].addEventListener('mouseover', () => {
            storeInfos[i].style.visibility = 'visible';
        });

        smallWalletNames[i].addEventListener('mouseout', () => {
            storeInfos[i].style.visibility = 'hidden';
        });
    }
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

  }
  
  function submitStoreItemForm(username, itemName, formId, price) {
      const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
      const lang = cookie ? cookie.split('=')[1] : 'en';
      const form = document.getElementById('store_item_form' + formId);
      const formData = new FormData(form);
      var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
      fetch(`/store/${username}/`, {
        method: form.method,
        body: formData,
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then(response => response.text())
      .then(data => {
        // hide the item after it is bought
        const productCard = document.getElementById('product-card-' + formId);
        productCard.style.display = 'none';
        //update the wallet amount with price
        const walletAmount = document.querySelector('.wallet-amount');
        walletAmount.textContent = (parseInt(walletAmount.textContent) - price) + 'N₩';
        document.body.innerHTML = data;
        if (lang === 'tr')
          showToast(`${itemName} öğesini başarıyla satın aldın!`, `text-bg-success`, `bi bi-shop`);
        else if (lang === 'hi')
          showToast(`आपने ${itemName} आइटम सफलतापूर्वक खरीद लिया है!`, `text-bg-success`, `bi bi-shop`);
        else if (lang === 'pt')
          showToast(`Você comprou com sucesso o item ${itemName}!`, `text-bg-success`, `bi bi-shop`);
        else
          showToast(`You have successfully bought ${itemName} item!`, `text-bg-success`, `bi bi-shop`);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
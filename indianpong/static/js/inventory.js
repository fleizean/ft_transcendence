function initializeInventory(){
    const inventoryInfos = document.getElementsByClassName('inventory-info'); // .inventory-info'ya erişim
      const smallWalletNames = document.getElementsByClassName('small-wallet-name');
  
      for (let i = 0; i < smallWalletNames.length; i++) {
          smallWalletNames[i].addEventListener('mouseover', () => {
              inventoryInfos[i].style.visibility = 'visible';
          });
  
          smallWalletNames[i].addEventListener('mouseout', () => {
              inventoryInfos[i].style.visibility = 'hidden';
          });
      };
}


function showToast(content, status, iconClass) {
    const liveToast = document.getElementById('liveToast');
  
    var toastContent = liveToast.querySelector('.fw-semibold');
    var toastIcon = liveToast.querySelector('.i-class i');
  
    toastIcon.className = iconClass;
    liveToast.classList.remove('text-bg-danger'); 
    liveToast.className = 'toast'; 
    liveToast.classList.add(status);
  
    toastContent.textContent = content;
  
    const toast = new bootstrap.Toast(liveToast);
    toast.show();
  }
  
  function openSetPropertyModal(itemName, itemWhatIs) {
      document.getElementById('itemNameInput').value = itemName;
      var propertyContent = document.getElementById('propertyContent');
          if (itemName === "My Playground" || itemName === "My Beautiful Paddle") {
          itemWhatIs = itemWhatIs || '#000000';
          propertyContent.innerHTML = `
              <label for="color">Choose Color:</label>
              <input type="color" id="color" name="whatis" value="${itemWhatIs}">
          `;
      } else {
          itemWhatIs = itemWhatIs || 'IndianAI';
          propertyContent.innerHTML = `
              <label for="propertyName">AI Name:</label>
              <input type="text" id="propertyName" name="whatis" value="${itemWhatIs}">
          `;
      }
  
      var modal = new bootstrap.Modal(document.getElementById('setPropertyModal'), { backdrop: false, keyboard: false });
      modal.show();
  
  }
  
  function saveProperty(username ,itemId) {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
      const lang = cookie ? cookie.split('=')[1] : 'en';
      var itemName = document.getElementById('itemNameInput').value;
      if (itemName === "My Playground" || itemName === "My Beautiful Paddle") {
          whatis = document.getElementById('color').value;
      } else {
          whatis = document.getElementById('propertyName').value;
      }
      var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
  
      const form = document.getElementById('store_item_form' + itemId);
      const formData = new FormData(form);
  
  
      fetch(`/inventory/${username}/`, {
        method: form.method,
        body: formData,
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then(response => response.text())
      .then(text => {
        let button = document.getElementById(`button-${itemName}`);
        button.setAttribute('data-whatis', whatis);
        if (lang === 'tr')
          showToast(`${itemName} öğesini başarıyla özelleştirdin!`, `text-bg-success`, `bi bi-shop`);
        else if (lang === 'hi')
          showToast(`आपने ${itemName} आइटम को सफलतापूर्वक अनुकूलित किया है!`, `text-bg-success`, `bi bi-shop`);
        else if (lang === 'pt')
          showToast(`Você personalizou com sucesso o item ${itemName}!`, `text-bg-success`, `bi bi-shop`);
        else
          showToast(`You have successfully customized ${itemName} item!`, `text-bg-success`, `bi bi-shop`);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  
  function submitInventoryItemForm(username, itemName) {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('selectedLanguage='));
    const lang = cookie ? cookie.split('=')[1] : 'en';
    const form = document.getElementById('store_item_form' + itemName);
    const formData = new FormData(form);
    // Access the data-is-equipped attribute
    let isEquipped = form.getAttribute('data-is-equipped');
    var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
  
    
    let toastMessage;
    let toastIcon;
    if (isEquipped == 'True') {
      if (lang === 'tr')
        toastMessage = `${itemName} öğesini başarıyla çıkardın!`; // You successfully unequipped the item!
      else if (lang === 'hi')
        toastMessage = `आपने ${itemName} आइटम को सफलतापूर्वक अनइक्विप किया है!`;
      else if (lang === 'pt')
        toastMessage = `Você desequipou com sucesso o item ${itemName}!`;
      else
        toastMessage = `You have successfully unequipped ${itemName} item!`;
      toastIcon = `bi bi-x-circle-fill`; // Change this to the icon you want to show when unequipping
    } else {
      if (lang === 'tr')
        toastMessage = `${itemName} öğesini başarıyla kuşandın!`; // You successfully equipped the item!
      else if (lang === 'hi')
        toastMessage = `आपने ${itemName} आइटम को सफलतापूर्वक इक्विप किया है!`;
      else if (lang === 'pt')
        toastMessage = `Você equipou com sucesso o item ${itemName}!`;
      else
        toastMessage = `You have successfully equipped ${itemName} item!`;
      toastIcon = `bi bi-check-circle-fill`;
    }
    
  
    fetch(`/inventory/${username}/`, {
      method: form.method,
      body: formData,
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
    .then(response => response.text())
    .then(data => {
       // Change the value of data-is-equipped attribute
      form.setAttribute('data-is-equipped', isEquipped == 'True' ? 'False' : 'True');
      document.body.innerHTML = data;
      showToast(toastMessage, `text-bg-success`, toastIcon);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
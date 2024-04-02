export function initializeInventory(){
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

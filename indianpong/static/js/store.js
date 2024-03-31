
export function initializeStore() {

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

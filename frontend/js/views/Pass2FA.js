import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Home");
    }

    async getHtml() {
        return `
        <div class="cursor">
            <div class="container">
                <div class="Pass2FaArea" id="Pass2FaArea">
                    <form class="form-pass2fa">
                        <a href="/"><span class="close">X</span></a>
                        <div class="info-pass2fa">
                            <span class="title-pass2fa">Two-Factor Verification</span>
                            <p class="description-pass2fa">Enter the two-factor authentication code provided by the authenticator app </p>
                        </div>
                        <div class="input-fields">
                            <input placeholder="" class="numbers-only" id="numbers-only1" type="text" maxlength="1">
                            <input placeholder="" class="numbers-only" id="numbers-only2" type="text" maxlength="1">
                            <input placeholder="" class="numbers-only" id="numbers-only3" type="text" maxlength="1">
                            <div class="seperator">
                                /
                            </div>
                            <input placeholder="" class="numbers-only" id="numbers-only4" type="text" maxlength="1">
                            <input placeholder="" class="numbers-only" id="numbers-only5" type="text" maxlength="1">
                            <input placeholder="" class="numbers-only" id="numbers-only6" type="text" maxlength="1">
                        </div>

                        <div class="action-btns">
                          <a class="verify" href="#">Verify</a>
                          <a class="clear" onclick="clear2FA()">Clear</a>
                        </div>
                    </form>
                </div>
            </div>
            
            `;
    }
    
}


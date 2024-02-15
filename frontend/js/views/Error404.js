import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("404 Error");
    }

    async getHtml() {
        return `
            <div class="HeaderArea" id="HeaderArea">
                <div class="big-text">404 ERROR</div>
                <div class="small-text">Problaly you lost in our website!</div>
            </div>`;
    }
}
const successSfx = new Audio('./sounds/sfxSuccess.mp3');
const failureSfx = new Audio('./sounds/sfxFailure.mp3');

import { notify } from "@kyvg/vue3-notification";

export default {
    hide: false,
    soundOn: true,
    isHidden() {
        if(document.getElementsByClassName('header__offline-bar').length > 0)
                this.hide = true;
        else    this.hide = false;
        return  this.hide;
    },
    notifySuccess(msg) {
        notify({ title: msg, type: 'success' });
        if(this.soundOn) successSfx.play();
    },
    notifyInfo(msg) {
        notify({ title: msg });
        if(this.soundOn) successSfx.play();
    },
    notifyWarning(msg) {
        if(this.isHidden()) return;
        
        notify({ title: msg, type: 'warn' });
        console.warn(msg);
        if(this.soundOn) failureSfx.play();
    },
    notifyError(msg) {
        if(this.isHidden()) return;

        notify({ title: msg, type: 'error' });
        console.error(msg);
        if(this.soundOn) failureSfx.play();
    },
}
const successSfx = new Audio('./sounds/sfxSuccess.mp3');
const failureSfx = new Audio('./sounds/sfxFailure.mp3');

import { notify } from "@kyvg/vue3-notification";

export default {
    hide: false,
    soundOn: true,
    isHidden() {
        // if(document.getElementsByClassName('header__offline-bar').length > 0)
        //         this.hide = true;
        // else    this.hide = false;
        return  this.hide;
    },
    notifySuccess(msg) {
        console.log(msg);
        if(this.isHidden()) return;

        notify({ title: msg, type: 'success' });
        this.playSfx('success');
    },
    notifyInfo(msg) {
        console.log(msg);
        if(this.isHidden()) return;

        notify({ title: msg });
        this.playSfx('success');
    },
    notifyWarning(msg) {
        console.warn(msg);
        if(this.isHidden()) return;

        notify({ title: msg, type: 'warn', clean: true });
        this.playSfx('error');
    },
    notifyError(msg) {
        console.error(msg);
        if(this.isHidden()) return;

        notify({ title: msg, type: 'error', clean: true });
        this.playSfx('error');
    },
    playSfx(type) {
        if(!this.soundOn)   return;
        (type == 'success') ? successSfx.play() : failureSfx.play();
    }
}
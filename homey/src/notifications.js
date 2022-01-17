const successSfx = new Audio('./sounds/sfxSuccess.mp3');
const failureSfx = new Audio('./sounds/sfxFailure.mp3');

import { notify } from "@kyvg/vue3-notification";

export default {
    notifySuccess(msg) {
        notify({ title: msg, type: 'success' });
        successSfx.play();
    },
    notifyInfo(msg) {
        notify({ title: msg });
        successSfx.play();
    },
    notifyWarning(msg) {
        notify({ title: msg, type: 'warn' });
        console.warn(msg);
        failureSfx.play();
    },
    notifyError(msg) {
        notify({ title: msg, type: 'error' });
        console.error(msg);
        failureSfx.play();
    },
}
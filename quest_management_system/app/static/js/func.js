//////////////////////////// Helping func ///////////////////////////

function el(el_selector) { return document.querySelector(el_selector); }
function els(el_selector) { return document.querySelectorAll(el_selector); }
function clog(val) { console.log(val); }

function change_class(ident, class_remove, class_add, text = 'none') {
    //clog(ident);
    if (ident != null) {
        if (ident.classList.contains(class_remove))
            ident.classList.remove(class_remove);
        if (!ident.classList.contains(class_add))
            ident.classList.add(class_add);
        if (text != 'none')
            ident.innerHTML = text;
    }
}

//////////////////////////////// Progressbar //////////////////////////

function set_progressbar(ident, sig_) { // set progress bar (pb)
    let sum = 0;
    let stat = document.getElementsByClassName('start-number')[0]; // pb status id

    let correct_sig_array = el('#pb_sig').innerHTML.split(',');
    // clog(correct_sig_array);

    if (sig_.str != sig_.last) {        // if sig was changed
        for (i of correct_sig_array) {  // count active signals ='1' in
            let sig_num = Number(parseInt(i) - parseInt(sig_.start_from_1));
            if (sig_.str[sig_num] == '1') {
                sum += 1;
            }
        }
        val_percent = Math.floor(sum / correct_sig_array.length * 100);
        let pb = el(ident);
        pb.style.width = val_percent + "%";
        stat.innerHTML = val_percent + "%";
        document.title = "Indiana " + val_percent + "%";
    }
}


//////////////////////////////// Signals /////////////////////////////

// func get the sig object. If sig.count = number of signals in this quest
function show_sig(sig_) {
    let class_remove = 'badge-secondary';
    let class_add = 'badge-success';

    if (sig_.count == sig_.str.length) {                    // if length of sig correct
        for (i in sig_.str) {

            if (sig_.str[i] != sig_.last[i]) {              // if sig has been changed

                let cur_sig_state = sig_.str[i];
                if (cur_sig_state == '1') {
                    class_remove = 'badge-secondary';
                    class_add = 'badge-success';
                }
                if (cur_sig_state == '0') {
                    class_remove = 'badge-success';
                    class_add = 'badge-secondary';
                }
                // if sig started from 1, sig_.start_from_1=1, else sig_.start_from_1=0
                let sig_num = Number(parseInt(i) + parseInt(sig_.start_from_1));
                let all_changed_sig = els('.s' + sig_num);
                let text = 'none';
                for (sig_el of all_changed_sig) {
                    if (sig_el.innerHTML == 'Close' && cur_sig_state == '1')
                        text = 'Open';
                    if (sig_el.innerHTML == 'Open' && cur_sig_state == '0')
                        text = 'Close';
                    if (sig_el.innerHTML != 'Open' && sig_el.innerHTML != 'Close')
                        text = 'none';
                    change_class(sig_el, class_remove, class_add, text);
                }
            }
        }
    }
}
////////////////////// Server tech_box state ///////////////////

function show_serv_techbox(server_, tech_box_) {
    if (server_) {
        change_class(el('#q_server'), 'badge-danger', 'badge-success');
    }
    else {
        change_class(el('#q_server'), 'badge-success', 'badge-danger');
    }

    if (tech_box_ == 'success') {
        change_class(el('#tech_box'), 'badge-danger', 'badge-success');
    }

    if (tech_box_ == 'danger') {
        change_class(el('#tech_box'), 'badge-success', 'badge-danger');
    }
}

///////////////////////////// BPS /////////////////////////////

// set color of all bps btn
function show_bps(bps_) {

    if (bps_.str.length == bps_.count) {

        for (i in bps_.str) {

            if (bps_.str[i] != bps_.last_str[i]) {
                if (bps_.str[i] == '1') {
                    let ident = el('#b' + Number(parseInt(i) + parseInt(1)));
                    change_class(ident, "btn-warning", "btn-danger");
                }
                if (bps_.str[i] == '0') {
                    let ident = el('#b' + Number(parseInt(i) + parseInt(1)));
                    change_class(ident, "btn-danger", "btn-warning");
                }
            }
        }
    }
}

///////////////////////// Timer /////////////////////////

function timer_show(timer_) {
    let t_ident = el('#q-timer');
    t_ident.innerHTML = timer_.str;
    if (timer_.started)
        change_class(t_ident, 'badge-danger', 'badge-success')
    else
        change_class(t_ident, 'badge-success', 'badge-danger')
}

/////////////////////// Control buttons /////////////////////////

function set_control_btn(play_) {
    if (play_) {
        change_class(el('#start'), 'emp', 'btn-success');
        change_class(el('#stop'), 'btn-success', 'emp');
    } else {
        change_class(el('#start'), 'btn-success', 'emp');
        change_class(el('#stop'), 'emp', 'btn-success');
    }
}

function set_lang_btn(lang_) {
    if (lang_ == 'en') {
        change_class(el('#en'), 'emp', 'btn-success');
        change_class(el('#de'), 'btn-success', 'emp');
        change_class(el('#ru'), 'btn-success', 'emp');
    }
    if (lang_ == 'de') {
        change_class(el('#en'), 'btn-success', 'emp');
        change_class(el('#de'), 'emp', 'btn-success');
        change_class(el('#ru'), 'btn-success', 'emp');
    }
    if (lang_ == 'ru') {
        change_class(el('#en'), 'btn-success', 'emp');
        change_class(el('#de'), 'btn-success', 'emp');
        change_class(el('#ru'), 'emp', 'btn-success');
    }
}

function show_hint_playing(hint_playing_) {
    if (hint_playing_.cur) {
        elem = el('#hi' + hint_playing_.cur);
        change_class(elem, "btn-warning", "btn-success");
    } else {
        if (hint_playing_.last) {
            els_hint = els('.hin');
            for (one_el of els_hint) {
                if (one_el == el('#hi' + hint_playing_.last))
                    change_class(one_el, "btn-success", "btn-warning");
            }
        }
    }
}

function set_test_btn(testing_) {
    if (testing_) {
        change_class(el('#test'), 'emp', 'btn-success');
    } else {
        change_class(el('#test'), 'btn-success', 'emp');
    }
}

////////////////////////// Sound task ///////////////////////////////////////

function show_sound(sound_task_, last_sound_task_) {
    let snd = sound_task_[0];
    let bg = sound_task_[1];
    let snd_ = last_sound_task_[0];
    let bg_ = last_sound_task_[1];

    // set audio btn color
    if (snd != '') {                            // if sound playing
        change_class(el('#' + snd), 'btn-warning', 'btn-success');
        if (snd_ != '' && snd_ != snd) {        // if sound was changed while playing
            change_class(el('#' + snd_), 'btn-success', 'btn-warning');
        }
    } else {
        if (snd_ != '')                         // if sound stoped, change it once
            change_class(el('#' + snd_), 'btn-success', 'btn-warning');
    }

    // set bg btn color
    if (bg != '' && bg_ != '' && bg != bg_)     // if bg has been changed, while playing
        change_class(el('#' + bg_), 'btn-success', 'btn-warning');

    if (bg != '') {                             // if bg playing
        change_class(el('#' + bg), 'btn-warning', 'btn-success');
    }
    else {
        if (bg_ != '')                          // when bg stopped playing, change it once
            change_class(el('#' + bg_), 'btn-success', 'btn-warning');
    }

}
let hide = document.getElementsByClassName('open')[0];
let hideBlock = document.getElementsByClassName('open-block')[0];
hide.onclick = function () {
    hide.classList.toggle('hide')
    hideBlock.classList.toggle('hide');
};
let more = document.getElementsByClassName('more')[0];
let menu = document.getElementsByClassName('settings')[0];
more.onclick = function () {
    menu.classList.toggle('open');
};

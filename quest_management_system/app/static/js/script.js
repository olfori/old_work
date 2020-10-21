$(function () {
    let server = 1;                 // server state, when application was load
    // tech box state, when application was load
    let tech_box = el('#tech_box_state').innerHTML;

    let sig = {
        str: '0',
        last: '0',
        count: el('#sig_count').innerHTML,
        start_from_1: el('#sig_start_from_1').innerHTML
    }

    let timer = {
        time: el('#timer_total').innerHTML,
        started: 0,
        str: el('#q-timer').innerHTML
    };

    let btn = {
        id: '',
        group: '',
        num: 0,
        execute: 0
    }

    let bps = {
        str: '',
        count: el('#bps_count').innerHTML,
        cur: 0,
        last_str: ''
    };

    let hint_playing = {
        cur: '',
        last: ''
    }

    let sound_task = ['', '']
    let last_sound_task = ['', '']

    let lang = '';
    let testing = 0;

    let play = 0;
    let start = -1;
    let set_lang = '';
    let audio_sig = -1;
    let hint_num = '';

    let game_id = '';
    let players = '';

    let game_reset = 0;

    let once_modal = 1;

    setInterval(function () {

        ajax_data();                            // send and cath data to/from the server

        show_sig(sig);                          // show signals on the page
        show_bps(bps);                          // showing bypasses on the page
        show_serv_techbox(server, tech_box);    // show techbox & server state 
        set_progressbar('#pb', sig);            // set progressbar (depends on the count of sig '1')
        set_control_btn(play);                  // 
        timer_show(timer);                      // show timer str_time
        set_lang_btn(lang);
        show_hint_playing(hint_playing);
        show_sound(sound_task, last_sound_task);
        set_test_btn(testing);

        sig.last = sig.str;
        bps.last_str = bps.str;
        hint_playing.last = hint_playing.cur;
        last_sound_task = sound_task;

        // if the modal was closed not by clicking on the button
        if (el('#mainModal').style.display == 'none') {
            if (once_modal) {
                once_modal = 0;
                reset_btn()
                el('#game_input').hidden = true;
            }
        }
        else once_modal = 1;

    }, 1000);

    function ajax_data() {
        var data = new Object();
        data.bps_cur = bps.cur;
        data.start = start;
        data.set_lang = set_lang;
        data.audio_sig = audio_sig;
        data.hint_num = hint_num;
        data.game_id = game_id;
        data.players = players;
        data.game_reset = game_reset;

        data = JSON.stringify(data);
        $.ajax({
            type: "POST",
            url: "/ajax_data",
            data: data,
            success: function (response) {
                var json = jQuery.parseJSON(response)

                sig.str = json.sig;
                timer = json.timer;
                tech_box = json.tech_box;
                play = json.play;
                lang = json.lang;
                hint_playing.cur = json.hint_playing;
                testing = json.testing;
                sound_task = json.sound_task;

                if (json.bps.length == bps.count) {
                    bps.str = json.bps;
                }

                server = 1;

                //console.log(sig.str);
            },
            error: function (error) {
                server = 0;
                tech_box = 'danger';
                timer.enable = 0;
            }
        });
    }

    // If any btn has been clicked
    $('.btn').click(function () {
        if (this.classList.contains('bps'))
            set_btn('bps', this.id)                                 // btn group = bps
        if (this.classList.contains('hin'))
            set_btn('hin', this.id)                                 // btn group = hints
        if (this.classList.contains('aud'))
            set_btn('aud', this.id)                                 // btn group = audio
        if (this.classList.contains('game')) {
            set_btn('game', this.id)                                // btn group = game start stop
            if (this.id == 'start')
                el('#game_input').hidden = false;
        }

        if (this.classList.contains('lang'))
            set_btn('lang', this.id)                                // btn group = lang
        if (this.classList.contains('load'))
            set_btn('load', this.id)                                // btn group = statistics_load
        if (this.classList.contains('audbg'))
            set_btn('audbg', this.id)                               // btn group = audio BG

        if (this.classList.contains('game_reset'))
            set_btn('game_reset', this.id)                          // btn group = game_reset

        if (this.classList.contains('mod-0')) {                     // "abort the action" btn
            el('#game_input').hidden = true;
            reset_btn();
        }

        if (this.classList.contains('mod-1')) {                     // "confirm the action" btn
            el('#game_input').hidden = true;

            if (btn.group == 'bps') {                           // if btn group = bps
                bps.cur = Number(btn.id.replace(/\D+/g, ""));   // get the btn num from id
                ajax_data();                                    // sending current bps num
                bps.cur = 0;
            }

            if (btn.group == 'hin' && !hint_playing.cur && !hint_playing.last) {
                hint_num = btn.id.slice(2);                     // get the btn num from id
                ajax_data();                                    // sending current bps num
                hint_num = '';
            }

            if (btn.group == 'aud') {                           // if btn group = aud
                audio_sig = Number(btn.id.replace(/\D+/g, "")); // get the btn num from id
                ajax_data();                                    // sending current bps num
                audio_sig = -1;
            }

            if (btn.group == 'game') {
                game_id = el('#game_id').value;
                players = el('#players').value;
                if (btn.id == 'start') {
                    start = 1;
                }
                if (btn.id == 'stop') {
                    start = 0;
                    el('#game_id').value = '';
                    el('#players').value = '1';
                }
                ajax_data();
                start = -1;
                game_id = '';
                players = '';
            }

            if (btn.group == 'lang') {
                if (btn.id == 'en') {
                    set_lang = 'en';
                }
                if (btn.id == 'de') {
                    set_lang = 'de';
                }
                if (btn.id == 'ru') {
                    set_lang = 'ru';
                }
                ajax_data();
                set_lang = '';
            }

            if (btn.group == 'load') {
                el('#download-link').click();
            }

            if (btn.group == 'audbg') {

            }

            if (btn.group == 'game_reset') {
                game_reset = 1;
                ajax_data();
                game_reset = 0;
            }

            reset_btn();
        }
        //clog(btn);
    })

    function set_btn(gr, id) {             // set btn parameters
        btn.group = gr;
        btn.id = id;
    }

    function reset_btn() {
        setTimeout(function () {            // Задержка нужна после модальн окна
            if (btn.id != '')
                $('#' + btn.id).blur();     // remove focus from the btn
            btn.group = '';
            btn.id = '';
            btn.num = 0;
            btn.execute = 0;
        }, 1000);
    }
});
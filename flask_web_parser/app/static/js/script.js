//////////////////////////// Helping func ///////////////////////////

function el(el_selector) { return document.querySelector(el_selector); }
function els(el_selector) { return document.querySelectorAll(el_selector); }
function clog(val) { console.log(val); }

/////////////////////////// Ajax function ///////////////////////////
$(function () {
    let search = '';
    let last_search = '';
    let list = [];
    let del_sq = 0;

    let no_data = 0;

    let on_focus = 1;

    setInterval(function () {
        if (1) {             // Если пользователь смотрит
            ajax_data();            // send and cath data to/from the server
            show_list();
        }
    }, 1000);

    function ajax_data() {
        var data = new Object();
        data.search = search;
        data.del_sq = del_sq;
        data = JSON.stringify(data);

        $.ajax({
            type: "POST",
            url: "/ajax_data",
            data: data,
            success: function (response) {
                var json = jQuery.parseJSON(response)
                list = json.lst;
                no_data = json.no_data;

                console.log(no_data);
            },
            error: function (error) {
                //err_ajax = 1;
            }
        });
    }

    function show_list() {              // показываю список, принятый от сервера
        if (last_search != search) {
            last_search = search
            let e = el("#text");
            let txt = '';
            list.forEach(function (item) {
                if (no_data)
                    txt += '<div class="col-sm-2">' + item[1] + '</div>' +
                        '<div class="col-sm-6">' +
                        '<span class="name_sq">' + item[0].slice(0, 30) + '</a>' +
                        '</div>' +
                        '<div class="col-sm-4">' +
                        '<button class="btn btn-danger del_sq" type="button" id="' + item[3] +
                        '"> Del_sq ' + item[3] + '</button>' +
                        '</div>';
                else
                    txt += '<div class="col-sm-2">' + item[1] + '</div>' +
                        '<div class="col-sm-10">' +
                        '<a href="' + item[2] + '">' + item[0].slice(0, 30) + '</a>' +
                        '</div>';

            })
            e.innerHTML = txt;
            list = [];
        }

        if (no_data) {
            el('.no_data').hidden = false;
        } else {
            el('.no_data').hidden = true;
        }

    }

    $('.btn').click(function () {       // If any btn has been clicked
        if (this.classList.contains('search')) {
            set_search();
            clear_focus('.search');
        };
    });

    $(document).on("click", ".del_sq", function () { // Ф-ция для сработки на клик созданной кнопкой
        let id = this.id;
        del_sq = id;
        ajax_data();
        del_sq = 0;
        clear_focus('#' + this.id);
    })

    $(document).on("click", ".name_sq", function () { // Ф-ция для сработки на клик созданной кнопкой
        let sq = this.innerText;
        inp.value = sq;
    })

    function clear_focus(name) {
        setTimeout(function () {        // Задержка нужна после модальн окна
            $(name).blur();             // remove focus from the btn
        }, 500);
    }

    window.onfocus = () => { on_focus = 1; }
    window.onblur = () => { on_focus = 0; }
    inp.onkeydown = (e) => {
        if (e.key == 'Enter') {
            set_search();
            clear_focus(inp);
        }
    }

    function set_search() {
        search = inp.value;
        el('#search').innerText = search;
    }
});
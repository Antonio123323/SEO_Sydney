$(document).ready(function () {

    $.validator.addMethod("usernameRegex", function (value, element) {
        return this.optional(element) || regex_first_last_name.test(value);
    }, "The username must be more than 2 characters long, without special characters or spaces");

    $.validator.addMethod("lastusernameRegex", function (value, element) {
        return this.optional(element) || regex_first_last_name.test(value);
    }, "The last name must be more than 2 characters long, without special characters or spaces");

    $.validator.addMethod("passwordRegex", function (value, element) {
        return this.optional(element) || /[a-z]/.test(value) && /[0-9]/.test(value) && /[A-Z]/.test(value) && /^[0-9A-Za-z]+$/.test(value);
    }, 'Passwords must contain between 8 to 12 characters, including letters (A-Z, a-z) and digits (0-9). They cannot contain special characters (^@()#*+/”?!=.{}~&) or spaces');

    $.validator.addMethod("phoneRegex", function (value, element) {
        return this.optional(element) || /^(\d[- ]?){7,11}$/.test(value);
    }, "The phone number must contain between 7 to 11 characters, without special characters");

    $(function () {
        var form = $("#myform")
        form.validate({
            onfocusout: function (element) {
                if (this.currentElements.length != 0 && this.currentElements[0].name == "email") {
                    rebuidEmail($(this.currentElements[0]))
                }
                this.element(element);
                $(element).valid()
            },
            onkeyup: function (element) {
                $(element).valid()
                $('[name="' + element.name + '"]').val(element.value);
                if ($(element).hasClass("phone")) {
                    if ($('.phone').valid() === false) {
                        $(".phone__icon").css("filter", "invert(8%) sepia(91%) saturate(6844%) hue-rotate(17deg) brightness(94%) contrast(120%)");
                        $(".selected-dial-code").css("color", "#c8102e");
                        $(".iti-arrow").css("border-top", "4px solid #c8102e");
                        $(".intl-tel-input .selected-flag").removeClass("valid");
                        $(".intl-tel-input .selected-flag").addClass("error");
                    }

                    if ($('.phone').valid() === true) {
                        $(".phone__icon").css("filter", "invert(32%) sepia(95%) saturate(1659%) hue-rotate(62deg) brightness(97%) contrast(101%)");
                        $(".selected-dial-code").css("color", "#10b534");
                        $(".iti-arrow").css("border-top", "4px solid #10b534");
                        $(".intl-tel-input .selected-flag").removeClass("error");
                        $(".intl-tel-input .selected-flag").addClass("valid");
                    }
                }
            },

            rules: {
                first_name: {
                    required: true,
                    usernameRegex: true,
                    minlength: 2,
                    maxlength: 60,
                },
                last_name: {
                    required: true,
                    lastusernameRegex: true,
                    minlength: 2,
                    maxlength: 60,
                },
                password: {
                    required: true,
                    passwordRegex: true,
                    minlength: 8,
                    maxlength: 12,
                },
                email: {
                    required: true,
                    email: true,
                },
                phone: {
                    phoneRegex: true,
                    required: true,
                }
            },
            messages: {
                first_name: {
                    required: "The first name field is required",
                    minlength: "The first name must be at least 2 characters long",
                    maxlength: "The first name can be a maximum of 60 characters",
                },

                last_name: {
                    required: "The last name field is required",
                    minlength: "The last name must be at least 2 characters long",
                    maxlength: "The last name can be a maximum of 60 characters",
                },
                password: {
                    required: "The password field is required",
                    minlength: "The password must be at least 8 characters long",
                    maxlength: "The password can be a maximum of 12 characters",
                },
                email: {
                    required: "The email address field is required",
                    email: "The email address must be valid",
                },
                phone: {
                    required: "The phone number field is required",
                }
            },
            submitHandler: function (form, event) {
                event.preventDefault();
                $('.preloader').show();
                $("input[name='first_name']").each(function () {
                    $(this).val($(this).val().substr(0, 60).replace(/[.-]/g, ' ').replace(/\s\s+/g, ' '))
                });
                $("input[name='last_name']").each(function () {
                    $(this).val($(this).val().substr(0, 60).replace(/[.-]/g, ' ').replace(/\s\s+/g, ' '))
                });
                var msg = $(form).serialize();
                var linkAdress = makeSendAdress();
                console.log('linkAdress= ' + linkAdress);
                $.post(linkAdress, msg)
                .done(function (data) {
                    // data уже является объектом JSON, так как Flask возвращает jsonify
                    if (data.status === 'success') {
                        let messageObj = JSON.parse(data.message);  // Парсим JSON-строку
                        if (messageObj.data) {  // Проверяем, есть ли ключ `data`
                            window.location = messageObj.data;  // Перенаправление
                        } else {
                            alert(data.message);
                        }
                        $('.preloader').hide();
                    } else {
                        alert(data.message);
                        $('.preloader').hide();
                    }
                    console.log(data);
                })
                    .fail(function (jqXHR, textStatus, errorThrown) {
                        $('.preloader').hide();
                        if (jqXHR.status == 400) {
                            var obj_data = JSON.parse(jqXHR.responseText)
                            for (key in obj_data.errors) {
                                if (key == "CROB") {
                                    window.location = obj_data.errors[key]
                                } else {
                                    alert(obj_data.errors[key])
                                }
                            }
                        } else {
                            alert('Errore nel modulo di registrazione');
                            console.log(jqXHR)
                        }
                    });

            }
        });
    });
    $(function () {
        var form = $("#myform1")
        form.validate({
            onfocusout: function (element) {
                if (this.currentElements.length != 0 && this.currentElements[0].name == "email") {
                    rebuidEmail($(this.currentElements[0]))
                }
                this.element(element);
                $(element).valid()
            },
            onkeyup: function (element) {
                $(element).valid()
                $('[name="' + element.name + '"]').val(element.value);
                if ($(element).hasClass("phone")) {
                    if ($('.phone').valid() === false) {
                        $(".phone__icon").css("filter", "invert(8%) sepia(91%) saturate(6844%) hue-rotate(17deg) brightness(94%) contrast(120%)");
                        $(".selected-dial-code").css("color", "#c8102e");
                        $(".iti-arrow").css("border-top", "4px solid #c8102e");
                        $(".intl-tel-input .selected-flag").removeClass("valid");
                        $(".intl-tel-input .selected-flag").addClass("error");
                    }

                    if ($('.phone').valid() === true) {
                        $(".phone__icon").css("filter", "invert(32%) sepia(95%) saturate(1659%) hue-rotate(62deg) brightness(97%) contrast(101%)");
                        $(".selected-dial-code").css("color", "#10b534");
                        $(".iti-arrow").css("border-top", "4px solid #10b534");
                        $(".intl-tel-input .selected-flag").removeClass("error");
                        $(".intl-tel-input .selected-flag").addClass("valid");
                    }
                }
            },

            rules: {
                first_name: {
                    required: true,
                    usernameRegex: true,
                    minlength: 2,
                    maxlength: 60,
                },
                last_name: {
                    required: true,
                    lastusernameRegex: true,
                    minlength: 2,
                    maxlength: 60,
                },
                password: {
                    required: true,
                    passwordRegex: true,
                    minlength: 8,
                    maxlength: 12,
                },
                email: {
                    required: true,
                    email: true,
                },
                phone: {
                    phoneRegex: true,
                    required: true,
                }
            },
            messages: {
                first_name: {
                    required: "The first name field is required",
                    minlength: "The first name must be at least 2 characters long",
                    maxlength: "The first name can be a maximum of 60 characters",
                },

                last_name: {
                    required: "The last name field is required",
                    minlength: "The last name must be at least 2 characters long",
                    maxlength: "The last name can be a maximum of 60 characters",
                },
                password: {
                    required: "The password field is required",
                    minlength: "The password must be at least 8 characters long",
                    maxlength: "The password can be a maximum of 12 characters",
                },
                email: {
                    required: "The email address field is required",
                    email: "The email address must be valid",
                },
                phone: {
                    required: "The phone number field is required",
                }
            },
            submitHandler: function (form, event) {
                event.preventDefault();
                $('.preloader').show();
                $("input[name='first_name']").each(function () {
                    $(this).val($(this).val().substr(0, 60).replace(/[.-]/g, ' ').replace(/\s\s+/g, ' '))
                });
                $("input[name='last_name']").each(function () {
                    $(this).val($(this).val().substr(0, 60).replace(/[.-]/g, ' ').replace(/\s\s+/g, ' '))
                });
                var msg = $(form).serialize();
                var linkAdress = makeSendAdress();
                console.log('linkAdress= ' + linkAdress);
                $.post(linkAdress, msg)
                .done(function (data) {
                    // data уже является объектом JSON, так как Flask возвращает jsonify
                    if (data.status === 'success') {
                        let messageObj = JSON.parse(data.message);  // Парсим JSON-строку
                        if (messageObj.data) {  // Проверяем, есть ли ключ `data`
                            window.location = messageObj.data;  // Перенаправление
                        } else {
                            alert(data.message);
                        }
                        $('.preloader').hide();
                    } else {
                        alert(data.message);
                        $('.preloader').hide();
                    }
                    console.log(data);
                })
                    .fail(function (jqXHR, textStatus, errorThrown) {
                        $('.preloader').hide();
                        if (jqXHR.status == 400) {
                            var obj_data = JSON.parse(jqXHR.responseText)
                            for (key in obj_data.errors) {
                                if (key == "CROB") {
                                    window.location = obj_data.errors[key]
                                } else {
                                    alert(obj_data.errors[key])
                                }
                            }
                        } else {
                            alert('Errore nel modulo di registrazione');
                            console.log(jqXHR)
                        }
                    });

            }
        });
    });
});
function makeSendAdress(){
    return '/send';
}
function rebuidEmail(this_element){
    var tmp_el = this_element.val();
    tmp_el = tmp_el.replace(/[\.+]{2,}/g, '.').replace(/^\.+/g, '').replace(/\.+$/g, '').replace(/[,\/]/g, '.'); // заменяем повторяющиеся точки на одну, убираем точки вначале и в конце, заменяем запятую и слеш на точку

    //=========
    tmp_el = tmp_el.replace(/[.]+\s+com$/g, '.com').replace(/\s+com$/g, '.com'); // убираем лишние точки и пробелы перед com
    tmp_el = tmp_el.replace(/[.]+\s+ru$/g, '.ru').replace(/\s+ru$/g, '.ru'); // убираем лишние точки и пробелы перед ru
    tmp_el = tmp_el.replace(/[.]+\s+net$/g, '.net').replace(/\s+net$/g, '.net'); // убираем лишние точки и пробелы перед net
    tmp_el = tmp_el.replace(/[.]+\s+ua$/g, '.ua').replace(/\s+ua$/g, '.ua'); // убираем лишние точки и пробелы перед ua
    //=========

    var brokenDomainsGmail = ['gmil','gmaail','gmaij','gmaila','googlemail','jimail','gmailcom','gimailcom','gaiml','gemail','gilmei','gmael','gmaol','gamail','gamil','glail','gmaik'];
    brokenDomainsGmail.forEach((element) => {     // правка домена gmail
        tmp_el = tmp_el.replace(element, 'gmail');
    });

    var brokenDomainsYandex = ['yande[','jandex'];
    brokenDomainsYandex.forEach((element) => {     // правка домена yandex
        tmp_el = tmp_el.replace(element, 'yandex');
    });

    var brokenDomainsMail = ['email', 'meil'];
    brokenDomainsMail.forEach((element) => {     // правка домена mail.ru
        tmp_el = tmp_el.replace(element, 'mail');
    });

    //=========
    tmp_el = tmp_el.replace(/gmail$/g, 'gmail.com'); // правка на домен первого уровня
    tmp_el = tmp_el.replace(/mail$/g, 'mail.ru'); // правка на домен первого уровня
    tmp_el = tmp_el.replace(/mail\.ry$/g, 'mail.ru'); // правка на домен первого уровня
    //=========
    tmp_el = tmp_el.replace(/\s+/g, '').replace(/[/.]{2,}/g, '.'); // убираем лишние пробелы и повторяющиеся точки
    tmp_el = tmp_el.replace(/@\s+/g, '@').replace(/\s+@/g, '@'); // убираем лишние пробелы до и после собачки
    tmp_el = tmp_el.replace(/[.]+@/g, '@').replace(/@[.]+/g, '@'); // убираем лишние точки до и после собачки

    $('[name=email]').val(tmp_el) //вставляем во все инпуты с именем емейл
}
(function () {
    // Функция для работы с куки
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000)); // Устанавливаем время жизни куки
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(`${name}=`)) {
                return cookie.substring(name.length + 1);
            }
        }
        return null;
    }

    // Функция для добавления значения subid в форму
    function addSubidToForm(subid) {
        const forms = document.querySelectorAll('form'); // Находим все формы на странице
        forms.forEach(form => {
            let subidInput = form.querySelector('input[name="subid"]');
            if (!subidInput) {
                // Если инпут для subid отсутствует, создаём его
                subidInput = document.createElement('input');
                subidInput.type = 'hidden';
                subidInput.name = 'subid';
                form.appendChild(subidInput);
            }
            subidInput.value = subid; // Устанавливаем значение
        });
    }

    // Основная логика
    document.addEventListener('DOMContentLoaded', () => {
        // 1. Ищем существующий subid в формах
        const forms = document.querySelectorAll('form');
        let formSubid = null;

        forms.forEach(form => {
            const subidInput = form.querySelector('input[name="subid"]');
            if (subidInput && subidInput.value !== '{subid}') {
                formSubid = subidInput.value; // Получаем subid из формы
            }
        });

        if (formSubid) {
            // 2. Если subid найден и не равен "{subid}", сохраняем его в куки
            setCookie('subid', formSubid, 30); // Сохраняем на 30 дней
        }

        // 3. Получаем subid из куки
        const storedSubid = getCookie('subid');

        if (storedSubid && storedSubid !== '{subid}') {
            // 4. Добавляем subid в формы
            addSubidToForm(storedSubid);
        }
    });
})();
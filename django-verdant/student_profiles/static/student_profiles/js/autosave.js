/**
 *  Enable auto-saving for the given form.
 */
var autosaveTimers = {};
var autosave_last_form_now = undefined;
function enableAutosave(formsel) {
    autosaveTimers[formsel] = 0;
    var form = $(formsel);
    if (form.length == 0) return;
    var delay = 4000;
    var delayShowSaved = 2000;
    var saveString = '';
    var overlay = $('<div id="overlay">Saving...</div>').appendTo(document.body).css('top', '-3em');

    if (window.form_errors)
    {
        overlay.css({'background-color': 'rgba(232,81,81,0.9)', 'height': '5em', 'top': 0}).html(
            'The data you entered could not be saved.<br/>Please check ' + window.form_errors + '.'
            + ' Afterwards, click "Save draft" at the bottom of the page again.'
        )
        return;
    }

    autosave_last_form_now = function() {
        window.onbeforeunload = null;
        var dataString = form.serialize();
        if (saveString == dataString) {
            // no need to save because nothing changed
            return;
        }
        saveString = dataString;

        overlay.html('Saving...').animate({'top': 0}, 400);

        $.ajax({
            type: "POST",
            data: dataString,
            success: function (msg) {
                if (msg.ok) {
                    overlay.css('background-color', '').html('Saved! <i class="icon ion-pizza"></i>');
                    setTimeout(function () {
                        overlay.animate({'top': '-3em'}, 400);
                    }, delayShowSaved);
                }
                else {
                    overlay.animate({'height': '5em'});
                    overlay.css('background-color', 'rgba(232,81,81,0.9)').html('<strong>Autosave failed:</strong><br>Field(s) require attention. View the form field(s) that need attention by clicking "Save draft" at the bottom of the form.');
                }
            },
            error: function (msg) {
                overlay.animate({'height': '5em'});
                overlay.css('background-color', 'rgba(232,81,81,0.9)').html('<strong>Autosave failed:</strong><br>Field(s) require attention. View the form field(s) that need attention by clicking "Save draft" at the bottom of the form.');
            }
        });
    };

    function save() {
        clearTimeout(autosaveTimers[formsel]);   // we clear the timeout because we only want to save n seconds after the last edit
        window.onbeforeunload = confirmOnPageExit;

        autosaveTimers[formsel] = setTimeout(autosave_last_form_now, delay);
    }

    $(form).find('input').each(function(i, val) {
        $(val).change(save);
        $(val).keyup(save);
    });
    $(form).find('select').each(function(i, val) {
        $(val).change(save);
    });
    $(form).find('textarea').each(function(i, val) {
        $(val).change(save);
        $(val).keyup(save);
    });
}
// stop any autosave timers that might be running at the moment
function stopAutosave() {
    for (var i in autosaveTimers)
    {
        clearTimeout(autosaveTimers[i]);
    }
}
// and then immediately enable it for the profile-form in the view
if (typeof autosave_disabled === 'undefined' || !autosave_disabled) {  // this is so a page can disable autosaving on a single-case basis
    enableAutosave('form.student-profile');
    enableAutosave('form.now-page');
}

var show_all = 0;
//Possibly use cookie

function load_proposal_listing(tag, show_all) {
    var target = $('#proposal-listing');
    target.empty();
    spinner().appendTo(target);
    var url = 'group_proposal_listing?tag=' + tag + '&all=' + show_all;
    target.load(url, function(responseText, textStatus, xhr) {
        target.find('img.spinner').remove();
    })
}

$('#pick-hashtag').live('change', function(event) {
    var tag = $(this).val();
    load_proposal_listing(tag);
    window.location.assign('group_proposals?tag=' + tag);
})

$('#show_all_groups').live('change', function(event) {
    var box = $(this);
    if (box.is(':checked')) { show_all = 1; }
    else { show_all = 0; }
    load_proposal_listing($('#pick-hashtag').val(), show_all);
})

$('.submit_recommendation').live('click', function(event) {
    try { event.preventDefault(); } catch(e) {};
    var button = $(this);
    spinner().appendTo(button);
    var form = button.parents('form')
    var form_data = form.serialize();
    $.post(form.attr('action'), form_data, function(data, textStatus, xhr) {
        //Update with response data
        var toggle_area = button.parents('.toggle_area');
        var readonly_text = toggle_area.find('.recommend_text_readonly');
        readonly_text.removeClass('approved denied');
        readonly_text.addClass(data['state']);
        readonly_text.html(data['text']);
        var toggle_area = form.parents('.toggle_area');
        toggle_area.toggleClass('toggle_opened').toggleClass('toggle_closed'); //Toggle so area closes
    })
    .success(function() {
        button.find('img.spinner').remove();
        //flash_message(voteit.translation['permssions_updated_success'], 'info', true);
    })
    .error(function() {
        button.find('img.spinner').remove();
        //FIXME: Insert flash messages somewhere
        //flash_message(voteit.translation['permssions_updated_error'], 'error', true);
    });
})

$('#add_propsal_button').live('click', function(event) {
    try { event.preventDefault(); } catch(e) {};
    var target = $(this).parents('#new_proposal_section');
    spinner().appendTo(this);
    var url = './_inline_add_group_proposal';
    target.load(url, function(responseText, status, xhr) {
         if (status == "error") {
             //FIXME: Proper translated error text
             flash_message('Add proposal error', 'error', true);
         }
         else {
             //Good stuff?
         }
        target.find('img.spinner').remove();
    })
})

$('#new_proposal_section #deformadd').live('click', function(event) {
    try { event.preventDefault(); } catch(e) {};
    var button = $(this);
    spinner().appendTo(button);
    var form = button.parents('form')
    var form_data = form.serialize();
    form_data += '&add=1'; //XXX Hack to make sure add is in there
    $.post(form.attr('action'), form_data, function(data, status, xhr) {
        //Update with response data
        //debugger;
        var target = $('#new_proposal_section');
        target.empty();
        target.html(data);
        if ($(data).find('.error').length > 0) {
            //Badness
        } else {
            load_proposal_listing($('#pick-hashtag').val(), show_all);
        }
    })
    .error(function(xhr, status, error) {
        button.find('img.spinner').remove();
        //FIXME: Flash message
        flash_message('Server error', 'error', true);
    });
    /*
    .success(function() {
        button.find('img.spinner').remove();
        //flash_message('Added', 'info', true);
        //flash_message(voteit.translation['permssions_updated_success'], 'info', true);
    })
    */

})

$(document).ready(function () {
    load_proposal_listing($('#pick-hashtag').val());
})
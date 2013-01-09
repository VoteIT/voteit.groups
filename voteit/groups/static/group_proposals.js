
$('#pick-hashtag').live('change', function(event) {
    var tag = $(this).val();
    load_proposal_listing(tag);
    window.location.assign('group_proposals?tag=' + tag);
})

function load_proposal_listing(tag) {
    var url = 'group_proposal_listing?tag=' + tag;
    $('#proposal-listing').load(url, function(responseText, textStatus, xhr) {
        //Spinner bs
    })
}

$(document).ready(function () {
    load_proposal_listing($('#pick-hashtag').val());
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
        console.log(data);
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


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
        //Success stuff
    })
    .success(function() {
        button.find('img.spinner').remove();
        flash_message(voteit.translation['permssions_updated_success'], 'info', true);
    })
    .error(function() {
        button.find('img.spinner').remove();
        flash_message(voteit.translation['permssions_updated_error'], 'error', true);
    });
})


$("#discussions span.more a").live('click', function(event) {
    /* IE might throw an error calling preventDefault(), so use a try/catch block. */
    try { event.preventDefault(); } catch(e) {}
    
    var url = $(this).attr('href');
    var body = $(this).parents('div.listing_block').find('span.body');
    var link = $(this)
    $.getJSON(url, function(data) {
        body.empty().append(data['body']);
        link.hide();
    });
});
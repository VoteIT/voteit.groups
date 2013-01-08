
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

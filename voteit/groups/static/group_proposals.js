
function update_recommendation_state(event) {
    event.preventDefault();
    var request = arche.do_request($(event.currentTarget).attr('href'));
    elem = $(event.currentTarget);
    request.done(function() {
        elem.parent().children(['data-state-button']).removeClass('btn-primary').addClass('btn-default');
        elem.addClass('btn-primary');
    });
    request.fail(arche.flash_error);
}

function update_recommendation_text(event) {
    var form = $(event.currentTarget).parents('form');
    var request = arche.do_request(form.attr('action'), {data: form.serialize(), method: 'POST'});
    request.fail(arche.flash_error);
}

$(document).ready(function() {
    var elem; //Outer scope
    $('body').on('click', '[data-state-button]', update_recommendation_state);
    $('body').on('change', '[data-recommendation-text]', update_recommendation_text);
});

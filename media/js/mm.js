var index = {
    init: function() {
        $(document).ready(function() {
            if (!$('#shortener form').length) return;

            // focus URL field or error
            var err = $('#shortener .errorlist:first');
            if (err.length) {
                err.prev().find('input').focus().select();
            } else {
                $('#id_url').focus();
            }
        });
    }
}

var index = {
    init: function() {
        $(document).ready(function() {
            // disable bookmarklet here
            $('#bookmarklet a').click(function(){ return false; });

            if (!$('#shortener form').length) return;

            // focus URL field or error
            var err = $('#shortener .errorlist:first');
            if (err.length) {
                err.prev().find('input').focus().select();
            } else {
                if ($('#id_url').val())
                    $('#id_slug').focus().select();
                else
                    $('#id_url').focus().select();
            }
        });
    }
}

var login = {
    init: function() {
        $(document).ready(function() {
            $('#id_username').focus();
        });
    }
}

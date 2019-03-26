<script type="text/javascript">
$("#id_username").on('input', function(){

    clearTimeout(this.delay);
    this.delay = setTimeout(function(){

        var username = $(this).val();
        $.ajax({
            url     : "{% url  'accounts:validate_username' %}",
            data    : {'username':username},
            dataType: 'json',
            success : function(data) {
                if (data.is_taken) {
                    $("#u-error").html(data.error_message);
                } else {
                    $("#u-error").html("");
                }

            }
        });
    }.bind(this), 800);
})

$("#id_email").on('input', function(){

    clearTimeout(this.delay);
    this.delay = setTimeout(function(){

        var email = $(this).val();

        $.ajax({
            url     : "{% url  'accounts:validate_email' %}",
            data    : {'email':email},
            dataType: 'json',
            success : function(data) {
                if (data.is_taken) {
                    $("#e-error").html(data.error_message);

                } else {
                    $("#e-error").html("");
                }
            }
        });
    }.bind(this), 800);
})
</script>
Lickr.QuestionView = Ember.View.extend({
    templateName: 'question',
    didInsertElement: function () {
        this.$('img').click(function(evt){
            $('.selected').removeClass('selected');
            $('#next').removeAttr('disabled');
            $(this).addClass('selected');
        });
    },

    willDestroyElement: function() {
        var winner = this.$(".selected");
        console.log($(winner).attr("src").replace(/\.\/img\//, ""));
        this.get('controller').send("addImage", $(winner).attr("src").replace(/\.\/img\//, ""));
    }
});

Lickr.ResultsView = Ember.View.extend({
    templateName: 'results',
    didInsertElement: function () {
        var images = this.get("controller").get("selectedImages"),
            array = JSON.stringify(images);
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/process_imgs',
            data: {'imgs': array}
        }).success(function(data){
            var colorDivs = [];
            data = JSON.parse(data);
            
            $("#results_header > h1").empty();
            $("#results_header > h1").html("Your color palette is...");
            $("#results_body_top").empty();
            for(var i = 0; i < data.colors.length; i++){
                var color = data.colors[i],
                    color_div = $("<div class='color'></div>"),
                    code_div = $("<p class='code'></p>");
                $(color_div).css("background-color", color);
                $(code_div).html(color);
                $(color_div).append(code_div);
                if(i < 2) {;
                    $("#results_body_top").append(color_div);
                } else {
                    $("#results_body_bottom").append(color_div);
                }
            }
        });
    }
});
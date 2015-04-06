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
            data = JSON.parse(data);
            var colorDivs = [];
            $("#results_header > h1").empty();
            $("#results_header > h1").html("Your color palette is");
            $("#results_body").empty();
            _.each(data.colors, function (color){
                console.log(color);
                var color_div = $("<div class='color'></div>");
                $(color_div).css("background-color", color.toString());
                $("#results_body").append(color_div);
            });
        });
    }
});
function createRow(){
    return $('<div class="row row-centered"></div>');
}

function createImg(img_path){
    var img= $('<img class="question-img">');
    $(img).attr('src', "./imgs/"+img_path+".jpg");
    $(img).attr('img_id', img_path);
    $(img).click(function(){
        $("#next").attr("disabled", false);
        $(".selected").removeClass("selected");
        $(this).addClass("selected");
    });
    return img;
}

function haveISeenThis(seenImgs, imgObj){
    return _.contains(seenImgs, imgObj['_id']);
}

Lickr.QuestionView = Ember.View.extend({
    templateName: 'question',
    didInsertElement: function () {
        // do we still need to ask a question? (assume yes if we're here)
        // ping the server for images (pass in the current top 4)
        // when done, insert the images

        var getTopColors = function(confDict){
            var colors = Object.keys(confDict);
            colors.sort(function(a, b){
                return confDict[b] - confDict[a]; // descending order
            });

            colors = colors.slice(0,4); // top 4
            var d = {};
            _.each(colors, function(color){
                d[color] = confDict[color];
            });
            return d;
        };
        var controller = this.get('controller'),
            seenImgs = controller.get('seenImgs');

        $.get('http://localhost:8000/get_imgs',{ "colors[]": getTopColors(this.get('controller.confDict'))})
            .done(function(images, index){

                images = $.parseJSON(images);
                var row = createRow();
                _.each(images.imgs, function (path){
                    controller.send('addImg', path);
                    if(!this(seenImgs, path)){
                        $(row).append(createImg(path['_id']));
                        if(index +1 % 3 === 0) {
                            $("#photos").append(row);
                            row = createRow();
                        }
                    }
                }, haveISeenThis);
                $("#photos").append(row);
            });



    },

    willDestroyElement: function() {

    }
});

Lickr.StartView = Ember.View.extend({
    templateName: 'start',
    didInsertElement: function () {
        this.$(".code").click(function(evt){
            $('.color-selected').removeClass('color-selected');
            $('#next').removeAttr('disabled');
            $(evt.target).parent().addClass('color-selected');
        });
    },
    willDestroyElement: function() {
        var fave = this.$(".color-selected");
        this.get('controller').send('favorite', $(fave).find(".code").html());
    }
});

Lickr.ResultsView = Ember.View.extend({
    templateName: 'results',
    willInsertElement: function () {
        var top = getTopColors(this.get('controller.confDict'));
        var colors = _.keys(top);
        $.post('http://localhost:8000/results', {'colors': colors});
    },
    didInsertElement: function () {
        var images = this.get("controller").get("selectedImages"),
            array = JSON.stringify(images);

        var top = getTopColors(this.get('controller.confDict'));
        var colors = _.keys(top);
        var colorDivs = [];
        
        $("#results_header > h1").empty();
        $("#results_header > h1").html("Your color palette is...");
        $("#results_body_top").empty();
        for(var i = 0; i < colors.length; i++){
            var color = colors[i],
                color_div = $("<div class='color'></div>"),
                code_div = $("<p class='code'></p>");
            $(color_div).css("background-color", "#"+color);
            $(code_div).html(color);
            $(color_div).append(code_div);
            if(i < 2) {;
                $("#results_body_top").append(color_div);
            } else {
                $("#results_body_bottom").append(color_div);
            }
        }
    }
});
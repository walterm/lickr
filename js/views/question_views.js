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
        var winner = this.$(".selected"),
            losers = this.$("img:not(.selected)"),
            metric = this.$(winner).attr("metric") == "oversaturated" ?  "55144e864199fe8337b9cc47" : "55144e8b4199fe8337b9cc48";
            result = {};

        result["'"+$(winner).attr("src").replace(/\.\/img\//, "").replace(/\.jpg/,"") + "'"] = 1;

        $(losers).each(function(index, img){
            result["'"+$(img).attr("src").replace(/\.\/img\//, "").replace(/\.jpg/,"") + "'"] = 0;
        });

        // qnt.vote(metric, 'data', qnt._user, result, '192.1.1.1', function(data){
        //     console.log(data);
        // });


    }
});

Lickr.ResultsView = Ember.View.extend({
    templateName: 'results',
    didInsertElement: function (){
        this.$('.color').each(function(index, div){
            var color = '#'+Math.floor(Math.random()*16777215).toString(16);
            $(div).css('background', color);
        });
    }
});
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
            result = {};

        result[$(winner).attr("src").replace(/\.\/img\//, "").replace(/\.jpg/,"")] = 1;

        $(losers).each(function(index, img){
            result[$(winner).attr("src").replace(/\.\/img\//, "").replace(/\.jpg/,"")] = 0;
        });
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